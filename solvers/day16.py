"""
--- Day 16: Permutation Promenade ---

You come upon a very unusual sight; a group of programs here appear to be
dancing.

There are sixteen programs in total, named a through p. They start by standing
in a line: a stands in position 0, b stands in position 1, and so on until p,
which stands in position 15.

The programs' dance consists of a sequence of dance moves:
    
    - Spin, written sX, makes X programs move from the end to the front, but
      maintain their order otherwise. (For example, s3 on abcde produces
      cdeab).
    - Exchange, written xA/B, makes the programs at positions A and B swap
      places.
    - Partner, written pA/B, makes the programs named A and B swap places.

For example, with only five programs standing in a line (abcde), they could do the following dance:

    - s1, a spin of size 1: eabcd.
    - x3/4, swapping the last two programs: eabdc.
    - pe/b, swapping programs e and b: baedc.

After finishing their dance, the programs end up in order baedc.

You watch the dance for a while and record their dance moves (your puzzle
input). In what order are the programs standing after their dance?

--- Part Two ---

Now that you're starting to get a feel for the dance moves, you turn your
attention to the dance as a whole.

Keeping the positions they ended up in from their previous dance, the programs
perform it again and again: including the first dance, a total of one billion
(1000000000) times.

In what order are the programs standing after their billion dances?
"""


import re

import numpy as np


def spin(progs, s):
    si = len(progs) - int(s)
    return progs[si:] + progs[:si]

def exchange(progs, p1, p2):
    (i1, i2) = (int(p1), int(p2))
    (progs[i1], progs[i2]) = (progs[i2], progs[i1])
    return progs

def partner(progs, p1, p2):
    return exchange(progs, progs.index(p1), progs.index(p2))


def test(*args):
    print(args[1:])


INITIAL_PROGS = "abcdefghijklmnop"

MOVE_MAP = {
    re.compile(r"s(\d+)"): spin,
    re.compile(r"x(\d+)/(\d+)"): exchange,
    re.compile(r"p(.)/(.)"): partner
}


def dance(progs, moves):
    """Dynamically perform the dance, given move strings."""
    for move in moves:
        for (rx, func) in MOVE_MAP.items():
            m = rx.match(move)
            if m:
                progs = func(progs, *m.groups())
    return progs


def parse_moves(moves):
    """We can do all the regex processing once to speed things up."""
    compiled = []
    for move in moves:
        for (rx, func) in MOVE_MAP.items():
            m = rx.match(move)
            if m:
                compiled.append((func, m.groups()))
    return compiled


def fastdance(progs, compiled_moves):
    """Dance faster using parsed moves."""
    for (func, args) in compiled_moves:
        progs = func(progs, *args)
    return progs


def detect_cycle(init_progs, compiled_moves):
    """Find a cycle length by repeating a list of compiled moves"""
    progs = fastdance(list(init_progs), compiled_moves)
    cycle = 1
    while progs != init_progs:
        progs = fastdance(progs, compiled_moves)
        cycle += 1
    return cycle


def part1(input_lines):
    """Just run the dance."""
    progs = list(INITIAL_PROGS)
    moves = "".join(input_lines).split(",")
    return "".join(dance(progs, moves))


def lcm(a, b):
    x = max(a, b)
    while True:
        if x % a == 0 and x % b == 0:
            return x
        x += 1


def part2(input_lines):
    """
    Run the dance a billion times. Except that we can't. It'll take
    too long.
    The dance is effectively a permutation. Well, it's really two.
    One for the swap/exchanges. One for the partnering.
    What we want to do is detect cycles in the dancing process, because
    that allows us to skip (hopefully) maaaaaany steps.
    Keep in mind that permutations can be performed via matrix, as well.
    So we can leverage numpy to speed things up.

    https://www.reddit.com/r/adventofcode/comments/7k5mrq/spoilers_in_title2017_day_16_part_2_cycles/

    is very, very handy.
    """
    progs = list(INITIAL_PROGS)
    moves = "".join(input_lines).split(",")
    # The neat intuition from the subreddit is that we can separate the
    # two permutations, basically rearranging the dance, without changing
    # its effect.
    sx_moves = parse_moves([m for m in moves if m[0] == "s" or m[0] == "x"])
    p_moves = parse_moves([m for m in moves if m[0] == "p"])
    # Then, we can find the cycle length of each of these and know
    # how many whole dances must be performed, overall, before the
    # programs are back in their initial order.
    sx_cycle = detect_cycle(progs, sx_moves)
    p_cycle = detect_cycle(progs, p_moves)
    # The actual cycle length is the LCM of those 2 sub-cycles.
    cycle_length = lcm(sx_cycle, p_cycle)
    # Now the *actual* number of times we need to run the dance is the remainder,
    # after dividing 1,000,000,000 by the cycle length.
    dances_remaining = 1000000000 % cycle_length
    # print("Sub-cycles: SX - {}, P - {}".format(sx_cycle, p_cycle))
    # print("Total cycle length:", cycle_length)
    # print("Dances needed:", dances_remaining)
    moves = sx_moves + p_moves
    for _ in range(dances_remaining):
        progs = fastdance(progs, moves)
    return "".join(progs)
