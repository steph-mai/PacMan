import pygame
from src.mlx_wrapper.base_view import BaseView
from src.mlx_wrapper.mlx_engine import MLXEngine
from src.mlx_wrapper.game_manager import GameManager
import random
import logging
import sys
from src.obj.player import Player
from src.obj.entity import NORTH, EAST, SOUTH, WEST
from src.obj.level import Level
from src.obj.ghost import Ghost
from src.ai.behaviors import SpeedyGhost, ShadowGhost, BashfulGhost, PokeyGhost
from src.ai.states import GhostState
from src.parsing.models import Config
from mazegenerator import MazeGenerator


logger = logging.getLogger("pacman")
CELL_SIZE = 32


class GameView(BaseView):
    """
    The main gameplay view displaying the maze and handling player actions.
    """

    def __init__(self, engine: MLXEngine, config: Config,
                 manager: GameManager,
                 level_index: int = 0,
                 player: Player | None = None,
                 cheat_mode_enabled: bool = False,
                 ghosts_frozen: bool = False) -> None:
        """
        Initialize the game view, maze data, and player object.
        """
        super().__init__(engine)
        self.manager = manager
        self.config = config
        self.level_index = level_index

        self.wall_h_img = self.engine.load_image(
            "inc/images/maze/horizontalwall.png")
        self.wall_v_img = self.engine.load_image(
            "inc/images/maze/verticalwall.png")
        self.player_images = {
            NORTH: [
                self.engine.load_image("inc/images/pacman/pacman-up/1.png"),
                self.engine.load_image("inc/images/pacman/pacman-up/2.png"),
                self.engine.load_image("inc/images/pacman/pacman-up/3.png")
            ],
            EAST: [
                self.engine.load_image("inc/images/pacman/pacman-right/1.png"),
                self.engine.load_image("inc/images/pacman/pacman-right/2.png"),
                self.engine.load_image("inc/images/pacman/pacman-right/3.png")
            ],
            SOUTH: [
                self.engine.load_image("inc/images/pacman/pacman-down/1.png"),
                self.engine.load_image("inc/images/pacman/pacman-down/2.png"),
                self.engine.load_image("inc/images/pacman/pacman-down/3.png")
            ],
            WEST: [
                self.engine.load_image("inc/images/pacman/pacman-left/1.png"),
                self.engine.load_image("inc/images/pacman/pacman-left/2.png"),
                self.engine.load_image("inc/images/pacman/pacman-left/3.png")
            ]
        }
        self.player_anim_timer: float = 0.0
        self.player_anim_frame: int = 0

        self.pacgum_img = self.engine.load_image(
            "inc/images/maze/other/dot.png")
        self.super_pacgum_img = self.engine.load_image(
            "inc/images/maze/other/strawberry.png")
        self.blinky_img = self.engine.load_image(
            "inc/images/ghosts/blinky.png")
        self.inky_img = self.engine.load_image("inc/images/ghosts/inky.png")
        self.pinky_img = self.engine.load_image("inc/images/ghosts/pinky.png")
        self.clyde_img = self.engine.load_image("inc/images/ghosts/clyde.png")
        self.ghost_scared_img = self.engine.load_image(
            "inc/images/ghosts/blue_ghost.png")
        # self.ghost_flashing_img = self.engine.load_image(
        #     "assets/ghost_flashing.png")
        # self.ghost_dead_img = self.engine.load_image("assets/ghost_dead.png")

        safe_level_index = min(level_index, len(self.config.level) - 1)
        level_config = self.config.level[safe_level_index]
        level_width = level_config.width
        level_height = level_config.height

        current_seed = self.config.seed if (
            self.level_index == 0) else (
                random.randint(1, 9999999))

        try:
            mazegen = MazeGenerator(
                size=(level_width, level_height),
                perfect=False,
                seed=current_seed)
            self.level = Level(mazegen.maze)

        except Exception as e:
            logger.error(f"External MazeGenerator crashed: {e}.")
            logger.error("Failed to load the level. Exiting game.")
            sys.exit(1)

        self.maze = mazegen.maze
        # pas de () après  mazegen.maze car @property dans mazegenerator.py
        # permet d'utiliser une méthode comme une simple variable

        self.cols = level_width
        self.rows = level_height

        start_row, start_col = self.level.find_valid_spawn_position()

        if player is None:
            self.player = Player(start_row, start_col, self.config)
        else:
            self.player = player
            self.player.prepare_for_next_level(start_row, start_col)

        self.pacgums: set[tuple[int, int]] = set()
        self.super_pacgums: set[tuple[int, int]] = set()
        self.ghosts: list[Ghost] = []
        self.setup_collectibles()
        self.setup_ghosts()

        self.is_game_over = False

        self.cheat_mode_enabled: bool = cheat_mode_enabled
        self.ghosts_frozen: bool = ghosts_frozen

    def setup_collectibles(self) -> None:
        """
        Populate the maze with pacgums and place super-pacgums
        in the 4 corners.
        """
        config_pacgum_count = self.config.pacgum

        corners = [
            (0, 0),
            (0, self.cols - 1),
            (self.rows - 1, 0),
            (self.rows - 1, self.cols - 1)
        ]

        for r, c in corners:
            self.super_pacgums.add((r, c))

        available_cells: list[tuple[int, int]] = []

        for r in range(self.rows):
            for c in range(self.cols):
                is_corner = (r, c) in corners
                is_player_start = (r, c) == (self.player.row, self.player.col)
                is_solid_wall = self.level.maze[r][c] == 15

                if not is_corner and not is_player_start and not is_solid_wall:
                    available_cells.append((r, c))

        max_allowed_pacgums = int(len(available_cells) * 0.80)

        if config_pacgum_count > max_allowed_pacgums:
            logger.warning(
                f"Requested pacgum count ({config_pacgum_count}) exceeds 80% "
                f"of available maze cells. Clamped to dynamic maximum: "
                f"{max_allowed_pacgums}."
            )

        actual_pacgum_count = min(config_pacgum_count, max_allowed_pacgums)

        selected_cells = random.sample(available_cells, actual_pacgum_count)

        for r, c in selected_cells:
            self.pacgums.add((r, c))

    def setup_ghosts(self) -> None:
        blinky = ShadowGhost(
            start_row=0,
            start_col=0,
            max_rows=self.rows,
            max_cols=self.cols,
            color=(255, 0, 0)
            )

        inky = BashfulGhost(
            start_row=0,
            start_col=self.cols - 1,
            max_rows=self.rows,
            max_cols=self.cols,
            color=(0, 255, 255)
        )

        pinky = SpeedyGhost(
            start_row=self.rows - 1,
            start_col=0,
            max_rows=self.rows,
            max_cols=self.cols,
            color=(255, 105, 180)
        )

        clyde = PokeyGhost(
            start_row=self.rows - 1,
            start_col=self.cols - 1,
            max_rows=self.rows,
            max_cols=self.cols,
            color=(255, 165, 0)
        )

        self.ghosts = [blinky, inky, pinky, clyde]

    def on_update(self, delta_time: float) -> None:
        """
        Update game logic: handle collectible consumption and game rules.

        Args:
            delta_time (float): Time elapsed since the last frame.
        """
        if self.is_game_over:
            return

        self.player_anim_timer += delta_time
        if self.player_anim_timer >= 0.1:
            self.player_anim_timer = 0.0
            self.player_anim_frame = (self.player_anim_frame + 1) % 3

        self.player.update_movement(delta_time, self.level.maze)

        if not self.ghosts_frozen:
            for ghost in self.ghosts:
                ghost.update_movement(
                    delta_time, self.level.maze,
                    self.player)

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

        if not self.pacgums and not self.super_pacgums:
            self.handle_level_complete()
            return

        if self.check_ghost_collision() and not self.player.is_invincible:
            is_dead = self.player.lose_life()

            if is_dead:
                print(f"Game Over! Final Score: {self.player.score}")
                self.is_game_over = True

                # Import local pour éviter les imports circulaires
                from src.mlx_wrapper.game_over_view import GameOverView
                game_over = GameOverView(
                    self.engine,
                    self.manager,
                    self.player.score,
                    self.config,
                    victory=False
                )
                self.manager.set_view(game_over)
            else:
                self.player.reset_position()

                for ghost in self.ghosts:
                    ghost.reset_position()
                    ghost.state = GhostState.CHASING

    def check_ghost_collision(self) -> bool:
        """
        Check if the player occupies the same grid cell as any active ghost.
        Handles eating scared ghosts directly.

        Returns:
            bool: True if a collision is detected, False otherwise.
        """
        for ghost in self.ghosts:
            if ghost.row == self.player.row and\
               ghost.col == self.player.col:
                if ghost.state == GhostState.RUNNING_AWAY:
                    ghost.die()
                    self.player.add_score(self.config.points_per_ghost)
                elif (
                    ghost.state == GhostState.CHASING
                    and not self.player.is_invincible
                ):
                    return True
        return False

    def handle_level_complete(self) -> None:
        """
        Process level completion. Transitions to the next level if available,
        or prints victory if the game is finished.
        """
        if self.level_index + 1 < len(self.config.level):
            next_view = GameView(self.engine,
                                 self.config,
                                 self.manager,
                                 self.level_index + 1,
                                 player=self.player,
                                 cheat_mode_enabled=self.cheat_mode_enabled,
                                 ghosts_frozen=self.ghosts_frozen)
            self.manager.set_view(next_view)
        else:
            print(f"Game Won! Final Score: {self.player.score}")
            self.is_game_over = True

            from src.mlx_wrapper.game_over_view import GameOverView
            victory_view = GameOverView(
                self.engine,
                self.manager,
                self.player.score,
                self.config,
                victory=True
            )
            self.manager.set_view(victory_view)

    def on_draw(self) -> None:
        """
        Render the maze walls, the player object and the ghosts objects.
        """
        if self.is_game_over:
            return

        start_x_offset = ((self.engine.screen.get_width() - (
            self.cols * CELL_SIZE)) // 2)
        start_y_offset = ((self.engine.screen.get_height() - (
            self.rows * CELL_SIZE)) // 2)

        for r in range(self.rows):
            for c in range(self.cols):
                cell_value = self.level.maze[r][c]

                x = start_x_offset + (c * CELL_SIZE)
                y = start_y_offset + (r * CELL_SIZE)

                if cell_value & NORTH:
                    self.engine.draw_image(self.wall_h_img, x, y)

                if cell_value & SOUTH:
                    self.engine.draw_image(self.wall_h_img, x, y + CELL_SIZE)

                if cell_value & WEST:
                    self.engine.draw_image(self.wall_v_img, x, y)

                if cell_value & EAST:
                    self.engine.draw_image(self.wall_v_img, x + CELL_SIZE, y)

        for r, c in self.pacgums:
            x = start_x_offset + (c * CELL_SIZE)
            y = start_y_offset + (r * CELL_SIZE)
            offset_x = (CELL_SIZE - self.pacgum_img.get_width()) // 2
            offset_y = (CELL_SIZE - self.pacgum_img.get_height()) // 2
            self.engine.draw_image(self.pacgum_img, x + offset_x, y + offset_y)

        for r, c in self.super_pacgums:
            x = start_x_offset + (c * CELL_SIZE)
            y = start_y_offset + (r * CELL_SIZE)
            offset_x = (CELL_SIZE - self.super_pacgum_img.get_width()) // 2
            offset_y = (CELL_SIZE - self.super_pacgum_img.get_height()) // 2
            self.engine.draw_image(self.super_pacgum_img,
                                   x + offset_x, y + offset_y)

        current_dir = self.player.current_direction
        if current_dir not in self.player_images:
            current_dir = EAST

        current_player_img = self.player_images[
            current_dir][self.player_anim_frame]

        player_x = start_x_offset + (self.player.col * CELL_SIZE)
        player_y = start_y_offset + (self.player.row * CELL_SIZE)

        p_offset_x = (CELL_SIZE - current_player_img.get_width()) // 2
        p_offset_y = (CELL_SIZE - current_player_img.get_height()) // 2

        self.engine.draw_image(current_player_img,
                               player_x + p_offset_x,
                               player_y + p_offset_y)

        for ghost in self.ghosts:
            ghost_x = start_x_offset + (ghost.col * CELL_SIZE)
            ghost_y = start_y_offset + (ghost.row * CELL_SIZE)

            if isinstance(ghost, ShadowGhost):
                base_ghost_img = self.blinky_img
            elif isinstance(ghost, BashfulGhost):
                base_ghost_img = self.inky_img
            elif isinstance(ghost, SpeedyGhost):
                base_ghost_img = self.pinky_img
            elif isinstance(ghost, PokeyGhost):
                base_ghost_img = self.clyde_img
            else:
                base_ghost_img = self.blinky_img

            current_ghost_img = base_ghost_img
            is_visible = True

            current_ghost_img = base_ghost_img
            if ghost.state == GhostState.RUNNING_AWAY:
                if ghost.is_flashing():
                    if int(ghost.scared_timer * 4) % 2 == 0:
                        current_ghost_img = base_ghost_img
                    else:
                        current_ghost_img = self.ghost_scared_img
                else:
                    current_ghost_img = self.ghost_scared_img
            elif ghost.state == GhostState.DEAD:
                if int(ghost.death_timer * 8) % 2 == 0:
                    current_ghost_img = base_ghost_img
                else:
                    is_visible = False

            if is_visible:
                g_offset_x = (CELL_SIZE - current_ghost_img.get_width()) // 2
                g_offset_y = (CELL_SIZE - current_ghost_img.get_height()) // 2

                self.engine.draw_image(current_ghost_img, ghost_x + g_offset_x,
                                       ghost_y + g_offset_y)

        self.draw_hud()

    def draw_hud(self) -> None:
        """
        Render the score, lives, and cheat mode status overlay.
        """
        text_color = (255, 255, 255)
        cheat_mode_text_color = (100, 150, 255)
        bottom_y = self.engine.screen.get_height()

        self.engine.put_string(
            10, bottom_y - 30, f"Score: {self.player.score}", text_color)
        self.engine.put_string(
            10, bottom_y - 50, f"Lives: {self.player.lives}", text_color)

        if self.cheat_mode_enabled:
            active_cheats = []
            if self.player.is_invincible:
                active_cheats.append("INVINCIBLE")
            if self.ghosts_frozen:
                active_cheats.append("GHOSTS FROZEN")
            if self.player.speed_boost:
                active_cheats.append("SPEED BOOST")

            status_text = "CHEAT MODE: ON"
            if active_cheats:
                status_text += " | " + " | ".join(active_cheats)

            self.engine.put_string(
                10, bottom_y - 70, status_text, text_color)

            help_text = ("F1 Invincibility | F2 Skip Level | "
                         "F3 Freeze Ghosts | F4 Extra Life | F5 Speed Boost")
            self.engine.put_string(
                10, 10, help_text, cheat_mode_text_color)

        else:
            self.engine.put_string(
                10, 10, "Press C for Cheat Mode", cheat_mode_text_color)

    def on_key_press(self, keycode: int) -> None:
        """
        Queue the user's keyboard inputs for player movement, and
        handle cheat mode toggles.
        """
        if keycode in (pygame.K_UP, pygame.K_w):
            self.player.queue_direction(NORTH)
        elif keycode in (pygame.K_RIGHT, pygame.K_d):
            self.player.queue_direction(EAST)
        elif keycode in (pygame.K_DOWN, pygame.K_s):
            self.player.queue_direction(SOUTH)
        elif keycode in (pygame.K_LEFT, pygame.K_a):
            self.player.queue_direction(WEST)
        elif keycode == pygame.K_c:
            self.cheat_mode_enabled = not self.cheat_mode_enabled
            if not self.cheat_mode_enabled:
                self.player.is_invincible = False
                self.ghosts_frozen = False
                self.player.speed_boost = False
            status = "ON" if self.cheat_mode_enabled else "OFF"
            print(f"[CHEAT MODE] {status}")
        elif self.cheat_mode_enabled:
            self.handle_cheat_key(keycode)

    def handle_cheat_key(self, key: int) -> None:
        """
        Apply the cheat corresponding to the pressed function key.
        Only called while cheat mode is enabled.

        Args:
            key (int): The pressed key code.
        """
        if key == pygame.K_F1:
            self.player.toggle_invincibility()
            status = "ON" if self.player.is_invincible else "OFF"
            print(f"[CHEAT] Invincibility: {status}")

        elif key == pygame.K_F2:
            print("[CHEAT] Skipping level")
            self.handle_level_complete()

        elif key == pygame.K_F3:
            self.ghosts_frozen = not self.ghosts_frozen
            status = "ON" if self.ghosts_frozen else "OFF"
            print(f"[CHEAT] Ghosts frozen: {status}")

        elif key == pygame.K_F4:
            self.player.add_extra_life()
            print(f"[CHEAT] Extra life added. Lives: {self.player.lives}")

        elif key == pygame.K_F5:
            self.player.toggle_speed_boost()
            status = "ON" if self.player.speed_boost else "OFF"
            print(f"[CHEAT] Speed boost: {status}")
