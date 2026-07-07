import arcade
from src.parsing.models import Config

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8
MOVE_DELAY = 0.21


class Player:
    """
    Represents the PacMan player character.

    Tracks the player's position on the grid, remaining lives,
    and handles movement logic with wall collisions.
    """

    def __init__(self, start_row: int, start_col: int, config: Config) -> None:
        """
        Initialize the player at a specific grid position.

        Args:
            start_row (int): Initial row index in the maze grid.
            start_col (int): Initial column index in the maze grid.
        """
        self.start_row: int = start_row
        self.start_col: int = start_col
        self.row: int = start_row
        self.col: int = start_col
        self.config: Config = config
        self.scores: int = 0
        self.lives: int = self.config.lives
        self.is_invincible: bool = False
        self.current_direction: int = 0
        self.next_direction: int = 0
        self.move_timer: float = 0.0
        self.move_delay: float = MOVE_DELAY

    def queue_direction(self, direction: int) -> None:
        """
        Store the player's intended next direction.

        Args:
            direction (int): The directional bitmask (NORTH, EAST,
            SOUTH, WEST).
        """
        self.next_direction = direction

    def update_movement(self, delta_time: float,
                        maze: list[list[int]]) -> None:
        """
        Handle continuous movement based on a timer and wall collisions.

        Args:
            delta_time (float): Time elapsed since the last frame.
            maze (list[list[int]]): The 2D maze array containing wall data.
        """
        self.move_timer += delta_time

        if self.move_timer < self.move_delay:
            return

        self.move_timer = 0.0
        current_walls = maze[self.row][self.col]

        if self.next_direction != 0 and self._can_move(self.next_direction,
                                                       current_walls):
            self.current_direction = self.next_direction
            self.next_direction = 0
            self._apply_movement(self.current_direction)

        elif self.current_direction != 0 and self.\
                _can_move(self.current_direction, current_walls):
            self._apply_movement(self.current_direction)

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

    def _apply_movement(self, direction: int) -> None:
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

    def lose_life(self) -> bool:
        """
        Decrease the player's life count and reset their position to the start.

        Returns:
            bool: True if the player is dead (0 lives remaining),
            False otherwise.
        """
        if self.is_invincible:
            return False

        self.lives -= 1
        return self.lives <= 0

    def reset_position(self) -> None:
        """
        Reset the player's current coordinates back to their
        designated starting position.
        """
        self.row = self.start_row
        self.col = self.start_col

    def prepare_for_next_level(self, new_start_row: int,
                               new_start_col: int) -> None:
        """
        Update the starting coordinates for a new level while maintaining
        score and lives.

        Args:
            new_start_row (int): The safe starting row for the new level.
            new_start_col (int): The safe starting column for the new level.
        """
        self.start_row = new_start_row
        self.start_col = new_start_col
        self.reset_position()

    def add_score(self, points: int) -> None:
        """
        Add points to the player's total score.

        Args:
            points (int): The amount of points to add.
        """
        self.score += points

    def toggle_invincibility(self) -> None:
        """
        Toggle the invincibility cheat mode on or off.
        """
        self.is_invincible = not self.is_invincible

    def add_extra_life(self) -> None:
        """
        Grant the player an extra life (Cheat Mode feature).
        """
        self.lives += 1

    def draw(self, start_x_offset: float,
             start_y_offset: float,
             cell_size: int) -> None:
        """
        Render the player as a yellow circle on the screen.

        Args:
            start_x_offset (float): The X coordinate alignment for the grid.
            start_y_offset (float): The Y coordinate alignment for the grid.
            cell_size (int): The width/height of a single cell in pixels.
        """
        x_center = start_x_offset + (self.col * cell_size) + (cell_size / 2)
        y_center = start_y_offset - (self.row * cell_size) - (cell_size / 2)

        color = arcade.color.ORANGE if self.is_invincible \
            else arcade.color.YELLOW

        arcade.draw_circle_filled(
            x_center,
            y_center,
            cell_size / 3,
            color
        )
