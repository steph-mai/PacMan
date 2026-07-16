from abc import ABC

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8


class Entity(ABC):
    """Base class for all movable entities in the maze."""

    def __init__(
            self, start_row: int, start_col: int, move_delay: float) -> None:
        """Initialize a maze entity.

        Args:
            start_row: The initial row position of the entity.
            start_col: The initial column position of the entity.
            move_delay: The delay between movement updates.
        """
        self.start_row: int = start_row
        self.start_col: int = start_col
        self.row: int = start_row
        self.col: int = start_col
        self.current_direction: int = 0
        self.move_timer: float = 0.0
        self.move_delay: float = move_delay

    def _can_move(self, direction: int, current_walls: int) -> bool:
        """Check whether movement in a specific direction is allowed.

        Args:
            direction: The direction to check.
            current_walls: The bitmask of walls in the current cell.

        Returns:
            True if the path is clear, otherwise False.
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
        """Apply the coordinate changes for a chosen direction.

        Args:
            direction: The validated direction to move.
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
        """Reset the entity to its starting position."""
        self.row = self.start_row
        self.col = self.start_col
        self.current_direction = 0
