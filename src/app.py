"""
This class represents the application for the physics simulation using nodes
and sticks. It includes methods to update the simulation over time and
create sample structures such as textiles, ropes, and squares.
"""

# pylint: disable=invalid-name

from math import cos, pi, radians, sin, sqrt
from random import uniform

from typing import List, Tuple

# pylint: disable=import-error
from src.constants import MAX_STRESS, USE_STRESS
from src.node import Node
from src.stick import Stick


class App:
    """
    The goal of this class is to provide a flexible and interactive environment
    for simulating physics-based structures. Users can create various
    structures, observe their behavior, and customize simulation parameters.
    """

    # pylint: disable=dangerous-default-value
    def __init__(self, nodes: List[Node] = [], sticks: List[Stick] = []):
        self.nodes: List[Node] = nodes
        self.sticks: List[Stick] = sticks

        self.paused = True

    def update(self, dt):
        """
        Updates the simulation by the given time increment

        Args:
            dt: Time increment in seconds

        Process:
            1. Checks if simulation is paused and skips if true
            2. Clips dt to a minimum of 0.01 seconds
            3. Updates each unlocked, non-new node by dt
            4. Updates each stick by removing if over max stress or updating normally
        """
        if self.paused:
            return
        dt = max(dt, 0.01)
        for node in self.nodes:
            if not node.locked and not node.isNew:
                node.update(dt)

        for stick in self.sticks:
            if USE_STRESS and stick.stress > MAX_STRESS:
                self.sticks.remove(stick)
            stick.update()

    def textileSample(
        self,
        pos: Tuple[int, int] = (50, 200),
        width: int = 17,
        height: int = 15,
        pad: int = 20,
    ):
        """
        Generates a textile sample

        Args:
            pos: Tuple[int, int]: The starting position of the grid
            width: int: Width of the grid
            height: int: Height of the grid
            pad: int: Padding between nodes

        Process:
            1. Creates a grid of Node objects with the given width and height
            2. Sets the nodes at the top left and top right corners as locked
            3. Adds all the nodes to the nodes list
            4. Creates horizontal and vertical sticks between nodes
            5. Adds all the sticks to the sticks list
        """

        grid = [
            [
                Node((pos[0] + x * pad, pos[1] + y * pad), False, False, mass=0.6)
                for x in range(width)
            ]
            for y in range(height)
        ]

        grid[0][0].locked = True
        grid[0][-1].locked = True

        for row in grid:
            for node in row:
                self.nodes.append(node)

        for y in range(height):
            for x in range(width - 1):
                self.sticks.append(Stick(grid[y][x], grid[y][x + 1]))

        for y in range(height - 1):
            for x in range(width):
                self.sticks.append(Stick(grid[y][x], grid[y + 1][x]))

    def ropeSample(
        self, pos: Tuple[int, int] = (600, 200), length: int = 15, pad: int = 20
    ):
        """
        Generates a sample rope with a random angle

        Args:
            pos: (Tuple[int, int]): Starting position of the rope
            length: (int): Number of nodes in the rope
            pad: (int): Distance between nodes

        Process:
            1. Generates a random starting rotation
            2. Creates a starting node at the given position
            3. Loops from 1 to length-1
                - Calculates new node position based on rotation and pad
                - Creates new node
                - Creates stick between previous and new node
                - Sets previous to new node
        """

        rot = radians(uniform(0.0, 359.9))
        prev = Node(pos, True, False)
        self.nodes.append(prev)
        for i in range(1, length - 1):
            node = Node(
                (pos[0] + sin(rot) * pad * i, pos[1] + cos(rot) * pad * i), False, False
            )
            self.nodes.append(node)
            self.sticks.append(Stick(prev, node))
            prev = node

    def squareSample(self, pos: Tuple[int, int], width: int = 50):
        """
        Generates a square shape sample

        Args:
            pos: (x, y) position of the square center.
            width: Width of the square sides.

        Process:
            - Generates a random rotation angle
            - Creates 4 nodes at rotated positions from the center
            - Adds the nodes to the nodes list
            - Creates sticks between the nodes
            - Adds the sticks to the sticks list
        """

        rot = radians(uniform(0.0, 359.9))

        a = Node((pos[0], pos[1]), False, False)
        b = Node((pos[0] + sin(rot) * width, pos[1] + cos(rot) * width), False, False)
        c = Node(
            (
                pos[0] + sin(rot + pi * 0.25) * sqrt(2) * width,
                pos[1] + cos(rot + pi * 0.25) * sqrt(2) * width,
            ),
            False,
            False,
        )
        d = Node(
            (
                pos[0] + sin(rot + pi * 0.5) * width,
                pos[1] + cos(rot + pi * 0.5) * width,
            ),
            False,
            False,
        )

        self.nodes.append(a)
        self.nodes.append(b)
        self.nodes.append(c)
        self.nodes.append(d)

        self.sticks.append(Stick(a, b))
        self.sticks.append(Stick(b, c))
        self.sticks.append(Stick(c, d))
        self.sticks.append(Stick(d, a))
        self.sticks.append(Stick(a, c))
        self.sticks.append(Stick(d, b))
