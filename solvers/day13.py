"""
--- Day 13: Packet Scanners ---

You need to cross a vast firewall. The firewall consists of several layers,
each with a security scanner that moves back and forth across the layer. To
succeed, you must not be detected by a scanner.

By studying the firewall briefly, you are able to record (in your puzzle input)
the depth of each layer and the range of the scanning area for the scanner
within it, written as depth: range. Each layer has a thickness of exactly 1. A
layer at depth 0 begins immediately inside the firewall; a layer at depth 1
would start immediately after that.

For example, suppose you've recorded the following:

0: 3
1: 2
4: 4
6: 4

This means that there is a layer immediately inside the firewall (with range 3),
a second layer immediately after that (with range 2), a third layer which
begins at depth 4 (with range 4), and a fourth layer which begins at depth 6
(also with range 4). Visually, it might look like this:

 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]

Within each layer, a security scanner moves back and forth within its range.
Each security scanner starts at the top and moves down until it reaches the
bottom, then moves up until it reaches the top, and repeats. A security
scanner takes one picosecond to move one step. Drawing scanners as S, the first
few picoseconds look like this:


Picosecond 0:
 0   1   2   3   4   5   6
[S] [S] ... ... [S] ... [S]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]

Picosecond 1:
 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

Picosecond 2:
 0   1   2   3   4   5   6
[ ] [S] ... ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]

Picosecond 3:
 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] ... [ ]
[S] [S]         [ ]     [ ]
[ ]             [ ]     [ ]
                [S]     [S]

Your plan is to hitch a ride on a packet about to move through the firewall.
The packet will travel along the top of each layer, and it moves at one layer
per picosecond. Each picosecond, the packet moves one layer forward (its first
move takes it into layer 0), and then the scanners move one step. If there is a
scanner at the top of the layer as your packet enters it, you are caught. (If a
scanner moves into the top of its layer while you are there, you are not
caught: it doesn't have time to notice you before you leave.) If you were to do
this in the configuration above, marking your current position with
parentheses, your passage through the firewall would look like this:

Initial state:
 0   1   2   3   4   5   6
[S] [S] ... ... [S] ... [S]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]

Picosecond 0:
 0   1   2   3   4   5   6
(S) [S] ... ... [S] ... [S]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
( ) [ ] ... ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

Picosecond 1:
 0   1   2   3   4   5   6
[ ] ( ) ... ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] (S) ... ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]

Picosecond 2:
 0   1   2   3   4   5   6
[ ] [S] (.) ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] (.) ... [ ] ... [ ]
[S] [S]         [ ]     [ ]
[ ]             [ ]     [ ]
                [S]     [S]

Picosecond 3:
 0   1   2   3   4   5   6
[ ] [ ] ... (.) [ ] ... [ ]
[S] [S]         [ ]     [ ]
[ ]             [ ]     [ ]
                [S]     [S]

 0   1   2   3   4   5   6
[S] [S] ... (.) [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[ ]             [S]     [S]
                [ ]     [ ]

Picosecond 4:
 0   1   2   3   4   5   6
[S] [S] ... ... ( ) ... [ ]
[ ] [ ]         [ ]     [ ]
[ ]             [S]     [S]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] ... ... ( ) ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

Picosecond 5:
 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] (.) [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [S] ... ... [S] (.) [S]
[ ] [ ]         [ ]     [ ]
[S]             [ ]     [ ]
                [ ]     [ ]

Picosecond 6:
 0   1   2   3   4   5   6
[ ] [S] ... ... [S] ... (S)
[ ] [ ]         [ ]     [ ]
[S]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] ... ( )
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

In this situation, you are caught in layers 0 and 6, because your packet
entered the layer when its scanner was at the top when you entered it. You are
not caught in layer 1, since the scanner moved into the top of the layer once
you were already there.

The severity of getting caught on a layer is equal to its depth multiplied by
its range. (Ignore layers in which you do not get caught.) The severity of the
whole trip is the sum of these values. In the example above, the trip severity
is 0*3 + 6*4 = 24.

Given the details of the firewall you've recorded, if you leave immediately,
what is the severity of your whole trip?

--- Part Two ---

Now, you need to pass through the firewall without being caught - easier said
than done.

You can't control the speed of the packet, but you can delay it any number of
picoseconds. For each picosecond you delay the packet before beginning your
trip, all security scanners move one step. You're not in the firewall during
this time; you don't enter layer 0 until you stop delaying the packet.

In the example above, if you delay 10 picoseconds (picoseconds 0 - 9), you
won't get caught:

State after delaying:
 0   1   2   3   4   5   6
[ ] [S] ... ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]

Picosecond 10:
 0   1   2   3   4   5   6
( ) [S] ... ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]

 0   1   2   3   4   5   6
( ) [ ] ... ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

Picosecond 11:
 0   1   2   3   4   5   6
[ ] ( ) ... ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[S] (S) ... ... [S] ... [S]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]

Picosecond 12:
 0   1   2   3   4   5   6
[S] [S] (.) ... [S] ... [S]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] (.) ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

Picosecond 13:
 0   1   2   3   4   5   6
[ ] [ ] ... (.) [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [S] ... (.) [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]

Picosecond 14:
 0   1   2   3   4   5   6
[ ] [S] ... ... ( ) ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] ... ... ( ) ... [ ]
[S] [S]         [ ]     [ ]
[ ]             [ ]     [ ]
                [S]     [S]

Picosecond 15:
 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] (.) [ ]
[S] [S]         [ ]     [ ]
[ ]             [ ]     [ ]
                [S]     [S]

 0   1   2   3   4   5   6
[S] [S] ... ... [ ] (.) [ ]
[ ] [ ]         [ ]     [ ]
[ ]             [S]     [S]
                [ ]     [ ]

Picosecond 16:
 0   1   2   3   4   5   6
[S] [S] ... ... [ ] ... ( )
[ ] [ ]         [ ]     [ ]
[ ]             [S]     [S]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] ... ( )
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

Because all smaller delays would get you caught, the fewest number of
picoseconds you would need to delay to get through safely is 10.

What is the fewest number of picoseconds that you need to delay the packet to
pass through the firewall without being caught?
"""


