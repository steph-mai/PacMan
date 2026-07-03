# test running with:
# uv run tests/test_mazegen.py

from mazegenerator import MazeGenerator

# Create a simple 20x20 maze
maze_gen = MazeGenerator(size=(20, 20), perfect=False)

# Get the maze structure
maze_grid = maze_gen.maze
shortest_path = maze_gen.shortest_path

print(f"Maze dimensions: {len(maze_grid[0])}x{len(maze_grid)}")
print(f"Entry: {maze_gen.maze_entry}, Exit: {maze_gen.maze_exit}")
print(f"Shortest path length: {len(shortest_path)}\n\n")
print(len(maze_gen.maze))
print("\n\n")
print(len(maze_gen.maze[1]))
print("\n\n")
print(maze_gen.maze[1][0])
print("\n\n")
print(maze_gen.maze[1][1])
print("\n\n")
print(maze_gen.maze[1][2])
print("\n\n")
print(maze_gen.maze[1][3])
print("\n\n")
print(maze_gen.maze[1][4])
print("\n\n")
print(maze_gen.maze[1][5])
print("\n\n")
print(maze_gen.maze[1][6])
print("\n\n")
print(maze_gen.maze[1][7])
print("\n\n")
print(maze_gen.maze[1][8])
print("\n\n")
print(maze_gen.maze[1][9])
