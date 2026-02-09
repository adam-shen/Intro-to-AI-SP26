import glob
from src.grid import Grid
from src.adaptive_astar import adaptive_forward_astar

def main():
    files = sorted(glob.glob("data/grid_*.txt"))
    if not files:
        print("No files matching data/grid_*.txt found.")
        return

    solved = 0
    total_len = 0

    for f in files:
        g = Grid.from_file(f)
        start = (0, 0)
        goal = (g.rows - 1, g.cols - 1)

        path = adaptive_forward_astar(g, start, goal)

        if path is None:
            print(f"{f}: NO PATH")
        else:
            solved += 1
            total_len += len(path)
            print(f"{f}: SOLVED  len={len(path)}")

    print("\nSummary")
    print(f"Solved: {solved}/{len(files)}")
    if solved > 0:
        print(f"Avg path length (solved only): {total_len / solved:.2f}")

if __name__ == "__main__":
    main()