from src.parsing.models import Config
from src.obj.entity import Entity

MOVE_DELAY = 0.21
SPEED_BOOST_MULTIPLIER = 1.8


class Player(Entity):
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
        super().__init__(start_row, start_col, MOVE_DELAY)

        self.row: int = start_row
        self.col: int = start_col
        self.config: Config = config
        self.score: int = 0
        self.lives: int = self.config.lives
        self.is_invincible: bool = False
        self.speed_boost: bool = False
        self.next_direction: int = 0

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

        effective_delay = (self.move_delay / SPEED_BOOST_MULTIPLIER
                           if self.speed_boost else self.move_delay)

        if self.move_timer < effective_delay:
            return

        self.move_timer = 0.0
        current_walls = maze[self.row][self.col]

        if self.next_direction != 0 and self._can_move(self.next_direction,
                                                       current_walls):
            self.current_direction = self.next_direction
            self.next_direction = 0
            self._apply_direction(self.current_direction)

        elif self.current_direction != 0 and self.\
                _can_move(self.current_direction, current_walls):
            self._apply_direction(self.current_direction)

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

    def toggle_speed_boost(self) -> None:
        """
        Toggle the speed boost cheat mode on or off.
        """
        self.speed_boost = not self.speed_boost

    def add_extra_life(self) -> None:
        """
        Grant the player an extra life (Cheat Mode feature).
        """
        self.lives += 1
