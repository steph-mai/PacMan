import sys
import arcade
import random
import logging
from src.parsing.models import Config
from src.obj.player import Player, NORTH, EAST, SOUTH, WEST
from src.obj.level import Level
from mazegenerator import MazeGenerator

logger = logging.getLogger("pacman")
CELL_SIZE = 32


class GameView(arcade.View):
    def __init__(self, config: Config, level_index: int = 0) -> None:
        super().__init__()
        self.config = config
        self.level_index = level_index
        arcade.set_background_color(arcade.color.WHITE)

        safe_index = min(self.level_index, len(self.config.level) - 1)
        level_config = self.config.level[safe_index]
        level_width = level_config.width
        level_height = level_config.height

        current_seed = self.config.seed if self.level_index == 0 else 0

        try:
            mazegen = MazeGenerator(
                size=(level_width, level_height),
                perfect=False,
                seed=current_seed
            )
            self.level = Level(mazegen.maze)

        except Exception as e:
            logger.error(f"External MazeGenerator crashed: {e}")
            logger.error("Failed to load the level. Exiting game gracefully.")
            sys.exit(1)

        self.maze = self.level.maze
        self.cols = self.level.cols
        self.rows = self.level.rows

        start_row, start_col = self.level.find_valid_spawn_position()
        self.player = Player(start_row, start_col, self.config)

        self.pacgums: set[tuple[int, int]] = set()
        self.super_pacgums: set[tuple[int, int]] = set()

        self.setup_collectibles()

import sys
import arcade
import random
import logging
from enum import Enum
from src.parsing.models import Config
from src.obj.player import Player, NORTH, EAST, SOUTH, WEST
from src.obj.level import Level
from mazegenerator import MazeGenerator

logger = logging.getLogger("pacman")
CELL_SIZE = 32

class GameState(Enum):
    PLAYING = 1
    PAUSED = 2
    LEVEL_COMPLETE = 3
    GAME_OVER = 4
    VICTORY = 5

