"""
Solutions for Day 7
"""


import functools as ft
import re
from statistics import mode, StatisticsError


def part1(input_lines):
    """
    Wandering further through the circuits of the computer, you come upon a
    tower of programs that have gotten themselves into a bit of trouble. A
    recursive algorithm has gotten out of hand, and now they're balanced
    precariously in a large tower.

    One program at the bottom supports the entire tower. It's holding a
    large disc, and on the disc are balanced several more sub-towers. At the
    bottom of these sub-towers, standing on the bottom disc, are other programs,
    each holding their own disc, and so on. At the very tops of these
    sub-sub-sub-...-towers, many programs stand simply keeping the disc below
    them balanced but with no disc of their own.

    You offer to help, but first you need to understand the structure of these towers.
    You ask each program to yell out their name, their weight, and (if they're holding
    a disc) the names of the programs immediately above them balancing on that disc.
    You write this information down (your puzzle input). Unfortunately, in their panic,
    they don't do this in an orderly fashion; by the time you're done, you're not sure
    which program gave which information.

    For example, if your list is the following:

    pbga (66)
    xhth (57)
    ebii (61)
    havc (66)
    ktlj (57)
    fwft (72) -> ktlj, cntj, xhth
    qoyq (66)
    padx (45) -> pbga, havc, qoyq
    tknk (41) -> ugml, padx, fwft
    jptl (61)
    ugml (68) -> gyxo, ebii, jptl
    gyxo (61)
    cntj (57)

    ...then you would be able to recreate the structure of the towers that looks like this:

                    gyxo
                  /
             ugml - ebii
           /      \
          |         jptl
          |
          |         pbga
         /        /
    tknk --- padx - havc
         \        \
          |         qoyq
          |
          |         ktlj
           \      /
             fwft - cntj
                  \
                    xhth

    In this example, tknk is at the bottom of the tower (the bottom program), and is
    holding up ugml, padx, and fwft. Those programs are, in turn, holding up other
    programs; in this example, none of those programs are holding up any other programs,
    and are all the tops of their own towers. (The actual tower balancing in front of
    you is much larger.)

    Before you're ready to help them, you need to make sure your information is correct.
    What is the name of the bottom program?
    """
    # This is a DAG problem. We need to form a dependency graph.
    tower = get_tower(input_lines)
    return find_root(tower)


def get_tower(lines):
    tower = {}
    for line in lines:
        (prog, weight, holding) = parse(line)
        tower[prog] = (weight, holding)
    return tower


SHOUT_RX = re.compile(r"(\w+)\s+\((\d+)\)(?:\s+->\s+(.+))?\s*\n?")


def parse(line):
    m = re.fullmatch(SHOUT_RX, line)
    if not m:
        raise ValueError("Bad input line: {}".format(line))
    (name, weight, holding) = m.groups()
    if holding is not None:
        holding = re.split(r"\s*,\s*", holding)
    return (name, int(weight), holding or [])


def find_root(tower):
    """
    Every program in the tower lists its dependents.
    Look at the list and determine which program wasn't listed
    as dependent. That's the root.
    """
    # Sublime's syntax highlighter complains about one of these parens.
    # I've no idea why...
    deps = {
        dep for (prog, (weight, holding)) in tower.items()
            for dep in holding
    }
    for (prog, (weight, holding)) in tower.items():
        if prog not in deps:
            return prog


