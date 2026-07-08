"""Ghost entity module.

Contains the Ghost class and ghost-related state definitions.
"""

import arcade
from src.ai.states import GhostState, get_running_away_directions
from src.ai.personalities import GhostPersonality, PERSONALITY_FUNCTION

RESPAWN_DELAY: float = 10.0
MOVE_DELAY: float = 0.25


class Ghost:
    """Represent a ghost in the PacMan maze."""

    def __init__(self,
                 start_row: int,
                 start_col: int,
                 max_rows: int,
                 max_cols: int,
                 color: arcade.types.Color,
                 personality: GhostPersonality) -> None:
        """Initialize a ghost instance.

        Args:
            start_row: Initial row position in the maze.
            start_col: Initial column position in the maze.
            max_rows: Number of rows in the maze.
            max_cols: Number of columns in the maze.
            color: Ghost display color.
        """
        self.spawn_row: int = start_row
        self.spawn_col: int = start_col
        self.row: int = start_row
        self.col: int = start_col
        self.max_rows: int = max_rows
        self.max_cols: int = max_cols
        self.state: GhostState = GhostState.CHASING
        self.personality: GhostPersonality = personality
        self.personal_behavior_function = PERSONALITY_FUNCTION[
            self.personality]
        self.color = color
        self.death_timer: float = 0.0
        self.respawn_delay = RESPAWN_DELAY
        self.move_timer: float = 0.0
        self.move_delay: float = MOVE_DELAY

        self.current_direction = 0
        # au début le fantôme est immobile.
        # On ne bloque aucune direction
        # par le suite on l'empêche de faire 1/2 tour spontanément.

    def _choose_direction(
            self,
            maze: list[list[int]],
            player_row: int,
            player_col: int
            ) -> int:
        """
        Update the ghost position based on the his state and then
        on his personality.

        Args:
            player_row: Player row position.
            player_col: Player column position.
        """
        direction = 0

        if self.state == GhostState.RUNNING_AWAY:
            direction = get_running_away_directions(self, maze)

        elif self.state == GhostState.DEAD:
            direction = 0

        elif self.state == GhostState.CHASING:
            direction = self.personal_behavior_function(
                self, maze, player_row, player_col)

        if direction != 0:
            self.current_direction = direction
            self._apply_direction(direction)

    def _apply_direction(self, direction: int):
        if direction == 1:
            self.row -= 1
        if direction == 2:
            self.col += 1
        if direction == 4:
            self.row += 1
        if direction == 8:
            self.col -= 1

    def update_movement(self,
                        delta_time: float,
                        maze: list[list[int]],
                        player_row: int,
                        player_col: int) -> None:
        """Update ghost movement and state each frame.

        Args:
            delta_time: Elapsed time since last update.
            maze: Maze layout as a 2D list.
            player_row: Player row position.
            player_col: Player column position.
        """
        if self.state == GhostState.DEAD:
            self.death_timer -= delta_time
            if self.death_timer <= 0:
                self.state = GhostState.CHASING
            return

        self.move_timer += delta_time
        if self.move_timer < self.move_delay:
            return
        self.move_timer = 0.0

        self._choose_direction(maze, player_row, player_col)

    def die(self) -> None:
        """Mark the ghost as dead and reset its position."""
        self.state = GhostState.DEAD
        self.death_timer = self.respawn_delay
        self.row = self.spawn_row
        self.col = self.spawn_col
        self.current_direction = 0

    def draw(
            self,
            start_x_offset: float,
            start_y_offset: float,
            cell_size: int) -> None:
        """Draw the ghost on the screen.

        Args:
            start_x_offset: X offset of the maze origin.
            start_y_offset: Y offset of the maze origin.
            cell_size: Size of one maze cell.
        """
        x_center = start_x_offset + (self.col * cell_size) + (cell_size / 2)
        y_center = start_y_offset - (self.row * cell_size) - (cell_size / 2)

        display_color = self.color
        if self.state == GhostState.RUNNING_AWAY:
            display_color = arcade.color.BLUE
        elif self.state == GhostState.DEAD:
            display_color = arcade.color.WHITE

        arcade.draw_circle_filled(
            center_x=x_center,
            center_y=y_center,
            radius=cell_size / 2.5,
            color=display_color
        )
