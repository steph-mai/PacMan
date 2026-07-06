from collections import deque


class Level:
    """
    Represents a game level, encapsulating the maze structure and its rules.
    """

    def __init__(self, maze_data: list[list[int]]) -> None:
        """
        Initialize the level with raw maze grid data.

        Args:
            maze_data (list[list[int]]): 2D array representing the maze walls.
        """
        self.maze: list[list[int]] = maze_data
        self.rows: int = len(maze_data)
        self.cols: int = len(maze_data[0]) if self.rows > 0 else 0

    def find_valid_spawn_position(self) -> tuple[int, int]:
        """
        Find the closest valid spawn position to the theoretical
        center of the maze.

        Returns:
            tuple[int, int]: A tuple containing the (row, col) coordinates
            of a safe cell.
        """
        center_row = self.rows // 2
        center_col = self.cols // 2

        if self.maze[center_row][center_col] != 15:
            return center_row, center_col

        queue: deque[tuple[int, int]] = deque([(center_row, center_col)])
        visited: set[tuple[int, int]] = {(center_row, center_col)}

        while queue:
            r, c = queue.popleft()

            if self.maze[r][c] != 15:
                return r, c

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols \
                        and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc))

        return center_row, center_col
