from enum import Enum, auto
from typing import Any


class GhostState(Enum):
    """Enumeration of ghost behavior states."""

    CHASING = auto()
    RUNNING_AWAY = auto()
    DEAD = auto()


def get_running_away_directions(ghost: Any, maze: list[list[int]]) -> int:
    pass
