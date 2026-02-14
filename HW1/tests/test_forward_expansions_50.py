import glob
from src.grid import Grid
from src.forward_astar import forward_astar_with_expansions

def main():
    files = sorted(glob.glob("data/grid_*.txt"))

    if not files:
        print("No grids found in data/ folder!")
        return

    solved = 0
    total_exp = 0

    print(f"{'File':<25} | {'Status':<10} | {'Expansions':<10}")
    print("-" * 50)

    for f in files:
        g = Grid.from_file(f)
        start = (0, 0)
        goal = (g.rows - 1, g.cols - 1)

        result = forward_astar_with_expansions(g, start, goal)

        if result[0] is None:
            expansions = result[1]
            print(f"{f:<25} | NO PATH    | {expansions}")
        else:
            path, expansions = result
            solved += 1
            total_exp += expansions
            print(f"{f:<25} | SOLVED     | {expansions}")

    print("\n" + "="*30)
    print("FINAL SUMMARY FOR FORWARD A*")
    print(f"Solved: {solved}/{len(files)}")
    if solved > 0:
        print(f"Avg expansions (solved only): {total_exp / solved:.2f}")
    print("="*30)

if __name__ == "__main__":
    main()