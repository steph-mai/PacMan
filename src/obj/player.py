import arcade
from src.parsing.models import Config
from src.obj.level import Level

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8


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
        self.config = config
        self.scores: int = 0
        self.lives: int = self.config.lives

    def move(self, direction: int, maze: list[list[int]]) -> None:
        """
        Attempt to move the player in a given direction if no wall blocks them.

        Args:
            direction (int): The directional bitmask (NORTH, EAST,
            SOUTH, WEST).
            maze (list[list[int]]): The 2D maze array containing wall data.
        """
        current_walls = maze[self.row][self.col]

        if direction == NORTH and not (current_walls & NORTH):
            self.row -= 1
        elif direction == EAST and not (current_walls & EAST):
            self.col += 1
        elif direction == SOUTH and not (current_walls & SOUTH):
            self.row += 1
        elif direction == WEST and not (current_walls & WEST):
            self.col -= 1

    def lose_life(self) -> bool:
        """
        Decrease the player's life count and reset their position to the start.

        Returns:
            bool: True if the player is dead (0 lives remaining),
            False otherwise.
        """
        self.lives -= 1
        self.row = self.start_row
        self.col = self.start_col
        return self.lives <= 0

    def add_score(self, points: int) -> None:
        """
        Add points to the player's total score.

        Args:
            points (int): The amount of points to add.
        """
        self.score += points

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
        arcade.draw_circle_filled(
            x_center,
            y_center,
            cell_size / 3,
            arcade.color.YELLOW
        )
