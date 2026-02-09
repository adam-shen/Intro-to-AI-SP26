# loads and prints a generated grid to verify file loading and visualization
from src.grid import Grid

g = Grid.from_file("data/grid_002.txt")
g.print_grid()
