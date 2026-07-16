import arcade
import random
import logging
import sys
from src.obj.player import Player
from src.obj.entity import NORTH, EAST, SOUTH, WEST
from src.obj.level import Level
from src.obj.ghost import Ghost
from src.ai.behaviors import (
    SpeedyGhost, ShadowGhost, BashfulGhost, PokeyGhost, get_reverse_direction)
from src.ai.states import GhostState
from src.parsing.models import Config
from mazegenerator import MazeGenerator
from .game_over_view import GameOverView


logger = logging.getLogger("pacman")
CELL_SIZE = 32


class GameView(arcade.View):
    """
    The main gameplay view displaying the maze and handling player actions.
    """

    def __init__(self, config: Config,
                 level_index: int = 0,
                 player: Player = None) -> None:
        """
        Initialize the game view, maze data, and player object.
        """
        super().__init__()
        self.config = config
        self.level_index = level_index
        arcade.set_background_color(arcade.color.WHITE)

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

        self.cheat_mode_enabled: bool = False
        self.ghosts_frozen: bool = False

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
            color=arcade.color.RED
        )

        inky = BashfulGhost(
            start_row=0,
            start_col=self.cols - 1,
            max_rows=self.rows,
            max_cols=self.cols,
            color=arcade.color.CYAN
        )

        pinky = SpeedyGhost(
            start_row=self.rows - 1,
            start_col=0,
            max_rows=self.rows,
            max_cols=self.cols,
            color=arcade.color.PINK
        )

        clyde = PokeyGhost(
            start_row=self.rows - 1,
            start_col=self.cols - 1,
            max_rows=self.rows,
            max_cols=self.cols,
            color=arcade.color.ORANGE
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

                    reverse_dir = get_reverse_direction(
                        ghost.current_direction)
                    if reverse_dir != 0:
                        ghost.current_direction = reverse_dir
                        ghost._apply_direction(reverse_dir)

        if not self.pacgums and not self.super_pacgums:
            self.handle_level_complete()
            return

        if self.check_ghost_collision() and not self.player.is_invincible:
            is_dead = self.player.lose_life()

            if is_dead:
                print(f"Game Over! Final Score: {self.player.score}")
                self.is_game_over = True
                self.window.show_view(GameOverView(self.player.score,
                                                   self.config,
                                                   victory=False))
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
                elif ghost.state == GhostState.CHASING and not self.player.is_invincible:
                    return True
        return False

    def handle_level_complete(self) -> None:
        """
        Process level completion. Transitions to the next level if available,
        or prints victory if the game is finished.
        """
        if self.level_index + 1 < len(self.config.level):
            next_view = GameView(self.config,
                                 self.level_index + 1,
                                 player=self.player)
            self.window.show_view(next_view)
        else:

            print(f"Game Won! Final Score: {self.player.score}")
            self.is_game_over = True

            self.window.show_view(GameOverView(self.player.score,
                                               self.config,
                                               victory=True))

    def on_draw(self) -> None:
        """
        Render the maze walls, the player object and the ghosts objects.
        """
        self.clear()

        start_x_offset = ((self.window.width - (self.cols * CELL_SIZE)) / 2)
        start_y_offset = ((self.window.height + (self.rows * CELL_SIZE)) / 2)

        for r in range(self.rows):
            for c in range(self.cols):
                cell_value = self.level.maze[r][c]

                x_left = start_x_offset + (c * CELL_SIZE)
                x_right = x_left + CELL_SIZE
                y_top = start_y_offset - (r * CELL_SIZE)
                y_bottom = y_top - CELL_SIZE

                if cell_value & NORTH:
                    arcade.draw_line(x_left, y_top,
                                     x_right, y_top,
                                     arcade.color.BLACK, 2)
                if cell_value & EAST:
                    arcade.draw_line(x_right, y_top,
                                     x_right, y_bottom,
                                     arcade.color.BLACK, 2)
                if cell_value & SOUTH:
                    arcade.draw_line(x_left, y_bottom, x_right, y_bottom,
                                     arcade.color.BLACK, 2)
                if cell_value & WEST:
                    arcade.draw_line(x_left, y_top, x_left, y_bottom,
                                     arcade.color.BLACK, 2)

        for r, c in self.pacgums:
            x = start_x_offset + (c * CELL_SIZE) + (CELL_SIZE / 2)
            y = start_y_offset - (r * CELL_SIZE) - (CELL_SIZE / 2)
            arcade.draw_circle_filled(x, y, CELL_SIZE / 8, arcade.color.BLUE)

        for r, c in self.super_pacgums:
            x = start_x_offset + (c * CELL_SIZE) + (CELL_SIZE / 2)
            y = start_y_offset - (r * CELL_SIZE) - (CELL_SIZE / 2)
            arcade.draw_circle_filled(x, y, CELL_SIZE / 4, arcade.color.RED)

        player_x = start_x_offset + (self.player.col *
                                     CELL_SIZE) + (CELL_SIZE / 2)
        player_y = start_y_offset - (self.player.row *
                                     CELL_SIZE) - (CELL_SIZE / 2)

        player_color = arcade.color.ORANGE if (
            self.player.is_invincible) else arcade.color.YELLOW
        arcade.draw_circle_filled(
            player_x,
            player_y,
            CELL_SIZE / 3,
            player_color)

        for ghost in self.ghosts:
            ghost_x = start_x_offset + (ghost.col *
                                        CELL_SIZE) + (CELL_SIZE / 2)
            ghost_y = start_y_offset - (ghost.row *
                                        CELL_SIZE) - (CELL_SIZE / 2)

            if ghost.state == GhostState.RUNNING_AWAY:
                if ghost.is_flashing():
                    if int(ghost.scared_timer * 4) % 2 == 0:
                        display_color = arcade.color.RED
                    else:
                        display_color = arcade.color.BLUE
                else:
                    display_color = arcade.color.BLUE
            elif ghost.state == GhostState.DEAD:
                display_color = arcade.color.BLACK
            else:
                display_color = ghost.color

            arcade.draw_circle_filled(
                center_x=ghost_x,
                center_y=ghost_y,
                radius=CELL_SIZE / 2.5,
                color=display_color
            )

        self.draw_hud()

    def draw_hud(self) -> None:
        """
        Render the score, lives, and cheat mode status overlay. This
        makes it easy for a reviewer to confirm each cheat's effect
        without checking the console.
        """
        arcade.draw_text(f"Score: {self.player.score}",
                         10, self.window.height - 25,
                         arcade.color.BLACK, 16)
        arcade.draw_text(f"Lives: {self.player.lives}",
                         10, self.window.height - 45,
                         arcade.color.BLACK, 16)

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

            arcade.draw_text(status_text, 10, self.window.height - 70,
                             arcade.color.RED, 14, bold=True)

            help_text = ("F1 Invincibility | F2 Skip Level | "
                         "F3 Freeze Ghosts | F4 Extra Life | F5 Speed Boost")
            arcade.draw_text(help_text, 10, 10,
                             arcade.color.DARK_BLUE, 12)
        else:
            arcade.draw_text("Press C for Cheat Mode",
                             10, 10, arcade.color.DARK_BLUE, 12)

    def on_key_press(self, key: int, modifiers: int) -> None:
        """
        Queue the user's keyboard inputs for player movement, and
        handle cheat mode toggles.
        """
        if key in (arcade.key.UP, arcade.key.W):
            self.player.queue_direction(NORTH)
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player.queue_direction(EAST)
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.player.queue_direction(SOUTH)
        elif key in (arcade.key.LEFT, arcade.key.A):
            self.player.queue_direction(WEST)
        elif key == arcade.key.C:
            self.cheat_mode_enabled = not self.cheat_mode_enabled
            if not self.cheat_mode_enabled:
                self.player.is_invincible = False
                self. ghosts_frozen = False
                self.player.speed_boost = False
            status = "ON" if self.cheat_mode_enabled else "OFF"
            print(f"[CHEAT MODE] {status}")
        elif self.cheat_mode_enabled:
            self.handle_cheat_key(key)

    def handle_cheat_key(self, key: int) -> None:
        """
        Apply the cheat corresponding to the pressed function key.
        Only called while cheat mode is enabled.

        Args:
            key (int): The pressed key code.
        """
        if key == arcade.key.F1:
            self.player.toggle_invincibility()
            status = "ON" if self.player.is_invincible else "OFF"
            print(f"[CHEAT] Invincibility: {status}")

        elif key == arcade.key.F2:
            print("[CHEAT] Skipping level")
            self.handle_level_complete()

        elif key == arcade.key.F3:
            self.ghosts_frozen = not self.ghosts_frozen
            status = "ON" if self.ghosts_frozen else "OFF"
            print(f"[CHEAT] Ghosts frozen: {status}")

        elif key == arcade.key.F4:
            self.player.add_extra_life()
            print(f"[CHEAT] Extra life added. Lives: {self.player.lives}")

        elif key == arcade.key.F5:
            self.player.toggle_speed_boost()
            status = "ON" if self.player.speed_boost else "OFF"
            print(f"[CHEAT] Speed boost: {status}")
