# this test measures node expansions for Forward A* across 50 grids to 
# baseline its efficiency against Adaptive A*.
import glob
from src.grid import Grid
from src.adaptive_astar import adaptive_forward_astar_with_expansions

def main():
    files = sorted(glob.glob("data/grid_*.txt"))

    solved = 0
    total_exp = 0

    for f in files:
        g = Grid.from_file(f)
        start = (0, 0)
        goal = (g.rows - 1, g.cols - 1)

        path, expansions = adaptive_forward_astar_with_expansions(g, start, goal)

        if path is None:
            print(f"{f}: NO PATH  expansions={expansions}")
        else:
            solved += 1
            total_exp += expansions
            print(f"{f}: SOLVED  len={len(path)}  expansions={expansions}")

    print("\nSummary")
    print(f"Solved: {solved}/{len(files)}")
    if solved > 0:
        print(f"Avg expansions (solved only): {total_exp / solved:.2f}")

if __name__ == "__main__":
    main()