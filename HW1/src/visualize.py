def print_grid(grid, path=None, start=None, goal=None, show_path_coords=True, max_coords=15):
    """
    Prints the FULL grid (ex: 101x101) with a readable column ruler + legend + optional path overlay.

    Legend:
      .=free, #=blocked, *=path, A=start, T=goal
    """
    rows, cols = grid.rows, grid.cols
    path = path or []
    path_set = set(path)

    print(f"Grid size: {rows} x {cols}")
    print("Legend: .=free, #=blocked, *=path, A=start, T=goal")
    if start is not None:
        print(f"Start (A): {start}")
    if goal is not None:
        print(f"Goal  (T): {goal}")
    if path:
        print(f"Path length: {len(path)}")
    print()

    # Clean column ruler every 10 columns
    ruler = [" "] * cols
    for c in range(0, cols, 10):
        label = str(c)
        for i, ch in enumerate(label):
            if c + i < cols:
                ruler[c + i] = ch

    ticks = ["-"] * cols
    for c in range(0, cols, 10):
        ticks[c] = "|"

    print("     " + "".join(ruler))
    print("     " + "".join(ticks))

    # Each row: "r | <cells>"
    for r in range(rows):
        line = []
        for c in range(cols):
            pos = (r, c)
            ch = grid.grid[r][c]  # '.' or '#'

            if start is not None and pos == start:
                ch = "A"
            elif goal is not None and pos == goal:
                ch = "T"
            elif pos in path_set:
                ch = "*"

            line.append(ch)

        print(f"{r:3d} | " + "".join(line))

    # Optional: print path coordinate summary
    if show_path_coords and path:
        print("\nPath summary:")
        print(f"Length: {len(path)}")
        if len(path) <= 2 * max_coords:
            print(path)
        else:
            print("First coords:", path[:max_coords])
            print("Last coords: ", path[-max_coords:])


def print_grid_window(grid, path=None, start=None, goal=None, padding=3):
    """
    Prints a cropped window around the start/goal/path so it stays readable.
    """
    rows, cols = grid.rows, grid.cols
    path = path or []
    pts = []
    if start is not None:
        pts.append(start)
    if goal is not None:
        pts.append(goal)
    pts.extend(path)

    if not pts:
        r0, r1, c0, c1 = 0, min(20, rows - 1), 0, min(20, cols - 1)
    else:
        rs = [p[0] for p in pts]
        cs = [p[1] for p in pts]
        r0 = max(0, min(rs) - padding)
        r1 = min(rows - 1, max(rs) + padding)
        c0 = max(0, min(cs) - padding)
        c1 = min(cols - 1, max(cs) + padding)

    path_set = set(path)

    print(f"\nGrid window: rows {r0}-{r1}, cols {c0}-{c1}")
    print("Legend: A=start, T=goal, *=path, #=blocked, .=free\n")

    # Column indices mod 10 for readability
    header = "     " + "".join(str(c % 10) for c in range(c0, c1 + 1))
    print(header)

    for r in range(r0, r1 + 1):
        line = []
        for c in range(c0, c1 + 1):
            pos = (r, c)
            ch = grid.grid[r][c]

            if start is not None and pos == start:
                ch = "A"
            elif goal is not None and pos == goal:
                ch = "T"
            elif pos in path_set:
                ch = "*"

            line.append(ch)
        print(f"{r:3d} | " + "".join(line))


def save_path_coords(filename, path):
    """
    Saves full path coordinates, one per line, to a txt file.
    """
    if not path:
        return
    with open(filename, "w") as f:
        for r, c in path:
            f.write(f"({r},{c})\n")