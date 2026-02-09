# simple test to verify repeated forward A* runs correctly on a grid
from src.grid import Grid
from src.forward_astar import forward_astar

# Load the true grid
true_grid = Grid.from_file("data/grid_002.txt")

start = (0, 0)
goal = (4, 4)

# Run Repeated Forward A*
path = forward_astar(true_grid, start, goal)

print("Repeated Forward A* path:")
print(path)
