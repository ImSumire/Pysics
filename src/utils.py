"""
This module provides utility functions used in the physics simulation for
distance calculation and value clamping. These functions are used in various
parts of the simulation, such as calculating distances between nodes and
clamping values for visualization properties.
"""

from math import sqrt

from typing import Tuple


def distance(a: Tuple[float, float], b: Tuple[float, float]):
    """
    Calculates the distance between two points (Euclidean distance)
    https://en.wikipedia.org/wiki/Euclidean_distance

    Args:
        a: Tuple of x,y coordinates of first point
        b: Tuple of x,y coordinates of second point

    Returns:
        distance: Distance between the two points as a float

    Process:
        1. Subtracting the x coordinates of the points and squaring the result
        2. Same for y
        3. Adding the squared differences
        4. Taking the square root of the sum to obtain the distance
    """
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def clamp(n: float, a: float = 0.0, b: float = 255.0):
    """
    Clamps a number between an upper and lower bound

    Args:
        n: Number to clamp
        a: Lower bound (default 0.0)
        b: Upper bound (default 255.0)

    Returns:
        Clamped number: The clamped value of n between a and b
    """
    return min(max(n, a), b)
