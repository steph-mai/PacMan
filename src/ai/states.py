from enum import Enum, auto


class GhostState(Enum):
    """Enumeration of ghost behavior states."""

    CHASING = auto()
    RUNNING_AWAY = auto()
    DEAD = auto()