def part2(input_lines):
    """
    The programs explain the situation: they can't get down. Rather, they could get down,
    if they weren't expending all of their energy trying to keep the tower balanced.
    Apparently, one program has the wrong weight, and until it's fixed, they're stuck here.

    For any program holding a disc, each program standing on that disc forms a sub-tower.
    Each of those sub-towers are supposed to be the same weight, or the disc itself isn't
    balanced. The weight of a tower is the sum of the weights of the programs in that tower.

    In the example above, this means that for ugml's disc to be balanced, gyxo, ebii, and
    jptl must all have the same weight, and they do: 61.

    However, for tknk to be balanced, each of the programs standing on its disc and all
    programs above it must each match. This means that the following sums must all be the
    same:

        - ugml + (gyxo + ebii + jptl) = 68 + (61 + 61 + 61) = 251
        - padx + (pbga + havc + qoyq) = 45 + (66 + 66 + 66) = 243
        - fwft + (ktlj + cntj + xhth) = 72 + (57 + 57 + 57) = 243
    
    As you can see, tknk's disc is unbalanced: ugml's stack is heavier than the other two.
    Even though the nodes above ugml are balanced, ugml itself is too heavy: it needs to be
    8 units lighter for its stack to weigh 243 and keep the towers balanced. If this change
    were made, its weight would be 60.

    Given that exactly one program is the wrong weight, what would its weight need to be to
    balance the entire tower?
    """
    tower = get_tower(input_lines)

    # Here are some facts:
    # If there is one node standing on a disc, it cannot have the wrong weight. It is balanced by definition.
    # For the same reason, the root program cannot have the wrong weight.
    # If exactly two programs are standing on a disc, then they must both have the right height:
    #   - otherwise which one is "wrong"? The problem stipulates exactly one wrong program.
    #   - if either node is a leaf (not holding a disc) then we cannot decide which is wrong
    #   - if both nodes are non-leaves, we can say they are both right and search higher on both branches for wrong weights
    # If 3+ programs are standing on a disc, and one has a different weight from the others, it is wrong

    # There's actually 2 recursive things going on here.
    #   1) Finding the total weight of a node. This is easy-mode recursion, and we can LRU cache it for speedup.
    #   2) Finding the incorrect weight. This uses the facts outlined above:
    #       Base case: node w/ 2 children, one of whom is a leaf: Error (ill-defined problem; cannot determine incorrect node)
    #       Base case: node w/ 3+ children, one with unequal weight: return delta between its weight and the others'
    #           * If that correction results in a weight of 0 or less, it's not a base case! We'll assume weights must be positive.
    #       Base case: leaf node: return None/False (it's balanced; no further work to do)
    #       Recursion: return the non-False value of find_weight_correction() among children; False if all results are False.

    @ft.lru_cache(maxsize=512)
    def node_weight(prog):
        (p_weight, holding) = tower[prog]
        held_weight = sum(node_weight(p) for p in holding)
        return p_weight + held_weight

    def is_leaf(prog):
        return not tower[prog][1]

    def find_weight_correction(prog):
        print("check", prog, "...")
        (p_weight, holding) = tower[prog]
        # Leaf?
        if not holding:
            print("leaf: balanced")
            return False
        # Find majority. StatsError = no mode = 2 children, or more than 1 incorrect weight.
        held_weights = [node_weight(p) for p in holding]
        try:
            majority_weight = mode(held_weights)
        except StatisticsError as e:
            raise AssertionError(
                "Bad problem definition - no majority weight found for node {}'s disc"
                .format(prog)) from e
        # Is there an inconsistent weight?
        bad_idx = None
        for (i, weight) in enumerate(held_weights):
            if weight != majority_weight:
                bad_idx = i
                break
        print("weights:", held_weights, "bad one?", bad_idx)
        # Found a bad weight?
        if bad_idx is not None:
            bad_child = holding[bad_idx]
            delta = majority_weight - held_weights[bad_idx]
            new_weight = tower[bad_child][0] + delta
            # Weights cannot be reduced to 0 or less (we assume - the problem did not state such)
            if new_weight > 0:
                return new_weight
            # Recurse: Search child
            return find_weight_correction(child)
        # Recurse: Search ALL children
        for child in holding:
            correct_weight = find_weight_correction(child)
            if correct_weight is not False:
                return correct_weight
        # Nothing wrong in this sub-tree...
        return False

    correct_weight = find_weight_correction(find_root(tower))
    if correct_weight is False:
        raise AssertionError("No correct weight found! Bad input, or time to debug...")
    return correct_weight
