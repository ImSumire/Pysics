"""
This class represents a node in the physics simulation, defining its position,
state, and behavior. Nodes interact with the environment, and their movement is
influenced by physics, such as gravity and bouncing off the bottom boundary.
"""

# pylint: disable=invalid-name

from typing import List

from numba import njit

# pylint: disable=import-error
from src.constants import H, GRAVITY, NODE_RADIUS
# from src.stick import Stick


class Node:
    """
    The goal of this class is to encapsulate the behavior of nodes within the
    simulation. Nodes can be locked, have a specified mass, and interact with
    sticks. The update method calculates the new position of the node based on
    physics calculations.
    """

    # pylint: disable=too-many-instance-attributes
    def __init__(
        self, pos, locked: bool = False, isNew: bool = True, mass: float = 1.0
    ):
        self.x, self.y = pos
        self.px, self.py = pos

        self.locked = locked
        self.isNew = isNew  # don't apply physics
        self.sticks: List[Stick] = []
        self.mass = mass

    @property
    def pos(self):
        """
        Get the position of an object

        Returns:
            tuple: The x,y position of the object as a tuple
        """
        return self.x, self.y

    def update(self, dt):
        """
        Updates the position of an object.

        Args:
            dt: Time delta since last update

        Process:
            1. Computes new position (x, y) based on current position, velocity and mass
            2. Computes new velocity (px, py) based on current velocity, mass and time
            3. Updates instance attributes with new computed position and velocity
        """

        self.x, self.y, self.px, self.py = self.compute(
            dt, self.x, self.y, self.px, self.py, self.mass
        )

    @staticmethod
    @njit
    # pylint: disable=too-many-arguments
    def compute(dt, x, y, px, py, mass):
        """
        Computes the next position and velocity of an object.
        Args:
            dt: Timestep in seconds
            x: Current x position
            y: Current y position
            px: Current x velocity
            py: Current y velocity
            mass: Mass of the object

        Returns:
            x, y, px, py: Updated position and velocity

        Process:
            1. Calculates new x position and velocity using a leapfrog integrator
            2. Calculates new y position including gravity acceleration
            3. Checks if object bounced off bottom and updates y position and velocity if true
            4. Returns updated position and velocity
        """
        preX = x
        preY = y
        x = 2.0 * x - px
        y = 2.0 * y - py + GRAVITY * dt * dt * mass
        px = preX
        py = preY

        if y > H - NODE_RADIUS:  # bounce off bottom
            excess = y - (H - NODE_RADIUS)
            py = y + 0.5 * (y - py) - excess
            y = H - NODE_RADIUS

        return x, y, px, py
