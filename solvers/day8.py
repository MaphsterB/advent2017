"""
Day 8 Solutions
"""


import operator as op
import re


INSTRUCTION_RX = re.compile(r"(\w+)\s+(inc|dec)\s+(-?\d+)(?:\s+if\s+(\w+)\s+(>|<|[><!=]=)\s+(-?\d+))?\s*")

CMP_MAP = {
    "==": op.eq,
    "!=": op.ne,
    ">": op.gt,
    "<": op.lt,
    ">=": op.ge,
    "<=": op.le
}


def parse(line):
    m = re.fullmatch(INSTRUCTION_RX, line)
    if not m:
        raise ValueError("Bad syntax on line: {}".format(line))
    return m.groups()


def execute(symtab, reg, op, val, cmp_reg=None, cmp_op=None, cmp_val=None):
    cmp_result = True
    if cmp_reg:
        cmp_reg_val = symtab.get(cmp_reg, 0)
        cmp_val = int(cmp_val)
        cmp_result = CMP_MAP[cmp_op](cmp_reg_val, cmp_val)
    if cmp_result:
        val = int(val)
        if reg not in symtab:
            symtab[reg] = 0
        if op == "dec":
            val = -val
        symtab[reg] += val
    return symtab.get(reg, 0)


def part1(input_lines):
    """
    You receive a signal directly from the CPU. Because of your recent assistance with jump
    instructions, it would like you to compute the result of a series of unusual register
    instructions.

    Each instruction consists of several parts: the register to modify, whether to increase
    or decrease that register's value, the amount by which to increase or decrease it,
    and a condition. If the condition fails, skip the instruction without modifying the
    register. The registers all start at 0. The instructions look like this:

    b inc 5 if a > 1
    a inc 1 if b < 5
    c dec -10 if a >= 1
    c inc -20 if c == 10

    These instructions would be processed as follows:

        - Because a starts at 0, it is not greater than 1, and so b is not modified.
        - a is increased by 1 (to 1) because b is less than 5 (it is 0).
        - c is decreased by -10 (to 10) because a is now greater than or equal to 1 (it is 1).
        - c is increased by -20 (to -10) because c is equal to 10.

    After this process, the largest value in any register is 1.

    You might also encounter <= (less than or equal to) or != (not equal to).
    However, the CPU doesn't have the bandwidth to tell you what all the registers are named,
    and leaves that to you to determine.

    What is the largest value in any register after completing the instructions in your puzzle
    input?
    """
    symtab = {}
    for line in input_lines:
        execute(symtab, *parse(line))
    return max(symtab.items(), key=lambda t: t[1])


def part2(input_lines):
    """
    To be safe, the CPU also needs to know the highest value held in any register during this
    process so that it can decide how much memory to allocate to these operations. For example,
    in the above instructions, the highest value ever held was 10 (in register c after the third
    instruction was evaluated).
    """
    max_val = 0
    symtab = {}
    for line in input_lines:
        result = execute(symtab, *parse(line))
        if result > max_val:
            max_val = result
    return max_val
