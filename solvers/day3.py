"""
Day 3 Solutions
"""


import numpy as np


def part1(input_lines):
    """
    You come across an experimental new kind of memory stored on an infinite two-dimensional grid.

    Each square on the grid is allocated in a spiral pattern starting at a location marked 1
    and then counting up while spiraling outward. For example, the first few squares are
    allocated like this:

    17  16  15  14  13
    18   5   4   3  12
    19   6   1   2  11
    20   7   8   9  10
    21  22  23---> ...
    
    While this is very space-efficient (no squares are skipped), requested data must be
    carried back to square 1 (the location of the only access port for this memory system)
    by programs that can only move up, down, left, or right. They always take the shortest path:
    the Manhattan Distance between the location of the data and square 1.

    For example:

        - Data from square 1 is carried 0 steps, since it's at the access port.
        - Data from square 12 is carried 3 steps, such as: down, left, left.
        - Data from square 23 is carried only 2 steps: up twice.
        - Data from square 1024 must be carried 31 steps.
    
    How many steps are required to carry the data from the square identified in your puzzle
    input all the way to the access port?
    """
    # Note: Rotation is right -> top -> left -> bottom; starting one cell away from the corner.
    # The size of the array is the smallest square-of-an-odd-int that fits our count
    # 1, 9, 25, etc.
    cell = int(input_lines[0])
    # (Special base case for 1)
    if cell == 1:
        return 0
    diam = 1
    while diam ** 2 < cell:
        diam += 2
    radius = diam // 2
    inner_area = (diam - 2) ** 2
    # Consider our cell as being on the "perimeter". We basically need to determine
    # distance-to-center of the side we're on (corners being the farthest away)
    # For the 3x3 case, this goes like so as we walk the spiral: 0, 1, 0, 1, 0, 1, 0, 1
    # The 5x5 case goes: 1, 0, 1, 2, 1, 0, 1, 2, ...
    # The 7x7 case goes: 2, 1, 0, 1, 2, 3, ...
    # Note that it's (decreasing, 0, increasing), shifted left by 1 due to where we start the spiral.
    # We use a modulus of diameter - 1 to rotate through that array, finding that delta.
    mod = diam - 1
    deltas = abs(np.array(range(mod)) - radius + 1)
    delta_to_center_of_side = deltas[(cell - inner_area) % mod - 1]
    # Now our distance is that delta + the radius!
    return delta_to_center_of_side + radius


def part2(input_lines):
    """
    As a stress test on the system, the programs here clear the grid and then store the value 1 in square 1.
    Then, in the same allocation order as shown above, they store the sum of the values in all adjacent squares,
    including diagonals.

    So, the first few squares' values are chosen as follows:

        - Square 1 starts with the value 1.
        - Square 2 has only one adjacent filled square (with value 1), so it also stores 1.
        - Square 3 has both of the above squares as neighbors and stores the sum of their values, 2.
        - Square 4 has all three of the aforementioned squares as neighbors and stores the sum of their values, 4.
        - Square 5 only has the first and fourth squares as neighbors, so it gets the value 5.

    Once a square is written, its value does not change. Therefore, the first few squares would receive
    the following values:

    147  142  133  122   59
    304    5    4    2   57
    330   10    1    1   54
    351   11   23   25   26
    362  747  806--->   ...

    What is the first value written that is larger than your puzzle input?
    """
    class SpiralGrid:
        """
        It was easier for me to conceptualize this as a class, so I did.

        This implements the spiral grid plus the debug storage method above.
        It knows how to run one layer of the spiral at a time, and how to
        reverse-search its data store for the right target value.
        """
        def __init__(self):
            self.x = 0
            self.y = 0
            self.cell = 2
            self.layer = 1
            self.map = {(0,0): 1}
            self.data = [1]
        def store(self):
            sum_ = 0
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    neighbor = (self.x + dx, self.y + dy)
                    if neighbor in self.map:
                        nval = self.data[self.map[neighbor] - 1]
                        sum_ += nval
            self.map[(self.x, self.y)] = self.cell
            self.data.append(sum_)
            self.cell += 1
        def up(self):
            self.y += 1
            self.store()
        def down(self):
            self.y -= 1
            self.store()
        def left(self):
            self.x -= 1
            self.store()
        def right(self):
            self.x += 1
            self.store()
        def fill_layer(self):
            side_len = (2 * self.layer)
            # Right to start
            self.right()
            # Up to the corner
            for _ in range(side_len - 1):
                self.up()
            # Left, then down, then right
            for _ in range(side_len):
                self.left()
            for _ in range(side_len):
                self.down()
            for _ in range(side_len):
                self.right()
            # Increment working layer
            self.layer += 1
        def get_cell_number(self, x, y):
            while self.layer <= max(abs(x), abs(y)):
                self.fill_layer()
            return self.map[(x, y)]
        def locate_target_sum(self, target):
            # We just do this one layer at a time,
            # then scan backwards once we're in the right layer.
            while self.data[-1] <= target:
                self.fill_layer()
            i = -1
            while self.data[i] > target:
                i -= 1
            return self.data[i + 1]

    target = int(input_lines[0])
    g = SpiralGrid()
    return g.locate_target_sum(target)
