import argparse
import os

from dataclasses import dataclass


@dataclass
class Node:
    name: str
    big: bool
    visited: bool = False

    def __hash__(self):
        return hash(self.name)

    @property
    def can_visit(self):
        return self.big or not self.visited


@dataclass(frozen=True)
class Path:
    path: set[Node]

    @property
    def length(self):
        return len(self.path)


class Graph:
    def __init__(self):
        self.__lookup: dict[str, Node] = dict()
        self.__nodes: dict[Node, set[Node]] = dict()

    def __str__(self):
        output = []
        for k, v in self.__nodes.items():
            output.append(f"{k.name} <-> {[n.name for n in v]}")
        return '\n'.join(output)

    def __new_node(self, name) -> Node:
        node = Node(name, name.isupper())
        self.__lookup[name] = node
        self.__nodes[node] = set()
        return node

    def add_node(self, name: str) -> Node:
        if node := self.__lookup.get(name, None):
            return node
        return self.__new_node(name)

    def add_connection(self, name1: str, name2: str):
        node1 = self.__lookup.get(name1, None)
        if not node1:
            node1 = self.add_node(name1)

        node2 = self.__lookup.get(name2, None)
        if not node2:
            node2 = self.add_node(name2)

        self.__nodes[node1].add(node2)
        self.__nodes[node2].add(node1)

    def find_paths(self) -> set[Path]:
        # TODO: the hard part
        return set()


def read_input(filepath: str) -> Graph:
    graph = Graph()
    with open(filepath, 'r') as f:
        for line in f.readlines():
            nodes = line.rstrip().split('-')
            graph.add_connection(nodes[0], nodes[1])
    return graph


def init_parser() -> str:
    parser = argparse.ArgumentParser(description="Advent of Code day 2 solution.")
    parser.add_argument('input', metavar='FILE', type=str, nargs=1, help="Path to input data.")
    args = parser.parse_args()
    return os.path.realpath(args.input[0])


if __name__ == "__main__":
    path = init_parser()
    graph = read_input(path)
    print(graph)
    paths = graph.find_paths()
    print(f"Part 1: {len(paths)}(10) distinct paths")
