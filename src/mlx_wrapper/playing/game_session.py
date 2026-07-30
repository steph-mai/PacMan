import random
import logging
import sys
from src.obj.player import Player
from src.obj.level import Level
from src.obj.ghost import Ghost, CHASING_DELAY, SCATTER_DELAY
from src.ai.behaviors import SpeedyGhost, ShadowGhost, BashfulGhost, PokeyGhost
from src.ai.states import GhostState
from src.parsing.models import Config
from mazegenerator import MazeGenerator

logger = logging.getLogger("pacman")


class GameSession:
    """
    Handles the core gameplay logic, state management, and entity updates.
    """

    def __init__(self, config: Config, level_index: int = 0,
                 player: Player | None = None,
                 cheat_mode_enabled: bool = False,
                 ghosts_frozen: bool = False) -> None:
        """
        Initialize a new game session with a specific configuration and level.

        Args:
            config (Config): The parsed configuration data.
            level_index (int): The current level index.
            player (Player | None): The existing player to carry over, if any.
            cheat_mode_enabled (bool): Whether cheat mode is active.
            ghosts_frozen (bool): Whether ghosts are currently frozen.
        """
        self.config = config
        self.time_remaining: float = float(self.config.level_max_time)
        self.level_index = level_index
        self.is_game_over = False
        self.is_victory = False

        self.cheat_mode_enabled = cheat_mode_enabled
        self.ghosts_frozen = ghosts_frozen

        self.player_anim_timer: float = 0.0
        self.player_anim_frame: int = 0

        safe_level_index = min(level_index, len(self.config.level) - 1)
        level_config = self.config.level[safe_level_index]
        self.cols = level_config.width
        self.rows = level_config.height

        if self.level_index == 0:
            current_seed = self.config.seed
        else:
            random.seed(None)
            current_seed = random.randint(1, 9999999)

        try:
            mazegen = MazeGenerator(size=(self.cols, self.rows),
                                    perfect=False,
                                    seed=current_seed)
            self.level = Level(mazegen.maze)
            self.maze = mazegen.maze
        except (AttributeError, IndexError, TypeError, ValueError) as e:
            logger.error(f"External MazeGenerator crashed: {e}.")
            logger.error("Failed to load the level. Exiting game.")
            sys.exit(1)

        start_row, start_col = self.level.find_valid_spawn_position()

        if player is None:
            self.player = Player(start_row, start_col, self.config)
        else:
            self.player = player
            self.player.prepare_for_next_level(start_row, start_col)

        self.pacgums: set[tuple[int, int]] = set()
        self.super_pacgums: set[tuple[int, int]] = set()
        self.ghosts: list[Ghost] = []

        self._setup_collectibles()
        self._setup_ghosts()

        self.phase_timer: float = 0.0
        self.is_scatter_phase: bool = True

    def _setup_collectibles(self) -> None:
        """Populate the maze with pacgums and super-pacgums."""
        corners = [(0, 0), (0, self.cols - 1),
                   (self.rows - 1, 0),
                   (self.rows - 1, self.cols - 1)]
        for r, c in corners:
            self.super_pacgums.add((r, c))

        available_cells: list[tuple[int, int]] = []
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) not in corners and (r, c) != (self.player.row,
                                                        self.player.col) \
                        and self.maze[r][c] != 15:
                    available_cells.append((r, c))

        max_allowed_pacgums = int(len(available_cells) * 0.80)
        actual_count = min(self.config.pacgum, max_allowed_pacgums)

        selected_cells = random.sample(available_cells, actual_count)
        for r, c in selected_cells:
            self.pacgums.add((r, c))

    def _setup_ghosts(self) -> None:
        """Initialize the four main ghosts and their start positions."""
        self.ghosts = [
            ShadowGhost(0, 0, self.rows, self.cols, (255, 0, 0)),
            BashfulGhost(0, self.cols - 1,
                         self.rows, self.cols,
                         (0, 255, 255)),
            SpeedyGhost(self.rows - 1, 0,
                        self.rows, self.cols,
                        (255, 105, 180)),
            PokeyGhost(self.rows - 1,
                       self.cols - 1, self.rows, self.cols,
                       (255, 165, 0))
        ]

    def reverse_all_ghosts(self) -> None:
        """Force all active chasing ghosts to immediately reverse
        their direction.

        This method is triggered during global phase transitions (e.g., from
        Scatter to Chase). It explicitly ignores ghosts that are currently dead
        or scared (running away) to prevent disrupting their specific
        behaviors.
        """
        for ghost in self.ghosts:
            if ghost.state == GhostState.CHASING:
                ghost.reverse_course()

    def update_ghosts_phase(self, delta_time: float) -> None:
        """Update the global Chase/Scatter timer and trigger phase changes.

        The global timer pauses while any ghost is scared. When the timer
        exceeds the current phase's delay, it toggles the phase and forces
        all active ghosts to reverse direction.

        Args:
            delta_time: The elapsed time since the previous update.
        """
        is_any_ghost_scared = any(
            g.state == GhostState.RUNNING_AWAY for g in self.ghosts)
        if is_any_ghost_scared:
            return

        self.phase_timer += delta_time

        if self.phase_timer >= (
                SCATTER_DELAY if self.is_scatter_phase else CHASING_DELAY):
            self.phase_timer = 0.0
            self.is_scatter_phase = not self.is_scatter_phase

            for ghost in self.ghosts:
                ghost.is_scatter_phase = self.is_scatter_phase

            # self.reverse_all_ghosts()

    def update(self, delta_time: float) -> None:
        """
        Update the game state, move entities, and resolve collisions.

        Args:
            delta_time (float): Time elapsed since the last update in seconds.
        """
        if self.is_game_over:
            return

        if not self.cheat_mode_enabled:
            self.time_remaining -= delta_time
        if self.time_remaining <= 0.0:
            self.time_remaining = 0.0
            self.is_game_over = True
            self.is_victory = False
            return

        self.player_anim_timer += delta_time
        if self.player_anim_timer >= 0.1:
            self.player_anim_timer = 0.0
            self.player_anim_frame = (self.player_anim_frame + 1) % 3

        self.player.update_movement(delta_time, self.maze)

        if not self.ghosts_frozen:
            self.update_ghosts_phase(delta_time)
            for ghost in self.ghosts:
                ghost.update_movement(delta_time, self.maze, self.player)

        current_pos = (self.player.row, self.player.col)

        if current_pos in self.pacgums:
            self.pacgums.remove(current_pos)
            self.player.add_score(self.config.points_per_pacgum)

        if current_pos in self.super_pacgums:
            self.super_pacgums.remove(current_pos)
            self.player.add_score(self.config.points_per_super_pacgum)
            for ghost in self.ghosts:
                if ghost.state != GhostState.DEAD:
                    ghost.state = GhostState.RUNNING_AWAY
                    ghost.scared_timer = ghost.scared_delay
                    ghost.reverse_course()

        if not self.pacgums:
            self.is_game_over = True
            self.is_victory = True
            return

        if self._check_ghost_collision() and not self.player.is_invincible:
            is_dead = self.player.lose_life()
            if is_dead:
                self.is_game_over = True
                self.is_victory = False
            else:
                self.player.reset_position()
                for ghost in self.ghosts:
                    ghost.reset_position()
                    ghost.state = GhostState.CHASING

    def _check_ghost_collision(self) -> bool:
        """
        Check if the player occupies the same grid cell as any active ghost.

        Returns:
            bool: True if a fatal collision is detected, False otherwise.
        """
        for ghost in self.ghosts:
            if ghost.row == self.player.row and ghost.col == self.player.col:
                if ghost.state == GhostState.RUNNING_AWAY:
                    ghost.die()
                    self.player.add_score(self.config.points_per_ghost)
                elif ghost.state == GhostState.CHASING and not \
                        self.player.is_invincible:
                    return True
        return False
