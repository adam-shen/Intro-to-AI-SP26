# test_adaptive_astar.py
from src.grid import Grid
from src.adaptive_astar import adaptive_forward_astar
from src.visualize import print_grid_window  

true_grid = Grid.from_file("data/grid_002.txt")

start = (0, 0)
goal = (4, 4)

path = adaptive_forward_astar(true_grid, start, goal)

print("Repeated Adaptive A* path:")
print(path)
print("Path length:", None if path is None else len(path))

# visualize in terminal
print("\nGrid window with path:")
print_grid_window(true_grid, path=path, start=start, goal=goal, padding=2)