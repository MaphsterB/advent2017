"""
Day 9 Solutions
"""


import re


# Lexing problem! Change state based on important characters.
# Start in group-parsing mode:
#   See { - increment open-counter; continue group-parsing.
#   See < - enter garbage-parsing mode
#   See } - decrement open-counter; if counter = 0 exit, else continue group-parsing
# garbage-parsing mode:
#   See ! - ignore whatever char follows, continue garbage-parsing
#   See > - exit garbage-parsing


def parse_groups(text):
    """
    This does the 'normal' scanning for groups. It defers to
    parse_garbage() to skip over garbage.
    """
    counter = 1
    scores = []
    i = 1
    while i < len(text):
        # Inside a group. First, check if we have an inner group or garbage.
        # Handle inner group.
        if text[i] == "{":
            i += 1
            counter += 1
            continue
        # Handle garbage - skip it.
        if text[i] == "<":
            i = parse_garbage(text, i)
            continue
        # If we get here, we need to scan. Stop scanning at , or }
        m = re.match(r"[^,}]*[,}]", text[i:])
        if not m:
            raise ValueError("Bad syntax (after position {}) in group: Expecting , or }}".format(i))
        i += m.end(0) - m.start(0)
        # If we ended on a }, process end-of-group. Save its score.
        if text[i-1] == "}":
            scores.append(counter)
            counter -= 1
            if counter < 0:
                raise ValueError("Bad syntax (position {}) in group: Too many }} closing braces".format(i))
            # Special case - skip over commas after }'s - saves us one loop.
            if i < len(text) and text[i] == ",":
                i += 1
    return (counter, scores)


def parse_garbage(text, i):
    """
    Scans garbage, returning the text position after the end of the garbage.
    """
    while True:
        m = re.match(r"[^!>]*[!>]", text[i:])
        if not m:
            raise ValueError("Bad syntax (after position {}) in garbage: Expecting >".format(i))
        i += m.end(0) - m.start(0)
        if text[i-1] == ">":
            return i
        i += 1


def part1(input_lines):
    """
    A large stream blocks your path. According to the locals, it's not safe to
    cross the stream at the moment because it's full of garbage. You look down
    at the stream; rather than water, you discover that it's a stream of
    characters.

    You sit for a while and record part of the stream (your puzzle input). The
    characters represent groups - sequences that begin with { and end with }.
    Within a group, there are zero or more other things, separated by commas:
    either another group or garbage. Since groups can contain other groups, a }
    only closes the most-recently-opened unclosed group - that is, they are
    nestable. Your puzzle input represents a single, large group which itself
    contains many smaller ones.

    Sometimes, instead of a group, you will find garbage. Garbage begins with
    < and ends with >. Between those angle brackets, almost any character can
    appear, including { and }. Within garbage, < has no special meaning.

    In a futile attempt to clean up the garbage, some program has canceled some
    of the characters within it using !: inside garbage, any character that
    comes after ! should be ignored, including <, >, and even another !.

    You don't see any characters that deviate from these rules. Outside
    garbage, you only find well-formed groups, and garbage always terminates
    according to the rules above.

    Here are some self-contained pieces of garbage:

        - <>, empty garbage.
        - <random characters>, garbage containing random characters.
        - <<<<>, because the extra < are ignored.
        - <{!>}>, because the first > is canceled.
        - <!!>, because the second ! is canceled, allowing the > to terminate the garbage.
        - <!!!>>, because the second ! and the first > are canceled.
        - <{o"i!a,<{i<a>, which ends at the first >.

    Here are some examples of whole streams and the number of groups they contain:

        - {}, 1 group.
        - {{{}}}, 3 groups.
        - {{},{}}, also 3 groups.
        - {{{},{},{{}}}}, 6 groups.
        - {<{},{},{{}}>}, 1 group (which itself contains garbage).
        - {<a>,<a>,<a>,<a>}, 1 group.
        - {{<a>},{<a>},{<a>},{<a>}}, 5 groups.
        - {{<!>},{<!>},{<!>},{<a>}}, 2 groups (since all but the last > are canceled).

    Your goal is to find the total score for all groups in your input. Each
    group is assigned a score which is one more than the score of the group
    that immediately contains it. (The outermost group gets a score of 1.)

        - {}, score of 1.
        - {{{}}}, score of 1 + 2 + 3 = 6.
        - {{},{}}, score of 1 + 2 + 2 = 5.
        - {{{},{},{{}}}}, score of 1 + 2 + 3 + 3 + 3 + 4 = 16.
        - {<a>,<a>,<a>,<a>}, score of 1.
        - {{<ab>},{<ab>},{<ab>},{<ab>}}, score of 1 + 2 + 2 + 2 + 2 = 9.
        - {{<!!>},{<!!>},{<!!>},{<!!>}}, score of 1 + 2 + 2 + 2 + 2 = 9.
        - {{<a!>},{<a!>},{<a!>},{<ab>}}, score of 1 + 2 = 3.

    What is the total score for all groups in your input?
    """
    text = "".join(input_lines).replace("\n", "")
    if text[0] != "{":
        raise ValueError("Bad syntax - must begin with a {{ group")
    (counter, scores) = parse_groups(text)
    if counter > 0:
        raise ValueError("Bad syntax - EOF reached with {} unclosed groups".format(counter))
    return sum(scores)


def part2(input_lines):
    """
    """
    return "Unsolved"
