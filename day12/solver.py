from collections import defaultdict
import string

from runner_utils import expected_test_result

DEFAULT_LOWEST_STEPS = float('inf')
HEIGHT_INDEX = string.printable[9:]
HEIGHT_EQUIVALENT = {
    "S": "a",
    "E": "z"
}


class Node:
    def __init__(self, height):
        height = HEIGHT_EQUIVALENT.get(height, height)
        self.height = HEIGHT_INDEX.index(height)
        self.neighbours = []
        self._available_steps = None

    def add_neighbour(self, neighbour):
        self.neighbours.append(neighbour)
        neighbour.neighbours.append(self)

    def get_available_steps(self):
        if self._available_steps is None:
            steps = [n for n in self.neighbours if n.height <= self.height + 1]
            self._available_steps = steps
        return self._available_steps

    def __repr__(self):
        return f"{self.height}"


def find_lowest_steps(start, end):
    scores = defaultdict(set)
    scores[0].add(start)
    node = start
    visited = set([node])

    while scores:
        for node in scores.pop(steps := min(scores.keys())):
            for subnode in node.get_available_steps():
                if subnode is end:
                    return steps + 1
                if subnode not in visited:
                    scores[steps + 1].add(subnode)
                    visited.add(subnode)
    return DEFAULT_LOWEST_STEPS


def make_grid(input):
    lowest_nodes = []
    grid = []
    start = None
    end = None
    for column_idx, line in enumerate(input.strip().splitlines()):
        row = []
        for row_idx, height in enumerate(line):
            node = Node(height)
            if node.height == 1:
                lowest_nodes.append(node)
            if height == "S":
                start = node
            if height == "E":
                end = node

            row.append(node)
            if row_idx > 0:
                row[row_idx - 1].add_neighbour(node)
            if column_idx > 0:
                grid[column_idx - 1][row_idx].add_neighbour(node)
        grid.append(row)
    return start, end, lowest_nodes


@expected_test_result(31)
def solve1(input):
    start, end, _ = make_grid(input)
    return find_lowest_steps(start, end)


@expected_test_result(29)
def solve2(input):
    _, end, lowest_nodes = make_grid(input)
    return min([find_lowest_steps(n, end) for n in lowest_nodes])
