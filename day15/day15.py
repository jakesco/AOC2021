import argparse
import os
import sys

from math import sqrt

from pprint import pprint
from dataclasses import dataclass
from collections import deque


def distance(x0: int, y0: int, x1: int, y1: int) -> float:
    dx = x1 - x0
    dy = y1 - y0
    return sqrt(dx * dx + dy * dy)


@dataclass(frozen=True)
class Node:
    x: int
    y: int
    risk: int
    distance: float
    end: bool = False

    def __repr__(self):
        return f"Node(({self.x}, {self.y}), {self.risk})"


class SearchWrapper:
    def __init__(self, current: Node, previous, heuristic: int):
        self.current = current
        self.previous = previous
        self.heuristic = heuristic

    def get_path(self) -> list[Node]:
        if self.previous:
            return self.previous.get_path() + [self.current]
        return [self.current]

    def __repr__(self):
        return f"Search(({self.current.x}, {self.current.y}), {self.previous}, {self.heuristic})"


class Graph:
    def __init__(self):
        self._nodes: list[Node] = list()
        self._edges: dict[Node, set[Node]] = dict()

    def __str__(self):
        output = []
        for k, v in self._edges.items():
            output.append(f"{k} <-> {[n for n in v]}")
        return '\n'.join(output)

    def render_path(self, path: list[Node], width: int):
        string = list()
        for i in range(len(self._nodes)):
            if i % width == 0:
                string.append("\n")
            node = self._nodes[i]
            string.append("." if node in path else str(node.risk))
        print(''.join(string))

    def add_node(self, node: Node):
        self._nodes.append(node)
        self._edges[node] = set()

    def find_node(self, x: int, y: int) -> Node | None:
        for node in self._nodes:
            if node.x == x and node.y == y:
                return node
        return None

    def add_connection(self, parent: Node, child: Node):
        self._edges[parent].add(child)

    def a_star(self, start: Node) -> SearchWrapper | None:
        """Search for shortest path using A*"""
        init = SearchWrapper(start, None, 0)
        visited = set()
        q = [init]
        while q:
            sw = q.pop()

            if sw.current in visited:
                continue

            if sw.current.end:
                return sw

            for node in [n for n in self._edges[sw.current] if n not in visited]:
                hueristic = sw.heuristic + node.risk
                new_path = SearchWrapper(node, sw, hueristic)
                q.append(new_path)

            visited.add(sw.current)
            q.sort(key=lambda p: p.heuristic, reverse=True)

        return None


def calculate_risk(path: list[Node]) -> int:
    return sum([n.risk for n in path if not (n.x == n.y == 0)])


def read_input(filepath: str, *, expand: bool = False) -> Graph:
    map_ = list()
    with open(filepath, 'r') as f:
        if expand:
            print("Building Map...")
            for line in f.readlines():
                l = [int(n) for n in line.strip()]
                out = l
                for i in range(4):
                    l = [1 if n == 9 else (n + 1) for n in l]
                    out = out + l
                map_.append(out)
            rows = len(map_)
            for i in range(4):
                tmp = list()
                for j in range(-1 * rows, 0):
                    tmp.append([1 if n == 9 else (n + 1) for n in map_[j]])
                for t in tmp:
                    map_.append(t)
        else:
            for line in f.readlines():
                map_.append([int(n) for n in line.strip()])

    g = Graph()
    end_x = len(map_[0]) - 1
    end_y = len(map_) - 1
    end = Node(end_x, end_y, map_[end_y][end_x], 0, True)
    # Add Nodes
    for i in range(len(map_)):
        for j in range(len(map_[0])):
            if i == end_x and j == end_y:
                node = end
            else:
                dist = distance(i, j, end_x, end_y)
                node = Node(i, j, map_[i][j], dist)

            g.add_node(node)
    # Add Connections
    for node in g._nodes:
        for x, y in (
                (node.x + 1, node.y),
                (node.x - 1, node.y),
                (node.x, node.y + 1),
                (node.x, node.y - 1),
        ):
            if x < 0 or y < 0 or x > end_x or y > end_y:
                continue
            child = g.find_node(x, y)
            g.add_connection(node, child)
    return g


def init_parser() -> str:
    parser = argparse.ArgumentParser(description="Advent of Code day 15 solution.")
    parser.add_argument('input', metavar='FILE', type=str, nargs=1, help="Path to input data.")
    args = parser.parse_args()
    return os.path.realpath(args.input[0])


if __name__ == "__main__":
    path = init_parser()
    g = read_input(path, expand=True)
    #g = read_input(path)

    start_node = g.find_node(0, 0)
    search_result = g.a_star(start_node)
    if not search_result:
        sys.exit()

    shortest_path = search_result.get_path()
    # g.render_path(shortest_path, 500)
    g.render_path(shortest_path, 50)
    print(f"Risk: {calculate_risk(shortest_path)}")

