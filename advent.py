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


import sys

from solvers import *


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

    # Locate the "dayN" module imported from solvers.
    # In there, locate the "partM" function.
    dstr = "day" + str(day)
    pstr = "part" + str(part)
    if dstr not in globals():
        log("{} is not a valid day. It may not have been written yet. "
            "Please provide an integer in the range (1,{})".format(day, ADVENT_DAYS+1))
        exit(1)
    solver = getattr(globals()[dstr], pstr, None)
    if solver is None:
        log("{} is not a valid part for day {}. It may not have been written yet. "
            "In general, each day only has 2 parts. "
            "Please make sure you provide a positive integer.".format(part, day))
        exit(1)

    # Call it =)
    solution = solver(text)
    log("Solution for Day {}, Part {}:".format(day, part))
    print(solution)


if __name__ == "__main__":
    main()
