# represents the grid world
# handles bounds checking, blocked cells, and valid neighbors

class Grid:
    def __init__(self, grid):
        # the grid is a 2D list of characters
        # the '.' represents a free cell
        # the '#' represents a blocked cell
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

    @staticmethod
    def from_file(filename):
        # loads a grid from a text file
        # each line in the file corresponds to one row of the grid
        grid = []
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    # converts each row into a list of characters
                    grid.append(list(line))
        return Grid(grid)

    def in_bounds(self, cell):
        # checks whether a cell is inside the grid boundaries
        row, col = cell
        return 0 <= row < self.rows and 0 <= col < self.cols

    def is_blocked(self, cell):
        # returns True if the cell is blocked
        row, col = cell
        return self.grid[row][col] == '#'

    def neighbors(self, cell):
        # returns all unblocked 4-connected neighbors of a cell
        row, col = cell
        directions = [
            (-1, 0),  # up
            (1, 0),   # down
            (0, -1),  # left
            (0, 1)    # right
        ]

        result = []
        for dr, dc in directions:
            next_cell = (row + dr, col + dc)
            # only includes neighbors that are in bounds and not blocked
            if self.in_bounds(next_cell) and not self.is_blocked(next_cell):
                result.append(next_cell)

        return result

    def print_grid(self):
        # prints the grid
        for row in self.grid:
            print("".join(row))
