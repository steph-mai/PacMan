import arcade
import random
import logging
import sys
from src.obj.player import Player
from src.obj.entity import NORTH, EAST, SOUTH, WEST
from src.obj.level import Level
from src.obj.ghost import Ghost
from src.ai.personalities import GhostPersonality
from src.ai.states import GhostState
from src.parsing.models import Config
from mazegenerator import MazeGenerator

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

        actual_pacgum_count = min(config_pacgum_count,
                                  int(len(available_cells) * 0.80))

        selected_cells = random.sample(available_cells, actual_pacgum_count)

        for r, c in selected_cells:
            self.pacgums.add((r, c))

    def setup_ghosts(self) -> None:
        ghosts_data = [
            # (1, 0, arcade.color.RED, GhostPersonality.SHADOW),
            # (1, self.cols - 1, arcade.color.CYAN, GhostPersonality.BASHFUL),
            # (self.rows - 2, 0, arcade.color.PINK, GhostPersonality.SPEEDY),
            # (self.rows - 2, self.cols - 1,
            #  arcade.color.ORANGE, GhostPersonality.POKEY)
            (1, 0, arcade.color.RED, GhostPersonality.RANDOM),
            (1, self.cols - 1, arcade.color.CYAN, GhostPersonality.RANDOM),
            (self.rows - 2, 0, arcade.color.PINK, GhostPersonality.RANDOM),
            (self.rows - 2, self.cols - 1,
             arcade.color.ORANGE, GhostPersonality.RANDOM)
        ]

        for r, c, color, personality in ghosts_data:
            ghost = Ghost(start_row=r,
                          start_col=c,
                          color=color,
                          max_rows=self.rows,
                          max_cols=self.cols,
                          personality=personality)
            self.ghosts.append(ghost)

    def on_update(self, delta_time: float) -> None:
        """
        Update game logic: handle collectible consumption and game rules.

        Args:
            delta_time (float): Time elapsed since the last frame.
        """
        self.player.update_movement(delta_time, self.level.maze)

        for ghost in self.ghosts:
            ghost.update_movement(
                delta_time, self.level.maze, self.player.row, self.player.col)

        current_pos = (self.player.row, self.player.col)

        if current_pos in self.pacgums:
            self.pacgums.remove(current_pos)
            self.player.add_score(self.config.points_per_pacgum)

        if current_pos in self.super_pacgums:
            self.super_pacgums.remove(current_pos)
            self.player.add_score(self.config.points_per_super_pacgum)
            # TODO: Make ghosts edible here

        if not self.pacgums and not self.super_pacgums:
            self.handle_level_complete()

        # Placeholder for Ghost Collision
        # if self.check_ghost_collision():
        #     is_dead = self.player.lose_life()
        #     if is_dead:
        #         print("Game Over!")
        #         # Trigger Game Over View

    def handle_level_complete(self) -> None:
        """
        Process level completion. Transitions to the next level if available,
        or prints victory if the game is finished.
        """
        if self.level_index + 1 < len(self.config.level):
            # Pass the existing player object to the next Level View
            next_view = GameView(self.config,
                                 self.level_index + 1,
                                 player=self.player)
            self.window.show_view(next_view)
        else:
            # Game Completed
            print(f"Game Won! Final Score: {self.player.score}")
            # self.window.show_view(VictoryView(self.player.score))

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

        player_x = start_x_offset + (self.player.col * CELL_SIZE) + (CELL_SIZE / 2)
        player_y = start_y_offset - (self.player.row * CELL_SIZE) - (CELL_SIZE / 2)

        player_color = arcade.color.ORANGE if (
            self.player.is_invincible) else arcade.color.YELLOW
        arcade.draw_circle_filled(
            player_x,
            player_y,
            CELL_SIZE / 3,
            player_color)

        for ghost in self.ghosts:
            ghost_x = start_x_offset + (ghost.col * CELL_SIZE) + (CELL_SIZE / 2)
            ghost_y = start_y_offset - (ghost.row * CELL_SIZE) - (CELL_SIZE / 2)

            if ghost.state == GhostState.RUNNING_AWAY:
                display_color = arcade.color.BLUE
            elif ghost.state == GhostState.DEAD:
                display_color = arcade.color.WHITE
            else:
                display_color = ghost.color

            arcade.draw_circle_filled(
                center_x=ghost_x,
                center_y=ghost_y,
                radius=CELL_SIZE / 2.5,
                color=display_color
            )

    def on_key_press(self, key: int, modifiers: int) -> None:
        """
        Queue the user's keyboard inputs for player movement.
        """
        if key in (arcade.key.UP, arcade.key.W):
            self.player.queue_direction(NORTH)
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player.queue_direction(EAST)
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.player.queue_direction(SOUTH)
        elif key in (arcade.key.LEFT, arcade.key.A):
            self.player.queue_direction(WEST)
