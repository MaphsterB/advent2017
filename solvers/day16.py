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
"""


import re


def spin(progs, s):
    si = len(progs) - int(s)
    return progs[si:] + progs[:si]

def swap(progs, p1, p2):
    (i1, i2) = (int(p1), int(p2))
    (progs[i1], progs[i2]) = (progs[i2], progs[i1])
    return progs

def partner(progs, p1, p2):
    return swap(progs, progs.index(p1), progs.index(p2))


def test(*args):
    print(args[1:])


MOVES = {
    re.compile(r"s(\d+)"): spin,
    re.compile(r"x(\d+)/(\d+)"): swap,
    re.compile(r"p(.)/(.)"): partner
}


def part1(input_lines):
    """Just run the dance."""
    import pdb; pdb.set_trace()
    progs = list("abcdefghijklmnop")
    moves = "".join(input_lines).split(",")
    for move in moves:
        for (rx, func) in MOVES.items():
            m = rx.match(move)
            if m:
                progs = func(progs, *m.groups())
    return "".join(progs)


def part2(input_lines):
    return "Unsolved"
