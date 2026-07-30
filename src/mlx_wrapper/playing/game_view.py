import logging

import pygame
from src.mlx_wrapper.base_view import BaseView
from src.mlx_wrapper.mlx_engine import MLXEngine
from src.mlx_wrapper.game_manager import GameManager
from src.parsing.models import Config
from src.obj.entity import NORTH, EAST, SOUTH, WEST
from src.obj.player import Player
from src.ai.behaviors import SpeedyGhost, ShadowGhost, BashfulGhost
from src.ai.states import GhostState
from src.mlx_wrapper.playing.asset_manager import AssetManager
from src.mlx_wrapper.playing.game_session import GameSession


logger = logging.getLogger("pacman")

CELL_SIZE = 32
ENTITY_SIZE = 16


class GameView(BaseView):
    """
    The main gameplay view responsible only for rendering the game state
    and forwarding player inputs.
    """

    def __init__(self, engine: MLXEngine, config: Config,
                 manager: GameManager, level_index: int = 0,
                 player: Player | None = None,
                 cheat_mode_enabled: bool = False,
                 ghosts_frozen: bool = False) -> None:
        """
        Initialize the view, load assets, and start the game session.
        """
        super().__init__(engine)
        self.manager = manager
        self.config = config
        self.level_index = level_index

        self.assets = AssetManager(engine)
        self.session = GameSession(config, level_index, player,
                                   cheat_mode_enabled, ghosts_frozen)

    def on_update(self, delta_time: float) -> None:
        """
        Forward the update tick to the game logic and handle view transitions.

        Args:
            delta_time (float): Time elapsed since the last frame.
        """
        try:
            self.session.update(delta_time)

            if self.session.is_game_over:
                if self.session.is_victory:
                    self._handle_level_complete()
                else:
                    from src.mlx_wrapper.game_over_view import GameOverView
                    game_over = GameOverView(
                        self.engine, self.manager,
                        self.session.player.score, self.config, victory=False
                    )
                    self.manager.set_view(game_over)
        except ImportError:
            logger.error("Failed to import GameOverView.")
        except (AttributeError, TypeError):
            logger.error("Failed to update session or create " +
                         "GameOverView.")

    def _handle_level_complete(self) -> None:
        """Handle transitioning to the next level
        or showing the victory screen."""
        try:
            if self.session.level_index + 1 < len(self.config.level):
                next_view = GameView(
                    self.engine, self.config, self.manager,
                    self.session.level_index + 1,
                    player=self.session.player,
                    cheat_mode_enabled=self.session.cheat_mode_enabled,
                    ghosts_frozen=self.session.ghosts_frozen
                )
                self.manager.set_view(next_view)
            else:
                from src.mlx_wrapper.game_over_view import GameOverView
                victory_view = GameOverView(
                    self.engine, self.manager,
                    self.session.player.score, self.config, victory=True
                )
                self.manager.set_view(victory_view)
        except ImportError:
            logger.error("Failed to import GameOverView or GameView.")
        except (AttributeError, TypeError):
            logger.error("Failed to handle level completion.")

    def on_draw(self) -> None:
        """Render the current state of the game session."""
        start_x_offset = (self.manager.width -
                          (self.session.cols * CELL_SIZE)) // 2
        start_y_offset = (self.manager.height -
                          (self.session.rows * CELL_SIZE)) // 2

        for r in range(self.session.rows):
            for c in range(self.session.cols):
                cell_value = self.session.maze[r][c]
                x = start_x_offset + (c * CELL_SIZE)
                y = start_y_offset + (r * CELL_SIZE)

                if cell_value & NORTH:
                    self.engine.draw_image(self.assets.wall_h_img, x, y)
                if cell_value & SOUTH:
                    self.engine.draw_image(self.assets.wall_h_img, x, y
                                           + CELL_SIZE)
                if cell_value & WEST:
                    self.engine.draw_image(self.assets.wall_v_img, x, y)
                if cell_value & EAST:
                    self.engine.draw_image(self.assets.wall_v_img, x
                                           + CELL_SIZE, y)

        for r, c in self.session.pacgums:
            x, y = start_x_offset + (c * CELL_SIZE), \
                start_y_offset + (r * CELL_SIZE)
            o_x = (CELL_SIZE - ENTITY_SIZE) // 2
            o_y = (CELL_SIZE - ENTITY_SIZE) // 2
            self.engine.draw_image(self.assets.pacgum_img, x + o_x, y + o_y)

        for r, c in self.session.super_pacgums:
            x, y = start_x_offset + (c * CELL_SIZE), \
                start_y_offset + (r * CELL_SIZE)
            o_x = (CELL_SIZE - ENTITY_SIZE) // 2
            o_y = (CELL_SIZE - ENTITY_SIZE) // 2
            self.engine.draw_image(self.assets.super_pacgum_img,
                                   x + o_x,
                                   y + o_y)

        current_dir = self.session.player.current_direction
        if current_dir not in self.assets.player_images:
            current_dir = EAST

        current_player_img = self.assets.\
            player_images[current_dir][self.session.player_anim_frame]
        player_x = start_x_offset + (self.session.player.col * CELL_SIZE)
        player_y = start_y_offset + (self.session.player.row * CELL_SIZE)

        p_offset_x = (CELL_SIZE - ENTITY_SIZE) // 2
        p_offset_y = (CELL_SIZE - ENTITY_SIZE) // 2
        self.engine.draw_image(current_player_img,
                               player_x + p_offset_x,
                               player_y + p_offset_y)

        for ghost in self.session.ghosts:
            ghost_x = start_x_offset + (ghost.col * CELL_SIZE)
            ghost_y = start_y_offset + (ghost.row * CELL_SIZE)

            if isinstance(ghost, ShadowGhost):
                base_img = self.assets.blinky_img
            elif isinstance(ghost, BashfulGhost):
                base_img = self.assets.inky_img
            elif isinstance(ghost, SpeedyGhost):
                base_img = self.assets.pinky_img
            else:
                base_img = self.assets.clyde_img

            current_ghost_img = base_img
            is_visible = True

            if ghost.state == GhostState.RUNNING_AWAY:
                if ghost.is_flashing() and \
                        int(ghost.scared_timer * 4) % 2 != 0:
                    current_ghost_img = self.assets.ghost_scared_img
                elif not ghost.is_flashing():
                    current_ghost_img = self.assets.ghost_scared_img
            elif ghost.state == GhostState.DEAD:
                if int(ghost.death_timer * 8) % 2 != 0:
                    is_visible = False

            if is_visible:
                g_o_x = (CELL_SIZE - ENTITY_SIZE) // 2
                g_o_y = (CELL_SIZE - ENTITY_SIZE) // 2
                self.engine.draw_image(current_ghost_img,
                                       ghost_x + g_o_x,
                                       ghost_y + g_o_y)

        self._draw_hud()

    def _draw_hud(self) -> None:
        """Render the score, lives, and cheat mode status overlay."""
        text_color = (255, 255, 255)
        cheat_color = (100, 150, 255)
        warning_color = (255, 50, 50)
        bottom_y = self.manager.height

        current_time = max(0, int(self.session.time_remaining))
        time_color = warning_color if current_time <= 10 else text_color

        current_lvl = self.session.level_index + 1
        total_lvls = len(self.config.level)
        self.engine.put_small_string(100,
                                     bottom_y - 220,
                                     f"Level: {current_lvl}/{total_lvls}",
                                     text_color)
        self.engine.put_small_string(100,
                                     bottom_y - 200,
                                     f"Time: {current_time}s",
                                     time_color)
        self.engine.put_small_string(100,
                                     bottom_y - 180,
                                     f"Score: {self.session.player.score}",
                                     text_color)
        self.engine.put_small_string(100,
                                     bottom_y - 160,
                                     f"Lives: {self.session.player.lives}",
                                     text_color)

        if self.session.cheat_mode_enabled:
            cheats = []
            if self.session.player.is_invincible:
                cheats.append("INVINCIBLE")
            if self.session.ghosts_frozen:
                cheats.append("GHOSTS FROZEN")
            if self.session.player.speed_boost:
                cheats.append("SPEED BOOST")

            status = "CHEAT MODE: ON" + (" | " + " | ".join(cheats)
                                         if cheats else "")
            self.engine.put_small_string(100,
                                         bottom_y - 140,
                                         status,
                                         text_color)
            self.engine.\
                put_small_string(100, 10, "F1 Invincible | F2 Skip | F3 Freeze"
                                          " | F4 Life | F5 Speed", cheat_color)
        else:
            self.engine.put_small_string(100, 10,
                                         "Press C for Cheat Mode",
                                         cheat_color)

    def on_key_press(self, keycode: int) -> None:
        """
        Forward input commands to the player entity or cheat manager.
        """
        try:
            if keycode in (pygame.K_UP, pygame.K_w):
                self.session.player.queue_direction(NORTH)
            elif keycode in (pygame.K_RIGHT, pygame.K_d):
                self.session.player.queue_direction(EAST)
            elif keycode in (pygame.K_DOWN, pygame.K_s):
                self.session.player.queue_direction(SOUTH)
            elif keycode in (pygame.K_LEFT, pygame.K_a):
                self.session.player.queue_direction(WEST)
            elif keycode in (pygame.K_ESCAPE, pygame.K_p):
                from src.mlx_wrapper.pause_view import PauseView
                pause_view = PauseView(self.engine,
                                       self.manager,
                                       self,
                                       self.config)
                self.manager.set_view(pause_view)
            elif keycode == pygame.K_c:
                self.session.cheat_mode_enabled = not \
                    self.session.cheat_mode_enabled
                if not self.session.cheat_mode_enabled:
                    self.session.player.is_invincible = False
                    self.session.ghosts_frozen = False
                    self.session.player.speed_boost = False
            elif self.session.cheat_mode_enabled:
                self._handle_cheat_key(keycode)
        except ImportError:
            logger.error("Failed to import PauseView.")
        except (AttributeError, TypeError):
            logger.error("Failed to handle input or create PauseView.")

    def _handle_cheat_key(self, key: int) -> None:
        """Apply the cheat corresponding to the pressed function key."""
        if key == pygame.K_F1:
            self.session.player.toggle_invincibility()
        elif key == pygame.K_F2:
            self.session.is_game_over = True
            self.session.is_victory = True
        elif key == pygame.K_F3:
            self.session.ghosts_frozen = not self.session.ghosts_frozen
        elif key == pygame.K_F4:
            self.session.player.add_extra_life()
        elif key == pygame.K_F5:
            self.session.player.toggle_speed_boost()
