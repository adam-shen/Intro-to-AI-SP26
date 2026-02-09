# tests A* tie-breaking behavior and compares node expansion counts
from src.grid import Grid
from src.astar import astar

grid = Grid.from_file("data/grid_002.txt")

start = (0, 0)
goal = (4, 4)

path1, exp1 = astar(grid, start, goal, tie_break="larger_g", return_expansions=True)
path2, exp2 = astar(grid, start, goal, tie_break="smaller_g", return_expansions=True)

print("Larger g path:", path1)
print("Larger g expansions:", exp1)

print("Smaller g path:", path2)
print("Smaller g expansions:", exp2)
