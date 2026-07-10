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


def _get_valid_directions(
        ghost: "Ghost",
        maze: list[list[int]]) -> list[int]:

    current_walls = maze[ghost.row][ghost.col]

    valid_directions = []
    if not (current_walls & NORTH):
        valid_directions.append(NORTH)
    if not (current_walls & WEST):
        valid_directions.append(WEST)
    if not (current_walls & SOUTH):
        valid_directions.append(SOUTH)
    if not (current_walls & EAST):
        valid_directions.append(EAST)
    reverse_direction = _get_reverse_direction(ghost.current_direction)
    if reverse_direction in valid_directions and len(valid_directions) > 1:
        valid_directions.remove(reverse_direction)

    return valid_directions


def shadow_personality_move(
        ghost: "Ghost",
        maze: list[list[int]],
        player_row: int,
        player_col: int
        ) -> int:

    valid_directions = _get_valid_directions(ghost, maze)
    if not valid_directions:
        return 0

    best_direction = 0
    min_distance = float('inf')

    for direction in valid_directions:
        next_row = ghost.row
        next_col = ghost.col
        if direction == NORTH:
            next_row -= 1
        elif direction == EAST:
            next_col += 1
        elif direction == SOUTH:
            next_row += 1
        elif direction == WEST:
            next_col -= 1

        distance = calculate_as_the_crow_flies_distance(next_row, next_col, player_row, player_col)

        if distance < min_distance:
            min_distance = distance
            best_direction = direction

    return best_direction


def calculate_as_the_crow_flies_distance(row1, col1, row2, col2):
    return (row1 - row2)**2 + (col1 - col2)**2


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

    valid_directions = _get_valid_directions(ghost, maze)
    return random.choice(valid_directions)


PERSONALITY_FUNCTION = {
    GhostPersonality.SHADOW: shadow_personality_move,
    GhostPersonality.SPEEDY: speedy_personality_move,
    GhostPersonality.BASHFUL: bashful_personality_move,
    GhostPersonality.POKEY: indifference_personality_move,
    GhostPersonality.RANDOM: random_move,
}
