import arcade

CELL_SIZE = 32

NORTH = 1  # 0001
EAST = 2   # 0010
SOUTH = 4  # 0100
WEST = 8   # 1000


class GameView(arcade.View):

    def __init__(self, maze: list[list[int]]) -> None:
        super().__init__()
        self.maze = maze
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.clear()

        rows = len(self.maze)
        cols = len(self.maze[0]) if rows > 0 else 0

        for r in range(rows):
            for c in range(cols):
                cell_value = self.maze[r][c]

                x_left = ((self.window.width
                           - (rows * CELL_SIZE)) / 2) + (c * CELL_SIZE)
                x_right = x_left + CELL_SIZE
                y_top = ((self.window.height
                          + (cols * CELL_SIZE)) / 2) - (r * CELL_SIZE)
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
                    arcade.draw_line(x_left, y_bottom,
                                     x_right, y_bottom,
                                     arcade.color.BLACK, 2)

                if cell_value & WEST:
                    arcade.draw_line(x_left, y_top,
                                     x_left, y_bottom,
                                     arcade.color.BLACK, 2)

        return super().on_draw()
