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

    Returns a 3-tuple: the brace counter (should be zero for correct input),
    the scores array (for part 1) and the garbage scores array (for part 2).
    """
    counter = 1
    scores = []
    garbage_scores = []
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
            (i, gscore) = parse_garbage(text, i+1)
            garbage_scores.append(gscore)
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
    return (counter, scores, garbage_scores)


def parse_garbage(text, i):
    """
    Scans garbage, returning the text position after the end of the garbage.
    Now also returns the garbage's "score" - the # of characters, not counting
    the opening/closing <> and any !'s or characters they cancel.

    The i parameter is the text position *after* the opening <
    """
    score = 0
    # Loop 'til the closing > is found.
    while True:
        m = re.match(r"[^!>]*[!>]", text[i:])
        if not m:
            raise ValueError("Bad syntax (after position {}) in garbage: Expecting >".format(i))
        delta = m.end(0) - m.start(0)
        i += delta
        score += delta
        if text[i-1] == ">":
            return (i, score - 1)
        # If we get here, we hit a ! - skip it and the char following.
        i += 1
        score -= 1


def parse_input(input_lines):
    """
    Wrapper for part1/part2 common code.
    """
    text = "".join(input_lines).replace("\n", "")
    if text[0] != "{":
        raise ValueError("Bad syntax - must begin with a {{ group")
    (counter, scores, garbage_scores) = parse_groups(text)
    if counter > 0:
        raise ValueError("Bad syntax - EOF reached with {} unclosed groups".format(counter))
    return (scores, garbage_scores)


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
    (scores, _) = parse_input(input_lines)
    return sum(scores)


def part2(input_lines):
    """
    Now, you're ready to remove the garbage.

    To prove you've removed it, you need to count all of the characters within
    the garbage. The leading and trailing < and > don't count, nor do any
    canceled characters or the ! doing the canceling.

        - <>, 0 characters.
        - <random characters>, 17 characters.
        - <<<<>, 3 characters.
        - <{!>}>, 2 characters.
        - <!!>, 0 characters.
        - <!!!>>, 0 characters.
        - <{o"i!a,<{i<a>, 10 characters.
    
    How many non-canceled characters are within the garbage in your puzzle input?
    """
    (_, garbage_scores) = parse_input(input_lines)
    return sum(garbage_scores)
