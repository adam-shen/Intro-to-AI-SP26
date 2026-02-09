# basic check for A* on a small grid

from src.grid import Grid
from src.astar import astar

# load a small predefined grid
grid = Grid.from_file("data/small_grid.txt")

start = (0, 0)
goal = (4, 4)

# run standard A*
path = astar(grid, start, goal)

print("A* path on small grid:")
print(path)
