"""Ghost movement behavior helpers for the Pac-Man game."""

from src.obj.entity import NORTH, WEST, SOUTH, EAST
from src.obj.ghost import Ghost
from src.obj.player import Player


class ShadowGhost(Ghost):
    """Blinky behavior: always target the player's current position.

    This ghost simply chases the player directly and uses the shortest
    straight-line path toward the player's current cell.
    """
    def _get_next_direction(
            self, maze: list[list[int]], player: Player) -> int:
        return self._get_direction_towards_target(
            maze, player.row, player.col)


class SpeedyGhost(Ghost):
    """Pinky behavior: target four cells ahead of the player.

    This ghost predicts the player's movement and tries to intercept
    four cells in front of the player's current direction.
    """
    def _get_next_direction(
            self, maze: list[list[int]], player: Player) -> int:
        dir_row, dir_col = 0, 0
        if player.current_direction == NORTH:
            dir_row = -1
        elif player.current_direction == SOUTH:
            dir_row = 1
        elif player.current_direction == EAST:
            dir_col = 1
        elif player.current_direction == WEST:
            dir_col = -1

        target_row = player.row + (4 * dir_row)
        target_col = player.col + (4 * dir_col)

        return self._get_direction_towards_target(
            maze, target_row, target_col)


class BashfulGhost(Ghost):
    """Inky behavior: target four cells behind the player.

    This ghost aims for a point four cells behind the player's current
    direction, creating a more indirect pursuit path.
    """
    def _get_next_direction(
            self, maze: list[list[int]], player: Player) -> int:
        dir_row, dir_col = 0, 0
        if player.current_direction == NORTH:
            dir_row = -1
        elif player.current_direction == SOUTH:
            dir_row = 1
        elif player.current_direction == EAST:
            dir_col = 1
        elif player.current_direction == WEST:
            dir_col = -1

        target_row = player.row - (4 * dir_row)
        target_col = player.col - (4 * dir_col)

        return self._get_direction_towards_target(
            maze, target_row, target_col)


class PokeyGhost(Ghost):
    """Clyde behavior: chase the player until close, then wander away.

    If the player is farther than five cells away (squared distance > 25),
    this ghost chases the player. Otherwise, it behaves like a scared ghost
    and moves randomly.
    """
    def _get_next_direction(
            self, maze: list[list[int]], player: Player) -> int:
        distance_square_to_player = self._calculate_as_the_crow_flies_distance(
            self.row, self.col, player.row, player.col)
        if distance_square_to_player > 64:
            return self._get_direction_towards_target(
                maze, player.row, player.col)
        else:
            return self._get_direction_towards_target(
                maze, self.spawn_row, self.spawn_col)
