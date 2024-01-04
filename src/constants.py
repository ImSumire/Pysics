"""
This module defines constants used in the physics simulation application.
These constants control parameters such as screen dimensions, gravity, stress
limits and rendering colors.
"""

W = 1280
H = 720

GRAVITY = 500.0

USE_STRESS = True
MAX_STRESS = 15
MAX_STRESS_FACTOR = 1.0 / MAX_STRESS

SNAP_RADIUS = 20
DELETE_RADIUS = 10

NODE_RADIUS = 3
STICK_WIDTH = 5

WHITE = (255, 255, 255)

NODE_PREVIEW_COLOR = (85, 85, 160)
NODE_COLOR = (255, 255, 255)
LOCKED_NODE_COLOR = (255, 75, 75)
DELETING_COLOR = (255, 105, 105)
