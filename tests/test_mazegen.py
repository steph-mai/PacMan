from mazegenerator import MazeGenerator


def test_maze_dimensions() -> None:
    """Checks that the requested dimensions are respected."""
    maze_gen = MazeGenerator(size=(20, 20), perfect=False)
    maze_grid = maze_gen.maze

    assert len(maze_grid) == 20, "The maze height should be 20"
    assert len(maze_grid[0]) == 20, "The maze width should be 20"


def test_maze_pathfinding() -> None:
    """Checks that an entry, an exit, and a valid path actually exist."""
    maze_gen = MazeGenerator(size=(20, 20), perfect=False)

    assert maze_gen.maze_entry is not None, "The maze must have an entry"
    assert maze_gen.maze_exit is not None, "The maze must have an exit"
    assert len(str(maze_gen.shortest_path)) > 0, "A valid path must exist"


def test_maze_grid_data() -> None:
    """Checks that the grid contains valid data (integers)."""
    maze_gen = MazeGenerator(size=(20, 20), perfect=False)

    for i in range(10):
        cell_value = maze_gen.maze[1][i]
        assert isinstance(
            cell_value, int), f"The cell at [1][{i}] is not an integer"
