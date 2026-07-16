"""Ghost movement behavior helpers for the Pac-Man game."""

from src.obj.entity import NORTH, WEST, SOUTH, EAST
from src.obj.ghost import Ghost
from src.obj.player import Player
import random

DIRECTIONS_VECTORS = {
            NORTH: (-1, 0),
            EAST: (0, 1),
            SOUTH: (1, 0),
            WEST: (0, -1),
        }


def get_reverse_direction(direction: int) -> int:
    """Return the opposite maze direction for a given direction.

    Args:
        direction (int): One of NORTH, EAST, SOUTH, or WEST.

    Returns:
        int: The opposite direction constant, or 0 if the input is invalid.
    """
    if direction == NORTH:
        return SOUTH
    if direction == SOUTH:
        return NORTH
    if direction == EAST:
        return WEST
    if direction == WEST:
        return EAST
    return 0


def _get_valid_directions(
        ghost: Ghost,
        maze: list[list[int]]) -> list[int]:
    """Return valid movement directions from the ghost's current cell.

    The ghost may not move through walls, and it avoids reversing
    direction unless it has no other choice.

    Args:
        ghost (Ghost): The ghost whose movement is being evaluated.
        maze (list[list[int]]): The maze wall grid.

    Returns:
        list[int]: A list of valid direction constants.
    """
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
    reverse_direction = get_reverse_direction(ghost.current_direction)
    if reverse_direction in valid_directions and len(valid_directions) > 1:
        valid_directions.remove(reverse_direction)

    return valid_directions


def get_running_away_directions(ghost: Ghost, maze: list[list[int]]) -> int:
    """Choose a random valid direction for a fleeing ghost.

    This behavior is used when the ghost is in the scared state and
    should wander unpredictably.

    Args:
        ghost (Ghost): The ghost that is running away.
        maze (list[list[int]]): The maze wall grid.

    Returns:
        int: A randomly chosen valid direction constant or 0 if none found.
    """
    valid_directions = _get_valid_directions(ghost, maze)

    if not valid_directions:
        return 0

    return random.choice(valid_directions)


def _calculate_as_the_crow_flies_distance(
        row1: int, col1: int, row2: int, col2: int) -> int:
    """Calculate squared Euclidean distance between two grid positions.

    Using squared distance avoids the cost of a square root while preserving
    ordering comparisons.

    Args:
        row1: Row of first position.
        col1: Column of first position.
        row2: Row of second position.
        col2: Column of second position.

    Returns:
        int: Squared distance between the two positions.
    """
    return (row1 - row2)**2 + (col1 - col2)**2


def get_direction_towards_target(
        ghost: Ghost, maze: list[list[int]],
        target_row: int, target_col: int
        ) -> int:
    """Select the direction that moves the ghost closest to a target.

    The ghost evaluates all valid adjacent moves and chooses the one
    that minimizes the straight-line distance to the target position.

    Args:
        ghost (Ghost): The ghost whose movement is being evaluated.
        maze (list[list[int]]): The maze wall grid.
        target_row (int): Target row coordinate.
        target_col (int): Target column coordinate.

    Returns:
        int: The best direction constant to move toward the target, or 0.
    """
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

        distance = _calculate_as_the_crow_flies_distance(
            next_row,
            next_col,
            target_row,
            target_col)

        if distance < min_distance:
            min_distance = distance
            best_direction = direction

    return best_direction


class ShadowGhost(Ghost):
    """Blinky behavior: always target the player's current position.

    This ghost simply chases the player directly and uses the shortest
    straight-line path toward the player's current cell.
    """
    def get_next_direction(self, maze: list[list[int]], player: Player) -> int:
        return get_direction_towards_target(self, maze, player.row, player.col)


class SpeedyGhost(Ghost):
    """Pinky behavior: target four cells ahead of the player.

    This ghost predicts the player's movement and tries to intercept
    four cells in front of the player's current direction.
    """
    def get_next_direction(self, maze: list[list[int]], player: Player) -> int:
        dir_row, dir_col = DIRECTIONS_VECTORS.get(
            player.current_direction, (0, 0))

        target_row = player.row + (4 * dir_row)
        target_col = player.col + (4 * dir_col)

        return get_direction_towards_target(self, maze, target_row, target_col)


class BashfulGhost(Ghost):
    """Inky behavior: target four cells behind the player.

    This ghost aims for a point four cells behind the player's current
    direction, creating a more indirect pursuit path.
    """
    def get_next_direction(self, maze: list[list[int]], player: Player) -> int:
        dir_row, dir_col = DIRECTIONS_VECTORS.get(
            player.current_direction, (0, 0))

        target_row = player.row - (4 * dir_row)
        target_col = player.col - (4 * dir_col)

        return get_direction_towards_target(self, maze, target_row, target_col)


class PokeyGhost(Ghost):
    """Clyde behavior: chase the player until close, then wander away.

    If the player is farther than five cells away (squared distance > 25),
    this ghost chases the player. Otherwise, it behaves like a scared ghost
    and moves randomly.
    """
    def get_next_direction(self, maze: list[list[int]], player: Player) -> int:
        distance_square_to_player = _calculate_as_the_crow_flies_distance(
            self.row, self.col, player.row, player.col)
        if distance_square_to_player > 25:
            return get_direction_towards_target(
                self, maze, player.row, player.col)
        else:
            return get_running_away_directions(self, maze)
