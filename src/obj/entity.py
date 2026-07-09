from abc import ABC

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8


class Entity(ABC):

    def __init__(self, start_row: int, start_col: int, move_delay: float) -> None:
        self.start_row: int = start_row
        self.start_col: int = start_col
        self.row: int = start_row
        self.col: int = start_col
        self.current_direction: int = 0
        self.move_timer: float = 0.0
        self.move_delay: float = move_delay

    def _can_move(self, direction: int, current_walls: int) -> bool:
        """
        Check if movement in a specific direction is blocked by a wall.

        Args:
            direction (int): The direction to check.
            current_walls (int): The bitmask of walls in the current cell.

        Returns:
            bool: True if the path is clear, False otherwise.
        """
        if direction == NORTH and not (current_walls & NORTH):
            return True
        if direction == EAST and not (current_walls & EAST):
            return True
        if direction == SOUTH and not (current_walls & SOUTH):
            return True
        if direction == WEST and not (current_walls & WEST):
            return True
        return False

    def _apply_direction(self, direction: int) -> None:
        """
        Apply the coordinate changes to the player's position.

        Args:
            direction (int): The validated direction to move.
        """
        if direction == NORTH:
            self.row -= 1
        elif direction == EAST:
            self.col += 1
        elif direction == SOUTH:
            self.row += 1
        elif direction == WEST:
            self.col -= 1

    def reset_position(self) -> None:
        self.row = self.start_row
        self.col = self.start_col
        self.current_direction = 0





















# NORTH = 1
# EAST = 2
# SOUTH = 4
# WEST = 8

# class MazeEntity(ABC):
#     """Abstract base class for all moving entities in the maze."""

#     def __init__(self, start_row: int, start_col: int, move_delay: float):
#         self.start_row = start_row
#         self.start_col = start_col
#         self.row = start_row
#         self.col = start_col

#         self.move_timer: float = 0.0
#         self.move_delay: float = move_delay
#         self.current_direction: int = 0

#     def _can_move(self, direction: int, current_walls: int) -> bool:
#         if direction == NORTH and not (current_walls & NORTH): return True
#         if direction == EAST and not (current_walls & EAST): return True
#         if direction == SOUTH and not (current_walls & SOUTH): return True
#         if direction == WEST and not (current_walls & WEST): return True
#         return False

#     def _apply_direction(self, direction: int) -> None:
#         if direction == NORTH: self.row -= 1
#         elif direction == EAST: self.col += 1
#         elif direction == SOUTH: self.row += 1
#         elif direction == WEST: self.col -= 1

#     def reset_position(self) -> None:
#         self.row = self.start_row
#         self.col = self.start_col
#         self.current_direction = 0