class GameView(arcade.View):
    """
    The main gameplay view displaying the maze and handling player actions.
    """

    def __init__(self, config: Config, level_index: int = 0, carried_score: int = 0, carried_lives: int = -1) -> None:
        """
        Initialize the game view, maze data, and player object.
        """
        super().__init__()
        self.config = config
        self.level_index = level_index
        self.state = GameState.PLAYING

        # Timer setup
        self.time_left = float(self.config.level_max_time)

        arcade.set_background_color(arcade.color.WHITE)

        # 1. Load specific level configuration safely
        safe_index = min(self.level_index, len(self.config.level) - 1)
        level_config = self.config.level[safe_index]

        # 2. Generator Seed Logic
        current_seed = self.config.seed if self.level_index == 0 else 0

        # 3. Safe Maze Generation
        try:
            mazegen = MazeGenerator(
                size=(level_config.width, level_config.height),
                perfect=False,
                seed=current_seed
            )
            self.level = Level(mazegen.maze)
        except Exception as e:
            logger.error(f"External MazeGenerator crashed: {e}")
            logger.error("Failed to load the level. Exiting game gracefully.")
            sys.exit(1)

        self.maze = self.level.maze
        self.cols = self.level.cols
        self.rows = self.level.rows

        # 4. Player Setup (Inheriting stats if progressing)
        start_row, start_col = self.level.find_valid_spawn_position()
        self.player = Player(start_row, start_col, self.config)

        # Override config defaults if carrying over from a previous level
        if carried_lives != -1:
            self.player.lives = carried_lives
        self.player.score = carried_score

        self.pacgums: set[tuple[int, int]] = set()
        self.super_pacgums: set[tuple[int, int]] = set()

        self.setup_collectibles()

    def setup_collectibles(self) -> None:
        """
        Populate the maze with pacgums and place super-pacgums.
        """
        target_pacgum_count = self.config.pacgum

        theoretical_corners = [
            (0, 0),
            (0, self.cols - 1),
            (self.rows - 1, 0),
            (self.rows - 1, self.cols - 1)
        ]

        valid_corners = []

        for r, c in theoretical_corners:
            if self.level.maze[r][c] != 15:
                self.super_pacgums.add((r, c))
                valid_corners.append((r, c))
            else:
                logger.warning(f"Corner at ({r}, {c}) is a solid wall. Super Pacgum skipped.")

        available_cells: list[tuple[int, int]] = []

        for r in range(self.rows):
            for c in range(self.cols):
                is_corner = (r, c) in valid_corners
                is_player_start = (r, c) == (self.player.row, self.player.col)
                is_solid_wall = self.level.maze[r][c] == 15

                if not is_corner and not is_player_start and not is_solid_wall:
                    available_cells.append((r, c))

        actual_pacgum_count = min(target_pacgum_count, int(len(available_cells) * 0.80))
        selected_cells = random.sample(available_cells, actual_pacgum_count)

        for r, c in selected_cells:
            self.pacgums.add((r, c))

    def on_update(self, delta_time: float) -> None:
        """
        Core game logic loop. Runs ~60 times per second.
        """
        if self.state != GameState.PLAYING:
            return

        # 1. Timer Logic
        self.time_left -= delta_time
        if self.time_left <= 0:
            self.time_left = 0
            self.handle_timeout()

        # 2. Check for Level Completion
        # Level ends when all standard pacgums are eaten
        if len(self.pacgums) == 0:
            self.handle_level_complete()

    def handle_timeout(self) -> None:
        """
        Called when the level timer reaches 0.
        Treats timeout as losing a life.
        """
        logger.info("Time's up! Player lost a life.")
        is_dead = self.player.lose_life()
        if is_dead:
            self.state = GameState.GAME_OVER
        else:
            # Reset timer and player position, but keep the eaten pacgums
            self.time_left = float(self.config.level_max_time)

    def handle_level_complete(self) -> None:
        """
        Handles transition to the next level or victory.
        """
        logger.info(f"Level {self.level_index + 1} complete!")

        # Check if this was the last level (subject says at least 10)
        # We assume 10 levels minimum, but bounded by config length
        total_levels_to_win = max(10, len(self.config.level))

        if self.level_index + 1 >= total_levels_to_win:
            self.state = GameState.VICTORY
        else:
            self.state = GameState.LEVEL_COMPLETE

    def on_draw(self) -> None:
        """
        Render the maze, player, HUD, and overlay screens.
        """
        self.clear()

        start_x_offset = ((self.window.width - (self.cols * CELL_SIZE)) / 2)
        start_y_offset = ((self.window.height + (self.rows * CELL_SIZE)) / 2)

        # Draw Maze
        for r in range(self.rows):
            for c in range(self.cols):
                cell_value = self.maze[r][c]

                x_left = start_x_offset + (c * CELL_SIZE)
                x_right = x_left + CELL_SIZE
                y_top = start_y_offset - (r * CELL_SIZE)
                y_bottom = y_top - CELL_SIZE

                if cell_value & NORTH:
                    arcade.draw_line(x_left, y_top, x_right, y_top, arcade.color.BLACK, 2)
                if cell_value & EAST:
                    arcade.draw_line(x_right, y_top, x_right, y_bottom, arcade.color.BLACK, 2)
                if cell_value & SOUTH:
                    arcade.draw_line(x_left, y_bottom, x_right, y_bottom, arcade.color.BLACK, 2)
                if cell_value & WEST:
                    arcade.draw_line(x_left, y_top, x_left, y_bottom, arcade.color.BLACK, 2)

        # Draw Player
        self.player.draw(start_x_offset, start_y_offset, CELL_SIZE)

        # Draw HUD
        self.draw_hud()

        # Draw Overlays based on State
        if self.state == GameState.PAUSED:
            self.draw_overlay("PAUSED", "Press ESC to Resume or Q to Quit")
        elif self.state == GameState.LEVEL_COMPLETE:
            self.draw_overlay("LEVEL CLEARED!", "Press ENTER for Next Level")
        elif self.state == GameState.GAME_OVER:
            self.draw_overlay("GAME OVER", f"Final Score: {self.player.score}\nPress ENTER to Save Score")
        elif self.state == GameState.VICTORY:
            self.draw_overlay("VICTORY!", f"Final Score: {self.player.score}\nPress ENTER to Save Score")

    def draw_hud(self) -> None:
        """Draws the Heads Up Display with stats."""
        hud_text = f"Level: {self.level_index + 1}   Score: {self.player.score}   Lives: {self.player.lives}   Time: {int(self.time_left)}s"
        arcade.draw_text(hud_text, 10, self.window.height - 25, arcade.color.BLACK, 16, bold=True)

    def draw_overlay(self, title: str, subtitle: str) -> None:
        """Draws a semi-transparent overlay with text."""
        arcade.draw_rect_filled(self.window.width / 2, self.window.height / 2, self.window.width, self.window.height, (255, 255, 255, 200))
        arcade.draw_text(title, self.window.width / 2, self.window.height / 2 + 20, arcade.color.BLACK, 36, anchor_x="center", anchor_y="center", bold=True)
        arcade.draw_text(subtitle, self.window.width / 2, self.window.height / 2 - 30, arcade.color.DARK_GRAY, 18, anchor_x="center", anchor_y="center", multiline=True, width=400, align="center")

    def on_key_press(self, key: int, modifiers: int) -> None:
        """
        Handle keyboard inputs based on the current game state.
        """
        # State: PAUSED
        if self.state == GameState.PAUSED:
            if key == arcade.key.ESCAPE:
                self.state = GameState.PLAYING
            elif key == arcade.key.Q:
                # Need to import MenuView locally to avoid circular import issues
                from src.ui.menus import MenuView
                self.window.show_view(MenuView(self.config))
            return

        # State: PLAYING (Pause toggle)
        if self.state == GameState.PLAYING and key == arcade.key.ESCAPE:
            self.state = GameState.PAUSED
            return

        # State: LEVEL COMPLETE (Transition)
        if self.state == GameState.LEVEL_COMPLETE and key == arcade.key.ENTER:
            next_level_view = GameView(
                config=self.config,
                level_index=self.level_index + 1,
                carried_score=self.player.score,
                carried_lives=self.player.lives
            )
            self.window.show_view(next_level_view)
            return

        # State: GAME OVER / VICTORY (Transition to Highscore Input)
        if self.state in (GameState.GAME_OVER, GameState.VICTORY) and key == arcade.key.ENTER:
            # TODO: Transition to HighScoreInputView instead of Menu immediately
            from src.ui.menus import MenuView
            self.window.show_view(MenuView(self.config))
            return

        # Movement Inputs (Only when PLAYING)
        if self.state == GameState.PLAYING:
            if key in (arcade.key.UP, arcade.key.W):
                self.player.move(NORTH, self.maze)
            elif key in (arcade.key.RIGHT, arcade.key.D):
                self.player.move(EAST, self.maze)
            elif key in (arcade.key.DOWN, arcade.key.S):
                self.player.move(SOUTH, self.maze)
            elif key in (arcade.key.LEFT, arcade.key.A):
                self.player.move(WEST, self.maze)
