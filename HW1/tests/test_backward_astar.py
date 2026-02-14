# simple test to verify repeated backward A* runs correctly on a grid
from src.grid import Grid
from src.backward_astar import backward_astar

true_grid = Grid.from_file("data/grid_002.txt")

start = (0, 0)
goal = (4, 4)

path = backward_astar(true_grid, start, goal)

print("Repeated Backward A* path:")
print(path)