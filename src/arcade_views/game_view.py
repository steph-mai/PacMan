import arcade
import random
from ..obj.player import Player, NORTH, EAST, SOUTH, WEST
from ..obj.level import Level

CELL_SIZE = 32


class GameView(arcade.View):
    """
    The main gameplay view displaying the maze and handling player actions.
    """

    def __init__(self, level: Level) -> None:
        """
        Initialize the game view, maze data, and player object.
        """
        super().__init__()
        self.level = level
        arcade.set_background_color(arcade.color.WHITE)

        self.rows = self.level.rows
        self.cols = self.level.cols

        start_row, start_col = self.level.find_valid_spawn_position()

        self.player = Player(start_row, start_col)

        self.pacgums: set[tuple[int, int]] = set()
        self.super_pacgums: set[tuple[int, int]] = set()

        # Placeholder waiting for actual config logic
        pacgums_from_config = 400000
        self.setup_collectibles(pacgums_from_config)

    def setup_collectibles(self, config_pacgum_count: int = 42) -> None:
        """
        Populate the maze with pacgums and place super-pacgums
        in the 4 corners.
        """
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

    def on_update(self, delta_time: float) -> None:
        """
        Update game logic: handle collectible consumption and game rules.

        Args:
            delta_time (float): Time elapsed since the last frame.
        """
        current_pos = (self.player.row, self.player.col)

        if current_pos in self.pacgums:
            self.pacgums.remove(current_pos)
            self.player.add_score(10)  # Value can later be set from conf.json

        if current_pos in self.super_pacgums:
            self.super_pacgums.remove(current_pos)
            self.player.add_score(50)  # Value can later be set from conf.json
            # TODO: Make ghosts edible here

        # Placeholder for Ghost Collision
        # if self.check_ghost_collision():
        #     is_dead = self.player.lose_life()
        #     if is_dead:
        #         print("Game Over!")
        #         # Trigger Game Over View

    def on_draw(self) -> None:
        """
        Render the maze walls and the player object.
        """
        self.clear()

        start_x_offset = ((self.window.width - (self.rows * CELL_SIZE)) / 2)
        start_y_offset = ((self.window.height + (self.cols * CELL_SIZE)) / 2)

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

        self.player.draw(start_x_offset, start_y_offset, CELL_SIZE)

    def on_key_press(self, key: int, modifiers: int) -> None:
        """
        Handle keyboard inputs to trigger player movement.
        """
        if key in (arcade.key.UP, arcade.key.W):
            self.player.move(NORTH, self.level.maze)
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player.move(EAST, self.level.maze)
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.player.move(SOUTH, self.level.maze)
        elif key in (arcade.key.LEFT, arcade.key.A):
            self.player.move(WEST, self.level.maze)
