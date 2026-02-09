import random

def generate_dfs_grid(rows, cols, block_prob=0.3):
    # initialize the grid as fully blocked 
    # since the cells will open up as they are visited
    grid = [['#' for _ in range(cols)] for _ in range(rows)]
    # track which cells have already been visited by DFS
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    # possible movement directions (4-connected grid)
    directions = [(-1,0), (1,0), (0,-1), (0,1)]

    def in_bounds(r, c):
        # helper to check grid boundaries
        return 0 <= r < rows and 0 <= c < cols

    def dfs(start_r, start_c):
        # stack-based DFS to avoid recursion depth issues
        stack = [(start_r, start_c)]
        # marks the starting cell as visited and unblocked
        visited[start_r][start_c] = True
        grid[start_r][start_c] = '.'

        while stack:
            #looks at the current cell (top of stack)
            r, c = stack[-1]

            # collect sall unvisted neighbors
            neighbors = []
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if in_bounds(nr, nc) and not visited[nr][nc]:
                    neighbors.append((nr, nc))

            if neighbors:
                # random tie-breaking between unvisited neigbors
                nr, nc = random.choice(neighbors)
                visited[nr][nc] = True

                # deciding whether this cell is blocked or unblocked
                # if it has 30% probability then its blocked, otherwise its unblocked
                if random.random() < block_prob:
                    grid[nr][nc] = '#'
                else:
                    grid[nr][nc] = '.'
                    # only continue DFS through unblocked cells
                    stack.append((nr, nc))
            else:
                # dead end reached, agent backtracks
                stack.pop()

    # runs DFS starting from any unvisited cell
    # this makes sure the entire grid gets visited
    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                dfs(r, c)

    # this makes sure the start and goal cells are always free
    grid[0][0] = '.'
    grid[rows - 1][cols - 1] = '.'

    return grid


def save_grid(grid, filename):
    # saves the generated grid to a text file
    with open(filename, "w") as f:
        for row in grid:
            f.write("".join(row) + "\n")


if __name__ == "__main__":
    # parameters
    NUM_GRIDS = 50
    ROWS = 101
    COLS = 101

    # generates and stores all grid environments
    for i in range(NUM_GRIDS):
        grid = generate_dfs_grid(ROWS, COLS)
        filename = f"data/grid_{i+1:03d}.txt"
        save_grid(grid, filename)
        print(f"Generated {filename}")
