from enum import Enum, auto
from typing import TYPE_CHECKING, Any
import random

if TYPE_CHECKING:
    from src.obj.ghost import Ghost

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8


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

def _get_reverse_direction(direction: int) -> int:
    if direction == NORTH:
        return SOUTH
    if direction == SOUTH:
        return NORTH
    if direction == EAST:
        return WEST
    if direction == WEST:
        return EAST

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
        ghost: "Ghost",
        maze: list[list[int]],
        player_row: int,
        player_col: int
        ) -> int:

    current_walls = maze[ghost.row][ghost.col]

    valid_directions = []
    if not (current_walls & NORTH):
        valid_directions.append(NORTH)
    if not (current_walls & EAST):
        valid_directions.append(EAST)
    if not (current_walls & SOUTH):
        valid_directions.append(SOUTH)
    if not (current_walls & WEST):
        valid_directions.append(WEST)
    reverse_direction = _get_reverse_direction(ghost.current_direction)
    if reverse_direction in valid_directions and len(valid_directions) > 1:
        valid_directions.remove(reverse_direction)

    return random.choice(valid_directions)


PERSONALITY_FUNCTION = {
    GhostPersonality.SHADOW: shadow_personality_move,
    GhostPersonality.SPEEDY: speedy_personality_move,
    GhostPersonality.BASHFUL: bashful_personality_move,
    GhostPersonality.POKEY: indifference_personality_move,
    GhostPersonality.RANDOM: random_move,
}
