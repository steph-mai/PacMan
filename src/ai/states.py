"""Ghost state definitions for the Pac-Man game.

This module provides the enumeration of all possible behavioral states
a ghost can exhibit during gameplay.
"""
from enum import Enum, auto


class GhostState(Enum):
    """Enumeration of ghost behavior states.

    Attributes:
        CHASING: The ghost actively hunts the player or patrols its zone.
        RUNNING_AWAY: The ghost is frightened (blue) and moves randomly.
        DEAD: The ghost has been eaten and is returning to its spawn point.
    """

    CHASING = auto()
    RUNNING_AWAY = auto()
    DEAD = auto()
    RANDOM = auto()
