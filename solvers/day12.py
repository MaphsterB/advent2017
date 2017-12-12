"""
--- Day 12: Digital Plumber ---

Walking along the memory banks of the stream, you find a small village that is
experiencing a little confusion: some programs can't communicate with each
other.

Programs in this village communicate using a fixed system of pipes. Messages
are passed between programs using these pipes, but most programs aren't
connected to each other directly. Instead, programs pass messages between each
other until the message reaches the intended recipient.

For some reason, though, some of these messages aren't ever reaching their
intended recipient, and the programs suspect that some pipes are missing. They
would like you to investigate.

You walk through the village and record the ID of each program and the IDs with
which it can communicate directly (your puzzle input). Each program has one or
more programs with which it can communicate, and these pipes are bidirectional;
if 8 says it can communicate with 11, then 11 will say it can communicate with
8.

You need to figure out how many programs are in the group that contains program
ID 0.

For example, suppose you go door-to-door like a travelling salesman and record
the following list:

0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5

In this example, the following programs are in the group that contains program
ID 0:

    Program 0 by definition.
    Program 2, directly connected to program 0.
    Program 3 via program 2.
    Program 4 via program 2.
    Program 5 via programs 6, then 4, then 2.
    Program 6 via programs 4, then 2.

Therefore, a total of 6 programs are in this group; all but program 1, which
has a pipe that connects it to itself.

How many programs are in the group that contains program ID 0?

--- Part Two ---

There are more programs than just the ones in the group containing program ID
0. The rest of them have no way of reaching that group, and still might have no
way of reaching each other.

A group is a collection of programs that can all communicate via pipes either
directly or indirectly. The programs you identified just a moment ago are all
part of the same group. Now, they would like you to determine the total number
of groups.

In the example above, there were 2 groups: one consisting of programs
0,2,3,4,5,6, and the other consisting solely of program 1.

How many groups are there in total?
"""


import re


class PipeGraph:
    """
    The graph class used to solve the puzzle.
    It simply keeps an edge table dict (which would
    let us complete the problem even if the edge list
    showed up out-of-order) and knows how to run
    a variant of Dijkstra's algorithm for visiting
    nodes until we run out of newly-discovered ones.

    Also can do this for each node in the graph,
    returning partition sets.
    """

    def __init__(self):
        self.edge_table = {}

    def add_node(self, node, edges):
        self.edge_table[node] = set(edges)

    def find_all_connections(self, start_node):
        """
        Finds all nodes connected to start_node.
        In a fully-connected graph, this will be
        the set of all nodes in the graph.
        """
        visited = {start_node}
        to_visit = set(self.edge_table[start_node])
        cur_node = None
        while len(to_visit) > 0:
            cur_node = to_visit.pop()
            if cur_node not in visited:
                visited.add(cur_node)
                to_visit = to_visit | self.edge_table[cur_node]
        return visited

    def find_partitions(self):
        """
        Find the number of partitions in the graph. Each
        partition is a set of nodes, whose members are connected
        to each other but to no other group in the graph.

        Return value is a list of sets of nodes.
        """
        checklist = set(self.edge_table.keys())
        partitions = []
        while len(checklist) > 0:
            start_node = checklist.pop()
            found = False
            for partition in partitions:
                if start_node in partition:
                    found = True
                    break
            if found: continue
            partitions.append(self.find_all_connections(start_node))
        return partitions


def parse_graph(lines):
    """
    Input parsing convenience function.
    """
    graph = PipeGraph()
    for line in lines:
        (node, edgestr) = re.split(r"\s*<->\s*", line)
        edges = [int(e) for e in re.split(r"\s*,\s*", edgestr)]
        graph.add_node(int(node), edges)
    return graph


def part1(input_lines):
    """
    Straightforward Dijkstra.
    """
    graph = parse_graph(input_lines)
    return len(graph.find_all_connections(0))


def part2(input_lines):
    """
    Now we need to find all partitions. New method added to PipeGraph.
    """
    graph = parse_graph(input_lines)
    return len(graph.find_partitions())
