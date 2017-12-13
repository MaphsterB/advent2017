"""

"""


import re


class Firewall:

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
        def __init__(self, depth, range_):
            self.depth = depth
            self.range = range_
            self.dir = 1
            self.pos = 0

    def __init__(self):
        self.layers = {}
        self.num_layers = 0

    def add_layer(self, layer, range_):
        self.layers[layer] = self.Layer(layer, range_)
        self.num_layers = max(self.num_layers, layer + 1)

    def step_scanners(self):
        for (depth, layer) in self.layers.items():
            if layer.range == 1: continue
            layer.pos += layer.dir
            if layer.dir == 1 and layer.pos == layer.range - 1:
                layer.dir = -1
            elif layer.dir == -1 and layer.pos == 0:
                layer.dir = 1

    def simulate_run(self, delay=0):
        for _ in range(delay):
            self.step_scanners()
        total_sev = 0
        caught_on = []
        for i in range(self.num_layers):
            cur_layer = self.layers.get(i)
            if cur_layer and cur_layer.pos == 0:
                total_sev += i * cur_layer.range
                caught_on.append(i)
            self.step_scanners()
        return (caught_on, total_sev)

    def __str__(self):
        return " ".join([
            str(self.layers[L].pos) if L in self.layers else "."
            for L in range(self.num_layers)
        ])


def part1(input_lines):
    """
    Just run a simulation of the passage, starting immediately
    (no delay between layers)
    """
    firewall = Firewall.parse_layers(input_lines)
    (_, total_sev) = firewall.simulate_run()
    return total_sev


def part2(input_lines):
    """
    """
    return "Unsolved"
