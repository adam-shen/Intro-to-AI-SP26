from src.grid import Grid
from src.astar import astar

def create_agent_grid(true_grid):
    rows = true_grid.rows
    cols = true_grid.cols
    grid = [['.' for _ in range(cols)] for _ in range(rows)]
    return Grid(grid)

def observe_and_update(agent_grid, true_grid, current):
    # observes neighbors of the current cell 
    # if any cells are blocked in the true grid, updates the agent's map
    for neighbor in true_grid.neighbors(current):
        r, c = neighbor
        if true_grid.is_blocked(neighbor):
            agent_grid.grid[r][c] = '#'

def backward_astar(true_grid, start, goal):
    agent_grid = create_agent_grid(true_grid)

    current = start
    full_path = [current]
    
    # Observe the initial surroundings before the first move
    observe_and_update(agent_grid, true_grid, current)

    # keeps replanning until it reaches the goal
    while current != goal:
        path = astar(agent_grid, goal, current)

        # if it finds no path with its current knowledge
        if path is None:
            return None 

        # We reverse it so the agent can walk it
        path.reverse()

        replanned = False
        for next_cell in path[1:]:
          
            if true_grid.is_blocked(next_cell):
                r, c = next_cell
                agent_grid.grid[r][c] = '#'
                replanned = True
                break
            current = next_cell
            full_path.append(current)

            observe_and_update(agent_grid, true_grid, current)

            if current == goal:
                return full_path
        
        if replanned:
            continue

    return full_path