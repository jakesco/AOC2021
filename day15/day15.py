import argparse
import os

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
        return f"{self.risk}"


@dataclass
class PathSearch:
    node: Node
    prev: Node | None
    risk: int
    heuristic: float


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
            string.append("X" if node in path else node.__repr__())
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

    def a_star(self, start: Node) -> list[Node]:
        """Search for shortest path using A*"""
        init = PathSearch(start, None, 0, 0 + start.distance)
        q = [init]
        while q:
            current = q.pop()

            if current.node.end:
                break

            for node in self._edges[current.node]:
                new_risk = current.risk + current.node.risk
                path = PathSearch(node, current.node, new_risk, new_risk + node.distance)
                q.append(path)

            q.sort(key=lambda s: s.heuristic, reverse=True)


        return path


def read_input(filepath: str) -> Graph:
    map_ = list()
    with open(filepath, 'r') as f:
        for line in f.readlines():
            map_.append([int(n) for n in line.strip()])

    g = Graph()
    end_x = len(map_[0]) - 1
    end_y = len(map_) - 1
    end = Node(end_x, end_y, map_[end_y][end_x], 0, True)
    # Add Nodes
    for i in range(len(map_[0])):
        for j in range(len(map_)):
            if i == end_x and j == end_y:
                node = end
            else:
                dist = distance(i, j, end_x, end_y)
                node = Node(i, j, map_[j][i], dist)
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
    parser = argparse.ArgumentParser(description="Advent of Code day 2 solution.")
    parser.add_argument('input', metavar='FILE', type=str, nargs=1, help="Path to input data.")
    args = parser.parse_args()
    return os.path.realpath(args.input[0])


if __name__ == "__main__":
    path = init_parser()
    g = read_input(path)

    start_node = g.find_node(0, 0)
    shortest_path = g.a_star(start_node)

    g.render_path(shortest_path, 10)