import re


class Firewall:
    """
    Class that represents the firewall and can simulate
    its scanning. Packets can be sent across the firewall
    after a delay.

    Scanning layers of the firewall are represented
    as simple data objects by the inner class Firewall.Layer.

    This could be made considerably faster by using a better
    underlying data structure... bitmasks, mayhap?
    """

    LAYER_RX = re.compile(r"(\d+)\s*:\s*(\d+)\s*")

    @classmethod
    def parse_layers(cls, lines):
        firewall = cls()
        for (num, line) in enumerate(lines):
            m = re.fullmatch(cls.LAYER_RX, line)
            if not m:
                raise ValueError("Error in line {}: Invalid syntax.".format(num + 1))
            (layer, range_) = m.groups()
            firewall.add_layer(int(layer), int(range_))
        return firewall

    class Layer:
        """Inner Layer class. Simple data object."""
        def __init__(self, depth, range_):
            self.depth = depth
            self.range = range_
            self.dir = 1
            self.pos = 0

        def copy(self):
            c = Firewall.Layer(self.depth, self.range)
            c.dir = self.dir
            c.pos = self.pos
            return c

    def __init__(self, layers=None):
        self.layers = layers or {}
        if len(self.layers) == 0:
            self.num_layers = 0
        else:
            self.num_layers = max(k for k in self.layers.keys()) + 1

    def copy(self):
        """Return a new deep copy of the Firewall."""
        return Firewall(layers={
            k: v.copy() for (k, v) in self.layers.items()
        })

    def reset(self):
        """Reset all scanners."""
        for L in self.layers.values():
            L.pos = 0
            L.dir = 1

    def add_layer(self, layer, range_):
        self.layers[layer] = self.Layer(layer, range_)
        self.num_layers = max(self.num_layers, layer + 1)

    def step_scanners(self):
        """
        Step each layer's scanner once. Scanners scan back and forth
        within their layer's range.
        """
        for (depth, layer) in self.layers.items():
            if layer.range == 1: continue
            layer.pos += layer.dir
            if layer.dir == 1 and layer.pos == layer.range - 1:
                layer.dir = -1
            elif layer.dir == -1 and layer.pos == 0:
                layer.dir = 1

    def detect_cycle(self, limit=100000):
        """
        Speedup technique for long delays. Stepping the scanners
        each time is silly, if they're going to eventually cycle
        around again to the same spot. Find that spot and we can
        skip to it!

        Returns the cycle length.

        Update: Well that didn't work. Our puzzle input doesn't
        have short cycles >_<
        """
        delay = 1
        self.step_scanners()
        while any(L.pos for L in self.layers.values()) and delay < limit:
            print(delay)
            self.step_scanners()
            delay += 1
        self.reset()
        return delay if delay < limit else None

    def send_packet(self, delay=0, start_time=0, debug=0):
        """
        Send a packet through the firewall, optionally after a delay.
        Returns list of layers where the packet was caught
        by scanners, and the severity as described by the puzzle.

        Debug level determines verbosity:
            0 = none
            1 = print short debug before each scan step
            2 = print long debug before each scan step
            3 = print short debug before + after each scan step
            4 = print long debug before + after each scan step
        """
        picosecond = start_time + delay
        for _ in range(delay):
            self.step_scanners()
        total_sev = 0
        caught_on = []
        for i in range(self.num_layers):
            cur_layer = self.layers.get(i)
            if debug >= 1: print(self.pstr(i, picosecond))
            if cur_layer and cur_layer.pos == 0:
                total_sev += i * cur_layer.range
                caught_on.append(i)
            self.step_scanners()
            if debug >= 2: print(self.pstr(cur_layer=i))
            picosecond += 1
        return (caught_on, total_sev)

    def is_caught(self, delay=0, start_time=0, debug=0):
        """
        send_packet() with early-drop-out criteria. Instead of returning
        severity, this just checks whether we get caught at all.
        """
        picosecond = start_time + delay
        for _ in range(delay):
            self.step_scanners()
        for i in range(self.num_layers):
            cur_layer = self.layers.get(i)
            if debug >= 1: print(self.pstr(i, picosecond))
            if cur_layer and cur_layer.pos == 0:
                return True
            self.step_scanners()
            if debug >= 2: print(self.pstr(i))
            picosecond += 1
        return False

    def __str__(self):
        """String representation, for debugging."""
        return " ".join([
            str(self.layers[L].pos) if L in self.layers else "."
            for L in range(self.num_layers)
        ])

    def pstr(self, cur_layer=-1, time=None):
        """Prettier debug printout"""
        w = max(3, len(str(self.num_layers)))
        n_lines = max(L.range for L in self.layers.values())
        header = []
        if time:
            header.append("Picosecond {}:".format(time))
        header.append(" ".join([
            "{: ^{w}}".format(i, w=w) for i in range(self.num_layers)
        ]))
        lines = []
        for line in range(n_lines):
            parts = []
            for layer_idx in range(self.num_layers):
                # We could definitely clean this logic up a lot...
                if line == 0: # First line has the ... and (.) cases.
                    if layer_idx == cur_layer:
                        # Parens
                        if layer_idx in self.layers:
                            if self.layers[layer_idx].pos == line:
                                p = "(S)"
                            else:
                                p = "( )"
                        else:
                            p = "(.)"
                    elif layer_idx in self.layers:
                        if self.layers[layer_idx].pos == line:
                            p = "[S]"
                        else:
                            p = "[ ]"
                    else:
                        p = "..."
                else: # Not the first line has the "   " case; no parens.
                    if layer_idx in self.layers and line < self.layers[layer_idx].range:
                        if self.layers[layer_idx].pos == line:
                            p = "[S]"
                        else:
                            p = "[ ]"
                    else:
                        p = "   "
                parts.append("{: ^{w}}".format(p, w=w))
            lines.append(" ".join(parts))
        return "\n".join(header + lines + [""])


def part1(input_lines):
    """
    Just run a simulation of the passage, starting immediately
    (no delay between layers).
    """
    firewall = Firewall.parse_layers(input_lines)
    (_, total_sev) = firewall.send_packet()
    return total_sev


def part2(input_lines, debug=0, limit=int(1e7)):
    """
    Now we must delay by the minimal amount that doesn't get us
    caught. Brute forcing it sounds easy =)
    """
    firewall = Firewall.parse_layers(input_lines)
    # (We know delay 0 gets us caught =)
    firewall.step_scanners()
    delay = 1
    for _ in range(limit):
        # Eventually this gets faster than simulating the delay.
        checkpoint = firewall.copy()
        caught = firewall.is_caught(debug=debug)
        if not caught:
            return delay
        firewall = checkpoint
        firewall.step_scanners()
        delay += 1
    return "Limit reached!"
