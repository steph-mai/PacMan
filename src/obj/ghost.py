"""Ghost entity module.

This module defines the Ghost base class and ghost-related state definitions.
"""

from src.obj.entity import Entity
from src.obj.player import Player
from src.ai.states import GhostState

RESPAWN_DELAY: float = 5.0
SCARED_DELAY: float = 10.0
MOVE_DELAY: float = 0.25
FLASH_DELAY: float = 3.0

RGBcolor = tuple[int, int, int]


class Ghost(Entity):
    """Represent a ghost in the Pac-Man maze.

    This is a base class for concrete ghost implementations.
    """

    def __init__(
        self,
        start_row: int,
        start_col: int,
        max_rows: int,
        max_cols: int,
        color: RGBcolor,
    ) -> None:
        """Initialize a ghost instance.

        Args:
            start_row: The initial row position of the ghost.
            start_col: The initial column position of the ghost.
            max_rows: The total number of rows in the maze.
            max_cols: The total number of columns in the maze.
            color: The RGB color of the ghost.
        """

        super().__init__(start_row, start_col, MOVE_DELAY)
        self.spawn_row: int = start_row
        self.spawn_col: int = start_col
        self.max_rows: int = max_rows
        self.max_cols: int = max_cols
        self.state: GhostState = GhostState.CHASING
        self.color = color
        self.death_timer: float = 0.0
        self.scared_timer: float = 0.0
        self.scared_delay = SCARED_DELAY
        self.respawn_delay = RESPAWN_DELAY

    def _get_next_direction(
            self, maze: list[list[int]], player: Player) -> int:
        """Return the next direction for the ghost.

        Args:
            maze: A 2D grid representing the maze layout.
            player: The player entity used to determine the ghost behavior.

        Returns:
            The next movement direction to apply.
        """
        return 0

    def _choose_direction(
        self,
        maze: list[list[int]],
        player: Player,
    ) -> None:
        """Choose and apply a movement direction based on the ghost state.

        Args:
            maze: A 2D grid representing the maze layout.
            player: The player entity used to determine the ghost behavior.
        """

        direction = 0

        if self.state == GhostState.RUNNING_AWAY:
            from src.ai.behaviors import get_running_away_directions

            direction = get_running_away_directions(self, maze)

        elif self.state == GhostState.DEAD:
            direction = 0

        elif self.state == GhostState.CHASING:
            direction = self._get_next_direction(maze, player)

        if direction != 0:
            self.current_direction = direction
            self._apply_direction(direction)

    def reverse_course(self) -> None:
        """Force the ghost to reverse its current direction immediately."""
        from src.ai.behaviors import get_reverse_direction

        reverse_dir = get_reverse_direction(self.current_direction)
        if reverse_dir != 0:
            self.current_direction = reverse_dir
            self._apply_direction(reverse_dir)

    def update_movement(
        self,
        delta_time: float,
        maze: list[list[int]],
        player: Player,
    ) -> None:
        """Update the ghost's movement state.

        Args:
            delta_time: The elapsed time since the previous update.
            maze: A 2D grid representing the maze layout.
            player: The player entity used to determine the ghost behavior.
        """

        if self.state == GhostState.DEAD:
            self.death_timer -= delta_time
            if self.death_timer <= 0:
                self.state = GhostState.CHASING
            return

        if self.state == GhostState.RUNNING_AWAY:
            self.scared_timer -= delta_time
            if self.scared_timer <= 0:
                self.state = GhostState.CHASING

        self.move_timer += delta_time
        if self.move_timer < self.move_delay:
            return
        self.move_timer = 0.0

        self._choose_direction(maze, player)

    def die(self) -> None:
        """Mark the ghost as dead and reset its position."""
        self.state = GhostState.DEAD
        self.death_timer = self.respawn_delay
        self.reset_position()

    def is_flashing(self) -> bool:
        """Return whether the ghost is in its scared state and flashing.

        Returns:
            True if the ghost is scared and its scare timer is below the flash
            threshold.
        """
        return self.state == GhostState.RUNNING_AWAY and\
            self.scared_timer <= FLASH_DELAY
