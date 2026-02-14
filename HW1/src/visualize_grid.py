import argparse
from src.grid import Grid
from src.visualize import print_grid, print_grid_window, save_path_coords

from src.forward_astar import forward_astar
from src.adaptive_astar import adaptive_forward_astar

def main():
    parser = argparse.ArgumentParser(description="Load and visualize a stored grid.")
    parser.add_argument("--id", type=int, required=True, help="Grid number 1-50")
    parser.add_argument("--full", action="store_true", help="Print full 101x101 grid")
    parser.add_argument("--window", action="store_true", help="Print a cropped window (readable)")
    parser.add_argument("--padding", type=int, default=3, help="Window padding (only for --window)")
    parser.add_argument("--algo", choices=["none", "forward", "adaptive"], default="none",
                        help="Compute a path using the chosen algorithm and overlay it")
    parser.add_argument("--savepath", action="store_true", help="Save full path coords to data/path_grid_###.txt")
    args = parser.parse_args()

    if not (1 <= args.id <= 50):
        raise ValueError("Grid id must be between 1 and 50")

    filename = f"data/grid_{args.id:03d}.txt"
    g = Grid.from_file(filename)
    print(f"Loaded {filename} ({g.rows}x{g.cols})\n")

    start = (0, 0)
    goal = (g.rows - 1, g.cols - 1)

    path = None
    if args.algo == "forward":
        path = forward_astar(g, start, goal)
    elif args.algo == "adaptive":
        path = adaptive_forward_astar(g, start, goal)

    if args.savepath and path:
        out = f"data/path_grid_{args.id:03d}.txt"
        save_path_coords(out, path)
        print(f"Saved full path coords to {out}\n")

    # Default behavior if no flags: show window (readable)
    if not args.full and not args.window:
        args.window = True

    if args.full:
        print_grid(g, path=path, start=start, goal=goal)
    if args.window:
        print_grid_window(g, path=path, start=start, goal=goal, padding=args.padding)

if __name__ == "__main__":
    main()