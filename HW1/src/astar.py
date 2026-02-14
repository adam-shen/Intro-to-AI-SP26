# A* search implementation for grid worlds
# supports tie-breaking on g-values and optional expansion counting

import heapq

def manhattan(a, b):
    # manhattan distance heuristic
    # since the movement is 4-connected, this works well and is admissible
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, goal, tie_break="larger_g", return_expansions=False):
    # runs A* on a given grid from start to goal 
    # tie_break is either larger_g (which prefers nodes with larger g-values when f is equal)
    # or its smaller_g (which prefers nodes with smaller g-values when f is equal)
    # if true, return_expansions also returns the number of node expansions
    
    # priority queue stores (f, tie-break value, cell)
    open_list = []
    if tie_break == "larger_g":
        # initial state: g = 0, f = heuristic(start)
        heapq.heappush(open_list, (0, 0, start))
    else:
        heapq.heappush(open_list, (0, 0, start))

    # used to reconstruct the final path
    came_from = {}
    # tracks the best known cost from start to each node
    g_score = {start: 0}
    # closed set to avoid re-expanding nodes
    closed_set = set()

    # counter for how many nodes are expanded
    expansions = 0

    while open_list:
        # pops the node with lowest f-score (and tie-break)
        current_f, _, current = heapq.heappop(open_list)
        expansions += 1

        # when the goal is reached, the path is reconstructed
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            if return_expansions:
                return path, expansions
            return path

        # skip if already processed
        if current in closed_set:
            continue

        closed_set.add(current)

        # explore neighbors (up, down, left, right)
        for neighbor in grid.neighbors(current):
            if neighbor in closed_set:
                continue
            
            # cost of moving to a neighbor is always 1
            tentative_g = g_score[current] + 1

            # if this is a better path, it updates the records
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                # f = g + h
                f_score = tentative_g + manhattan(neighbor, goal)

                # pushes into open list with appropriate tie-breaking
                if tie_break == "larger_g":
                    # uses negative g so larger g gets priority when f ties
                    heapq.heappush(open_list, (f_score, -tentative_g, neighbor))
                else:
                    heapq.heappush(open_list, (f_score, tentative_g, neighbor))
    # no path found
    if return_expansions:
        return None, expansions
    return None

