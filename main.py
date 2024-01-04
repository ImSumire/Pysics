"""
Pysics - Interactive Physics Simulation using Pygame

GitHub Repository: https://github.com/ImSumire/Pysics

Dependencies:
- pygame : `$pip install pygame`
- numba : `$pip install numba`
"""

import sys
# pylint: disable=no-member, invalid-name, too-many-branches, too-many-statements
import pygame as pg

from src.constants import (
    W,
    H,
    SNAP_RADIUS,
    DELETE_RADIUS,
    STICK_WIDTH,
    DELETING_COLOR,
    NODE_PREVIEW_COLOR,
    NODE_RADIUS,
    LOCKED_NODE_COLOR,
    NODE_COLOR,
    WHITE,
)
from src.utils import distance
from src.node import Node
from src.stick import Stick
from src.app import App


def main():
    """
    Simulate a physical system using nodes and sticks.
    
    Processing Logic:
    - Initialize pygame and create display window
    - Create App object to manage nodes and sticks  
    - Load sample configurations using textile, rope, squares
    - Handle mouse and keyboard input for drawing/deleting nodes and sticks
    - Continuously update positions by simulating physics
    - Render nodes, sticks and preview lines to screen
    """
    pg.init()

    screen = pg.display.set_mode((W, H))
    clock = pg.time.Clock()
    app = App()

    app.textileSample()
    app.ropeSample()
    app.squareSample(pos=(900, 300))
    app.squareSample(pos=(1000, 200))
    app.squareSample(pos=(1100, 350))

    while True:
        mPos = pg.mouse.get_pos()
        mState = pg.mouse.get_pressed()
        # If there is a node nearby, start drawing at that node, otherwise, create a new node
        nearest = None
        distNearest = SNAP_RADIUS
        for node in app.nodes:
            dist = distance(mPos, node.pos)
            if dist < distNearest:
                nearest = node
                distNearest = dist

        drawing = False
        deleting = False

        # process inputs
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    app.paused = not app.paused

                elif event.key == pg.K_r:
                    app.sticks = []
                    app.nodes = []
                    app.paused = True

                elif event.key == pg.K_e:
                    app.sticks = []
                    app.nodes = []
                    app.paused = True

                    app.textileSample()
                    app.ropeSample()
                    app.squareSample(pos=(900, 300))
                    app.squareSample(pos=(1000, 200))
                    app.squareSample(pos=(1200, 350))

            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if nearest:
                    nodeA = nearest
                else:
                    nodeA = Node(mPos)
                    app.nodes.append(nodeA)

            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                if nearest:
                    nodeB = nearest
                else:
                    nodeB = Node(mPos)
                    app.nodes.append(nodeB)

                if nodeA != nodeB:
                    if not any(nodeB in stick.nodes for stick in nodeA.sticks):
                        app.sticks.append(Stick(nodeA, nodeB))
                elif not nodeA.isNew:
                    nodeA.locked = not nodeA.locked

                nodeA.isNew = False
                nodeB.isNew = False

        # Left mouse is being held, preview stick placement
        if mState[0]:
            drawing = True

        # If right mouse button is being held, remove any object hovered near
        if not drawing and mState[2]:
            deleting = True
            if nearest:
                app.nodes.remove(nearest)
                for stick in nearest.sticks:
                    try:
                        app.sticks.remove(stick)
                    except ValueError:
                        pass
            for stick in app.sticks:
                if distance(mPos, stick.center) < DELETE_RADIUS + STICK_WIDTH:
                    app.sticks.remove(stick)

        app.update(clock.tick() / 1000.0)

        # Render
        screen.fill(0)

        if deleting:
            pg.draw.circle(screen, DELETING_COLOR, mPos, DELETE_RADIUS)

        if drawing:
            pg.draw.line(
                screen,
                NODE_PREVIEW_COLOR,
                nodeA.pos,
                nearest.pos if nearest else mPos,
                STICK_WIDTH,
            )

        pg.draw.circle(
            screen,
            NODE_PREVIEW_COLOR,
            nearest.pos if nearest else mPos,
            NODE_RADIUS,
        )

        for stick in app.sticks:
            pg.draw.line(
                screen, stick.stressColor, stick.a.pos, stick.b.pos, STICK_WIDTH
            )
        for node in app.nodes:
            pg.draw.circle(
                screen,
                LOCKED_NODE_COLOR if node.locked else NODE_COLOR,
                node.pos,
                NODE_RADIUS,
            )

        if app.paused:
            pg.draw.rect(screen, WHITE, pg.Rect(20, 20, 7, 25))
            pg.draw.rect(screen, WHITE, pg.Rect(33, 20, 7, 25))

        clock.tick(600)
        pg.display.flip()
        pg.display.set_caption(f"Fps: {int(clock.get_fps())}")


if __name__ == "__main__":
    main()
