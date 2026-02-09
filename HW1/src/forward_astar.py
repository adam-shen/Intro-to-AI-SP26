# this implements repeated forward A*
# the agent plans while assuming unknown cells are free
# and then it replans whenever it discovers a blocked cell.

from src.grid import Grid
from src.astar import astar

def create_agent_grid(true_grid):
    # the agent starts with no knowledge of blocked cells
    rows = true_grid.rows
    cols = true_grid.cols

    grid = [['.' for _ in range(cols)] for _ in range(rows)]
    return Grid(grid)

def observe_and_update(agent_grid, true_grid, current):
    # it observes neighbors of the current cell 
    # if any cells are blocked in the true grid, it updates the agent's map
    for neighbor in true_grid.neighbors(current):
        r, c = neighbor
        if true_grid.is_blocked(neighbor):
            agent_grid.grid[r][c] = '#'

def forward_astar(true_grid, start, goal):
    agent_grid = create_agent_grid(true_grid)

    current = start
    full_path = [current]

    # it keeps replanning until it reaches the goal
    while current != goal:
        path = astar(agent_grid, current, goal)

        # if it finds no path with its current knowledge 
        if path is None:
            return None

        replanned = False

        # follows the planned path step by step
        for next_cell in path[1:]:
            # if it hits a blocked cell in the real grid, it replans
            if true_grid.is_blocked(next_cell):
                r, c = next_cell
                agent_grid.grid[r][c] = '#'
                replanned = True
                break

            current = next_cell
            full_path.append(current)

            # updates the agents knowledge after it moves 
            observe_and_update(agent_grid, true_grid, current)

            if current == goal:
                return full_path

        if replanned:
            continue

    return full_path
