"""
DAY 11:

Crossing the bridge, you've barely reached the other side of the stream when
a program comes up to you, clearly in distress. "It's my child process," she
says, "he's gotten lost in an infinite grid!"

Fortunately for her, you have plenty of experience with infinite grids.

Unfortunately for you, it's a hex grid.

The hexagons ("hexes") in this grid are aligned such that adjacent hexes can be
found to the north, northeast, southeast, south, southwest, and northwest:

      \ n  /
    nw +--+ ne
      /    \
    -+      +-
      \    /
    sw +--+ se
      / s  \

You have the path the child process took. Starting where he started, you need
to determine the fewest number of steps required to reach him. (A "step" means
to move from the hex you are in to any adjacent hex.)

For example:

    - ne,ne,ne is 3 steps away.
    - ne,ne,sw,sw is 0 steps away (back where you started).
    - ne,ne,s,s is 2 steps away (se,se).
    - se,sw,se,sw,sw is 3 steps away (s,s,sw).

--- Part Two ---

How many steps away is the furthest he ever got from his starting position?

"""


import re

import numpy as np


# x-y offsets for steps in the hex grid, in units of hexes.
# Stepping N/S is a full step. Stepping diagonally (NE/SE/NW/SW)
# is a half-hex to the N or S, and a full hex E or W.
OFFSETS = {
    "n":  np.array(( 0,  1), dtype=float),
    "ne": np.array(( 1,  0.5), dtype=float),
    "se": np.array(( 1, -0.5), dtype=float),
    "s":  np.array(( 0, -1), dtype=float),
    "sw": np.array((-1, -0.5), dtype=float),
    "nw": np.array((-1,  0.5), dtype=float),
}


def walk(steps, start=None):
    """
    Walk a path specified in hex steps.
    """
    coords = np.zeros(2, dtype=float) if start is None else start
    for step in steps:
        coords = coords + OFFSETS[step]
    return coords


def walk_with_max(steps, start=None):
    """
    Walk a specified path, determining where we end, and also
    the farthest distance from the origin we reach during the
    path.
    """
    coords = np.zeros(2, dtype=float) if start is None else start
    max_dist = 0
    for step in steps:
        print("step")
        coords = coords + OFFSETS[step]
        max_dist = max(max_dist, get_distance(coords))
    return coords, max_dist


def get_distance(coords):
    """
    Get shortest distance in hex steps from origin to coords.
    """
    # Special case: Did we end up where we started?
    if coords[0] == 0 and coords[1] == 0:
        return 0
    # N/S easy cases: just walk N or S
    if coords[0] == 0:
        return abs(coords[1])
    # Everything else: Walk east or west, keeping delta-Y minimal.
    # Then, when delta-X is zero, walk N or S to finish.
    if coords[0] < 0:
        northish = OFFSETS["ne"]
        southish = OFFSETS["se"]
    else:
        northish = OFFSETS["nw"]
        southish = OFFSETS["sw"]
    steps = 0
    while coords[0]:
        steps += 1
        if coords[1] > 0:
            coords = coords + southish
        else:
            coords = coords + northish
    if int(coords[1]) != coords[1]:
        raise AssertionError("Incorrect E/W walking algorithm - "
            "ended with Y-coord {}".format(coords[1]))
    return int(steps + abs(coords[1]))


def part1(input_lines):
    """
    Walk the specified path, then figure out how far away it was.
    """
    steps = re.split(r"\s*,\s*", "".join(input_lines).lower())
    coords = walk(steps)
    return get_distance(coords)


def part2(input_lines):
    """
    Use the updated walk_with_max().
    """
    steps = re.split(r"\s*,\s*", "".join(input_lines).lower())
    (_, max_dist) = walk_with_max(steps)
    return max_dist
