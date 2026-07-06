import arcade
from ..obj.player import Player, NORTH, EAST, SOUTH, WEST
from src.parsing.models import Config
from mazegenerator import MazeGenerator

CELL_SIZE = 32


class GameView(arcade.View):
    """
    The main gameplay view displaying the maze and handling player actions.
    """

    def __init__(self, config: Config) -> None:
        """
        Initialize the game view, maze data, and player object.
        """
        super().__init__()
        self.config = config
        arcade.set_background_color(arcade.color.WHITE)

        level_config = self.config.level[0]
        level_width = level_config.width
        level_height = level_config.height

        mazegen = MazeGenerator(
            size=(level_width, level_height), perfect=False)
        self.maze = mazegen.maze
        # pas de () après  mazegen.maze car @property dans mazegenerator.py
        # permet d'utiliser une méthode comme une simple variable

        self.cols = level_width
        self.rows = level_height
        start_col = self.cols // 2
        start_row = self.rows // 2
        self.player = Player(start_row, start_col, self.config)

    def on_draw(self) -> None:
        """
        Render the maze walls and the player object.
        """
        self.clear()

        start_x_offset = ((self.window.width - (self.cols * CELL_SIZE)) / 2)
        start_y_offset = ((self.window.height + (self.rows * CELL_SIZE)) / 2)


        for r in range(self.rows):
            for c in range(self.cols):
                cell_value = self.maze[r][c]

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

        self.player.draw(start_x_offset, start_y_offset, CELL_SIZE)

    def on_key_press(self, key: int, modifiers: int) -> None:
        """
        Handle keyboard inputs to trigger player movement.
        """
        if key in (arcade.key.UP, arcade.key.W):
            self.player.move(NORTH, self.maze)
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player.move(EAST, self.maze)
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.player.move(SOUTH, self.maze)
        elif key in (arcade.key.LEFT, arcade.key.A):
            self.player.move(WEST, self.maze)
