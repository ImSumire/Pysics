"""
This class represents a stick connecting two nodes in the physics simulation.
It defines properties and methods related to the stick's length, center, stress,
and visualization properties. Sticks influence the positions of connected nodes
based on their relative distances.
"""

# pylint: disable=invalid-name

from typing import Tuple

# pylint: disable=import-error
from src.constants import MAX_STRESS_FACTOR
from src.utils import distance, clamp
from src.node import Node


class Stick:
    """
    The goal of this class is to encapsulate the behavior of sticks within the
    simulation. Sticks connect nodes, exert forces on them, and are subject to
    stress calculations. Visualization properties, such as stress color, are
    provided for rendering.
    """

    def __init__(self, a: Node, b: Node):
        self.a = a
        self.b = b
        self.nodes: Tuple[Node, Node] = a, b

        self.len = distance(self.a.pos, self.b.pos)
        self.halfLen = self.len * 0.5

        a.sticks.append(self)
        b.sticks.append(self)

    @property
    def dist(self):
        """
        Calculates self distance between a & b

        Returns:
            distance: Distance between points a and b
        """

        return distance(self.a.pos, self.b.pos)

    @property
    def center(self):
        """
        Returns the center point between a & b

        Returns:
            tuple: The x,y coordinates of the center point
        """

        return (
            (self.a.x + self.b.x) * 0.5,
            (self.a.y + self.b.y) * 0.5,
        )

    @property
    def stress(self):
        """
        Calculates stress on an object by subtracting its length from its dist

        Returns:
            stress: Difference between distance and length of the object
        """

        return self.dist - self.len

    @property
    def stressColor(self):
        """
        Returns a tuple representing the color of stress

        Returns:
            tuple: A 3-tuple representing RGB color values between 0-255
        """

        return (
            clamp(30.0 + self.stress * 225.0 * MAX_STRESS_FACTOR),
            clamp(120.0 - self.stress * 8.0),
            50,
        )

    def update(self):
        """
        Updates the positions of the stick endpoints

        Process:
            1. Calculate the center point and distance factor of the spring
            2. Calculate the direction vectors from the center to each endpoint
            3. If endpoint a is not locked, update its position
            4. Same for b
        """

        cx, cy = self.center
        distFact = 1.0 / self.dist
        sDirX = (self.a.x - self.b.x) * distFact
        sDirY = (self.a.y - self.b.y) * distFact

        if not self.a.locked:
            self.a.x = cx + sDirX * self.halfLen
            self.a.y = cy + sDirY * self.halfLen

        if not self.b.locked:
            self.b.x = cx - sDirX * self.halfLen
            self.b.y = cy - sDirY * self.halfLen
