"""
advent.py - Solve puzzles for Advent of Code 2017.

    Each day unlocks a new set of puzzles. Each day may have many parts.

    Usage: python advent.py <day> <part> <input>

    Days/parts are 1-indexed. e.g. Day-1/Part-1 etc.

    Input may be either textual input, or the name of a file to be read,
    or "-" to accept input from STDIN.

    Solution is printed to STDOUT.

    We do a minimal amount of sanitation/validation, but don't count on
    all goofy user input cases being caught.
"""


import functools as ft
import itertools as it
import re
import sys

import numpy as np


ADVENT_DAYS = 25


def log(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def main():
    """
    Main entry point.

    Solvers all accept an array of strings as input,
    and produce a printable solution as return values.
    """
    if len(sys.argv) != 4:
        log("Missing required args.")
        log("Usage: python advent.py <day> <part> <input>")
        exit(1)

    try:
        day = int(sys.argv[1])
    except ValueError:
        log("{} is not a valid day. Please provide an integer in the range (1,{}).".format(day, ADVENT_DAYS))
        exit(1)
    try:
        part = int(sys.argv[2])
    except ValueError:
        log("{} is not a valid part. Please provide an integer.")
        exit(1)

    input_arg = sys.argv[3]
    if input_arg == "-":
        log("stdin specified. Enter Input. EOF terminates.")
        text = sys.stdin.readlines()
    else:
        try:
            with open(input_arg, "r") as f:
                log("File {} read as input.".format(input_arg))
                text = f.readlines()
        except OSError:
            log("No file found to read. Treating arg as input.")
            text = [input_arg]
    
    # Search the main namespace for a callable named "dXpY"
    dstr = "d" + str(day)
    pstr = "p" + str(part)
    solvers = {k : v for (k, v) in globals().items() if re.fullmatch(r"d\d+p\d+", k)}
    days = {re.sub(r"p\d+", "", sname) for sname in solvers.keys()}
    if dstr not in days:
        log("{} is not a valid day. It may not have been written yet. "
            "Please provide an integer in the range (1,{})".format(day, ADVENT_DAYS+1))
        exit(1)
    if (dstr + pstr) not in solvers:
        log("{} is not a valid part for day {}. It may not be solved yet. "
            "Please make sure you provide a positive integer.".format(day, part))
        exit(1)

    # Call it =)
    solution = solvers[dstr + pstr](text)
    log("Solution for Day {}, Part {}:".format(day, part))
    print(solution)


def d1p1(input_lines):
    """
    The captcha requires you to review a sequence of digits (your puzzle input) and find
    the sum of all digits that match the next digit in the list. The list is circular,
    so the digit after the last digit is the first digit in the list.

    For example:

        - 1122 produces a sum of 3 (1 + 2) because the first digit (1) matches the second digit
          and the third digit (2) matches the fourth digit.
        - 1111 produces 4 because each digit (all 1) matches the next.
        - 1234 produces 0 because no digit matches the next.
        - 91212129 produces 9 because the only digit that matches the next one is the last digit, 9.
    """
    captcha = input_lines[0]
    captcha = captcha + captcha[0]
    return sum([
        int(captcha[i]) for i in range(1, len(captcha))
            if captcha[i] == captcha[i - 1]
    ])


def d1p2(input_lines):
    """
    Now, instead of considering the next digit, it wants you to consider the digit halfway around
    the circular list. That is, if your list contains 10 items, only include a digit in your sum
    if the digit 10/2 = 5 steps forward matches it. Fortunately, your list has an even number of elements.

    For example:

        - 1212 produces 6: the list contains 4 items, and all four digits match the digit 2 items ahead.
        - 1221 produces 0, because every comparison is between a 1 and a 2.
        - 123425 produces 4, because both 2s match each other, but no other digit has a match.
        - 123123 produces 12.
        - 12131415 produces 4.
    """
    captcha = input_lines[0]
    if len(captcha) % 2 != 0:
        raise AssertionError("Day 1, Part 2 anticaptchas must have an even number of digits!")
    offset = len(captcha) // 2
    mod = len(captcha)
    return sum([
        int(captcha[i]) for i in range(len(captcha))
            if captcha[i] == captcha[(i + offset) % mod]
    ])


def d2p1(input_lines):
    """
    The spreadsheet consists of rows of apparently-random numbers. To make sure the
    recovery process is on the right track, they need you to calculate the spreadsheet's
    checksum. For each row, determine the difference between the largest value and the
    smallest value; the checksum is the sum of all of these differences.

    For example, given the following spreadsheet:

    5 1 9 5
    7 5 3
    2 4 6 8

        - The first row's largest and smallest values are 9 and 1, and their difference is 8.
        - The second row's largest and smallest values are 7 and 3, and their difference is 4.
        - The third row's difference is 6.
        - In this example, the spreadsheet's checksum would be 8 + 4 + 6 = 18.
    """
    sanitized = [re.sub(r"[^\d\t ]+", "", line) for line in input_lines]
    vals = [
        [int(v) for v in re.split(r"\s+", line)]
        for line in sanitized
    ]
    cksum = 0
    for arr in vals:
        if len(vals):
            cksum += np.ptp(arr)
    return cksum


def d2p2(input_lines):
    """
    "Based on what we're seeing, it looks like all the User wanted is some information about
    the evenly divisible values in the spreadsheet. Unfortunately, none of us are equipped
    for that kind of calculation - most of us specialize in bitwise operations."

    It sounds like the goal is to find the only two numbers in each row where one
    evenly divides the other - that is, where the result of the division operation is a whole
    number. They would like you to find those numbers on each line, divide them, and add up
    each line's result.

    For example, given the following spreadsheet:

    5 9 2 8
    9 4 7 3
    3 8 6 5

        - In the first row, the only two numbers that evenly divide are 8 and 2;
          the result of this division is 4.
        - In the second row, the two numbers are 9 and 3; the result is 3.
        - In the third row, the result is 2.
        - In this example, the sum of the results would be 4 + 3 + 2 = 9.
    """
    sanitized = [re.sub(r"[^\d\t ]+", "", line) for line in input_lines]
    vals = [
        [int(v) for v in re.split(r"\s+", line)]
        for line in sanitized
    ]
    cksum = 0
    for arr in vals:
        for (i, j) in it.product(range(len(arr)), repeat=2):
            if i != j and arr[i] % arr[j] == 0:
                cksum += arr[i] // arr[j]
                break
    return cksum


def d3p1(input_lines):
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


def d3p2(input_lines):
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


def d4p1(input_lines):
    """
    A new system policy has been put in place that requires all accounts to use a passphrase
    instead of simply a password. A passphrase consists of a series of words (lowercase letters)
    separated by spaces.

    To ensure security, a valid passphrase must contain no duplicate words.

    For example:

        - aa bb cc dd ee is valid.
        - aa bb cc dd aa is not valid - the word aa appears more than once.
        - aa bb cc dd aaa is valid - aa and aaa count as different words.

    The system's full passphrase list is available as your puzzle input. How many passphrases are valid?
    """
    def validate(passphrase):
        words = passphrase.lower().replace("\n", "").split(" ")
        return len(set(words)) == len(words)

    return len(tuple(p for p in input_lines if validate(p)))


def d4p2(input_lines):
    """
    For added security, yet another system policy has been put in place. Now, a valid passphrase must contain no two words that are anagrams of each other - that is, a passphrase is invalid if any word's letters can be rearranged to form any other word in the passphrase.

    For example:

        - abcde fghij is a valid passphrase.
        - abcde xyz ecdab is not valid - the letters from the third word can be rearranged to form the first word.
        - a ab abc abd abf abj is a valid passphrase, because all letters need to be used when forming another word.
        - iiii oiii ooii oooi oooo is valid.
        - oiii ioii iioi iiio is not valid - any of these words can be rearranged to form any other word.
    
    Under this new system policy, how many passphrases are valid?
    """
    def validate(passphrase):
        words = passphrase.lower().replace("\n", "").split(" ")
        anagram_set = set()
        for word in words:
            entry = "".join(sorted(word))
            if entry in anagram_set:
                return False
            anagram_set.add(entry)
        return True

    return len(tuple(p for p in input_lines if validate(p)))


def d5p1(input_lines):
    """
    An urgent interrupt arrives from the CPU: it's trapped in a maze of jump instructions,
    and it would like assistance from any programs with spare cycles to help find the exit.

    The message includes a list of the offsets for each jump. Jumps are relative: -1 moves
    to the previous instruction, and 2 skips the next one. Start at the first instruction in
    the list. The goal is to follow the jumps until one leads outside the list.

    In addition, these instructions are a little strange; after each jump, the offset of that
    instruction increases by 1. So, if you come across an offset of 3, you would move three
    instructions forward, but change it to a 4 for the next time it is encountered.

    For example, consider the following list of jump offsets:

    0
    3
    0
    1
    -3

    Positive jumps ("forward") move downward; negative jumps move upward. For legibility
    in this example, these offset values will be written all on one line, with the current
    instruction marked in parentheses. The following steps would be taken before an exit
    is found:

        - (0) 3  0  1  -3  - before we have taken any steps.
        - (1) 3  0  1  -3  - jump with offset 0 (that is, don't jump at all).
          Fortunately, the instruction is then incremented to 1.
        -  2 (3) 0  1  -3  - step forward because of the instruction we just modified.
          The first instruction is incremented again, now to 2.
        -  2  4  0  1 (-3) - jump all the way to the end; leave a 4 behind.
        -  2 (4) 0  1  -2  - go back to where we just were; increment -3 to -2.
        -  2  5  0  1  -2  - jump 4 steps forward, escaping the maze.
    
    In this example, the exit is reached in 5 steps.

    How many steps does it take to reach the exit?
    """
    jumps = [int(line) for line in input_lines]
    def jump(at):
        to = (at + jumps[at])
        jumps[at] += 1
        return to
    pos = 0
    count = 0
    while pos >= 0 and pos < len(jumps):
        count += 1
        pos = jump(pos)
    return count


def d5p2(input_lines):
    """
    Now, the jumps are even stranger: after each jump, if the offset was three or more,
    instead decrease it by 1. Otherwise, increase it by 1 as before.

    Using this rule with the above example, the process now takes 10 steps,
    and the offset values after finding the exit are left as 2 3 2 3 -1.

    How many steps does it now take to reach the exit?
    """
    jumps = [int(line) for line in input_lines]
    def jump(at):
        to = (at + jumps[at])
        if jumps[at] > 2:
            jumps[at] -= 1
        else:
            jumps[at] += 1
        return to
    pos = 0
    count = 0
    while pos >= 0 and pos < len(jumps):
        count += 1
        pos = jump(pos)
    return count


def d6p1(input_lines):
    """
    In this area, there are sixteen memory banks; each memory bank can hold any number of blocks.
    The goal of the reallocation routine is to balance the blocks between the memory banks.

    The reallocation routine operates in cycles. In each cycle, it finds the memory bank with the
    most blocks (ties won by the lowest-numbered memory bank) and redistributes those blocks among
    the banks. To do this, it removes all of the blocks from the selected bank, then moves to the
    next (by index) memory bank and inserts one of the blocks. It continues doing this until it runs
    out of blocks; if it reaches the last memory bank, it wraps around to the first one.

    The debugger would like to know how many redistributions can be done before a blocks-in-banks
    configuration is produced that has been seen before.

    For example, imagine a scenario with only four memory banks:

        - The banks start with 0, 2, 7, and 0 blocks. The third bank has the most blocks,
          so it is chosen for redistribution.
        - Starting with the next bank (the fourth bank) and then continuing to the first bank,
          the second bank, and so on, the 7 blocks are spread out over the memory banks. 
          The fourth, first, and second banks get two blocks each, and the third bank gets one
          back. The final result looks like this: 2 4 1 2.
        - Next, the second bank is chosen because it contains the most blocks (four). Because
          there are four memory banks, each gets one block. The result is: 3 1 2 3.
        - Now, there is a tie between the first and fourth memory banks, both of which have
          three blocks. The first bank wins the tie, and its three blocks are distributed
          evenly over the other three banks, leaving it with none: 0 2 3 4.
        - The fourth bank is chosen, and its four blocks are distributed such that each of the
          four banks receives one: 1 3 4 1.
        - The third bank is chosen, and the same thing happens: 2 4 1 2.
        - At this point, we've reached a state we've seen before: 2 4 1 2 was already seen.
          The infinite loop is detected after the fifth block redistribution cycle, and so
          the answer in this example is 5.

    Given the initial block counts in your puzzle input, how many redistribution cycles must be
    completed before a configuration is produced that has been seen before?
    """
    banks = np.array([int(x) for x in re.split(r"\s+", input_lines[0])])
    nbanks = len(banks)
    prev_states = {tuple(banks)}
    step_count = 0
    while True:
        mi = np.argmax(banks)
        dbg = banks[mi]
        div = banks[mi] // nbanks
        rem = banks[mi] % nbanks
        banks[mi] = 0
        banks += div
        for off in range(1, rem + 1):
            banks[(mi + off) % nbanks] += 1
        step_count += 1
        key = tuple(banks)
        if key in prev_states:
            break
        prev_states.add(key)
    return step_count


def d6p2(input_lines):
    """
    Out of curiosity, the debugger would also like to know the size of the loop: starting from
    a state that has already been seen, how many block redistribution cycles must be performed
    before that same state is seen again?

    In the example above, 2 4 1 2 is seen again after four cycles, and so the answer in that
    example would be 4.

    How many cycles are in the infinite loop that arises from the configuration in your
    puzzle input?
    """
    banks = np.array([int(x) for x in re.split(r"\s+", input_lines[0])])
    def realloc(banks):
        mi = np.argmax(banks)
        nbanks = len(banks)
        dbg = banks[mi]
        (div, rem) = divmod(banks[mi], nbanks)
        banks[mi] = 0
        banks += div
        for off in range(1, rem + 1):
            banks[(mi + off) % nbanks] += 1
        return banks
    def detect_cycle(banks):
        count = 0
        states = set()
        while tuple(banks) not in states:
            count += 1
            states.add(tuple(banks))
            banks = realloc(banks)
        return (count, banks)
    (step_count, banks) = detect_cycle(banks)
    (loop_count, banks) = detect_cycle(banks)
    return loop_count


if __name__ == "__main__":
    main()
