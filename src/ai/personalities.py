from enum import Enum, auto
from typing import Any


class GhostPersonality(Enum):
    """Enumeration of ghost personnalities."""
    SHADOW = auto()  # Blinky(the red ghost) attacks Pac-Man directly.
    # He follows Pac-Man like a shadow.
    SPEEDY = auto()  # Pinky tends to lie in ambush.
    # She aims for the spot where Pac-Man is going to be.
    BASHFUL = auto()  # Inky (the blue ghost) is unpredictable.
    # From time to time, he heads in the opposite direction to Pac-Man.
    POKEY = auto()  # Clyde (the orange ghost) feigns indifference.
    # From time to time, he chooses a direction at random
    # (which may be the direction Pac-Man is heading).
    RANDOM = auto()  # mode_test


def shadow_personality_move(
        ghost: Any,
        maze: list[list[int]],
        player_row: int,
        player_col: int
        ) -> int:
    pass


def speedy_personality_move(
        ghost: Any,
        maze: list[list[int]],
        player_row: int,
        player_col: int
        ) -> int:
    pass


def bashful_personality_move(
        ghost: Any,
        maze: list[list[int]],
        player_row: int,
        player_col: int
        ) -> int:
    pass


def indifference_personality_move(
        ghost: Any,
        maze: list[list[int]],
        player_row: int,
        player_col: int
        ) -> int:
    pass


def random_move(
        ghost: Any,
        maze: list[list[int]],
        player_row: int,
        player_col: int
        ) -> int:
    pass


PERSONALITY_FUNCTION = {
    GhostPersonality.SHADOW: shadow_personality_move,
    GhostPersonality.SPEEDY: speedy_personality_move,
    GhostPersonality.BASHFUL: bashful_personality_move,
    GhostPersonality.POKEY: indifference_personality_move,
    GhostPersonality.RANDOM: random_move,
}
