# implements repeated Adaptive A*
# idea: run A* forward many times, and after each search update h-values:
# h(s) = g(goal) - g(s) for states that were expanded (in CLOSED)

import heapq
from src.grid import Grid
from src.astar import manhattan

INF = 10**18


def create_agent_grid(true_grid):
    rows = true_grid.rows
    cols = true_grid.cols
    grid = [['.' for _ in range(cols)] for _ in range(rows)]
    return Grid(grid)


def observe_and_update(agent_grid, true_grid, current):
    # observes the 4-neighbors of current and updates agent's map
    for neighbor in true_grid.neighbors(current):
        r, c = neighbor
        if true_grid.is_blocked(neighbor):
            agent_grid.grid[r][c] = '#'


def adaptive_astar_search(agent_grid, start, goal, h_table, tie_break="larger_g", return_expansions=False):
    """
    A* search but with an adaptive heuristic table.
    If a cell has an entry in h_table, we use that as its h-value.
    Otherwise, use Manhattan.
    Returns:
      - path (list of cells) or None
      - optionally: expansions, closed_list, g_score, g_goal
    """

    def h(cell):
        if cell in h_table:
            return h_table[cell]
        return manhattan(cell, goal)

    open_list = []
    came_from = {}
    g_score = {start: 0}
    closed_set = set()
    closed_list = []
    expansions = 0

    # push start (priority = f then tie-break on g)
    g0 = 0
    f0 = g0 + h(start)
    if tie_break == "larger_g":
        heapq.heappush(open_list, (f0, -g0, start))
    else:
        heapq.heappush(open_list, (f0, g0, start))

    while open_list:
        _, _, current = heapq.heappop(open_list)

        if current in closed_set:
            continue

        # expand current
        closed_set.add(current)
        closed_list.append(current)
        expansions += 1

        if current == goal:
            # reconstruct path
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()

            g_goal = g_score[goal]
            if return_expansions:
                return path, expansions, closed_list, g_score, g_goal
            return path, closed_list, g_score, g_goal

        for neighbor in agent_grid.neighbors(current):
            if neighbor in closed_set:
                continue

            tentative_g = g_score[current] + 1

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + h(neighbor)

                if tie_break == "larger_g":
                    heapq.heappush(open_list, (f_score, -tentative_g, neighbor))
                else:
                    heapq.heappush(open_list, (f_score, tentative_g, neighbor))

    # no path
    if return_expansions:
        return None, expansions, closed_list, g_score, INF
    return None, closed_list, g_score, INF


def adaptive_forward_astar(true_grid, start, goal, tie_break="larger_g", return_expansions=False):
    """
    Repeated Adaptive A* (forward):
      - plan using adaptive A*
      - walk the path in the true grid
      - when you hit a blocked cell, mark it and replan
      - after each search, update h-values of expanded states:
           h(s) = g(goal) - g(s)
    """
    agent_grid = create_agent_grid(true_grid)

    current = start
    full_path = [current]

    # stores improved h-values for some cells
    h_table = {}

    total_expansions = 0

    # optional: update from the very start
    observe_and_update(agent_grid, true_grid, current)

    while current != goal:
        # run adaptive A* search (not using src/astar.py so we can use h_table)
        if return_expansions:
            path, expansions, closed_list, g_score, g_goal = adaptive_astar_search(
                agent_grid, current, goal, h_table, tie_break=tie_break, return_expansions=True
            )
            total_expansions += expansions
        else:
            path, closed_list, g_score, g_goal = adaptive_astar_search(
                agent_grid, current, goal, h_table, tie_break=tie_break, return_expansions=False
            )

        if path is None:
            if return_expansions:
                return None, total_expansions
            return None

        # --- Adaptive heuristic update step ---
        # update only expanded states from this search (closed_list)
        # h(s) = g(goal) - g(s)
        if g_goal < INF:
            for s in closed_list:
                if s in g_score:
                    new_h = g_goal - g_score[s]
                    # keep it non-decreasing to be safe
                    if s not in h_table or new_h > h_table[s]:
                        h_table[s] = new_h

        replanned = False

        # follow planned path
        for next_cell in path[1:]:
            if true_grid.is_blocked(next_cell):
                # discovered a blocked cell in the real world
                r, c = next_cell
                agent_grid.grid[r][c] = '#'
                replanned = True
                break

            current = next_cell
            full_path.append(current)

            observe_and_update(agent_grid, true_grid, current)

            if current == goal:
                if return_expansions:
                    return full_path, total_expansions
                return full_path

        if replanned:
            continue

    if return_expansions:
        return full_path, total_expansions
    return full_path

def adaptive_forward_astar_with_expansions(true_grid, start, goal, tie_break="larger_g"):
    agent_grid = create_agent_grid(true_grid)
    current = start
    full_path = [current]
    h_table = {}

    total_expansions = 0

    while current != goal:
        path, closed_list, g_score, g_goal = adaptive_astar_search(
            agent_grid, current, goal, h_table, tie_break=tie_break
        )

        total_expansions += len(closed_list)

        if path is None:
            return None, total_expansions

        # update h-table
        if g_goal < INF:
            for s in closed_list:
                if s in g_score:
                    new_h = g_goal - g_score[s]
                    if s not in h_table or new_h > h_table[s]:
                        h_table[s] = new_h

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
                return full_path, total_expansions

        if replanned:
            continue

    return full_path, total_expansions