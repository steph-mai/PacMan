"""Ghost entity module.

Contains the Ghost class and ghost-related state definitions.
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
    """Represent a ghost in the PacMan maze. (Base class)"""

    def __init__(self,
                 start_row: int,
                 start_col: int,
                 max_rows: int,
                 max_cols: int,
                 color: RGBcolor
                 ) -> None:

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

    def get_next_direction(self, maze: list[list[int]], player: Player) -> int:
        """
        To be overridden by child classes (ShadowGhost, SpeedyGhost, etc.)
        """
        return 0

    def _choose_direction(
            self,
            maze: list[list[int]],
            player: Player
            ) -> None:

        direction = 0

        if self.state == GhostState.RUNNING_AWAY:
            from src.ai.behaviors import get_running_away_directions
            direction = get_running_away_directions(self, maze)

        elif self.state == GhostState.DEAD:
            direction = 0

        elif self.state == GhostState.CHASING:
            direction = self.get_next_direction(maze, player)

        if direction != 0:
            self.current_direction = direction
            self._apply_direction(direction)

    def update_movement(self,
                        delta_time: float,
                        maze: list[list[int]],
                        player: Player) -> None:

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
        return self.state == GhostState.RUNNING_AWAY and self.scared_timer\
            <= FLASH_DELAY
