import argparse
import os
import re

from math import sqrt
from itertools import combinations


from dataclasses import dataclass


@dataclass(frozen=True)
class Beacon:
    x: int
    y: int

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def distance(self, other: 'Beacon') -> float:
        return sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)


@dataclass(frozen=True)
class Scanner:
    id: int
    beacons: set[Beacon]

    def distances(self) -> list[float]:
        return [a.distance(b) for a, b in combinations(self.beacons, 2)]


def read_input(filepath: str) -> list[Scanner]:
    output = list()
    scanner = 0
    with open(filepath, 'r') as f:
        for line in (l.strip() for l in f.readlines()):
            if line.startswith("---"):
                beacons = set()
            elif line != '':
                point = line.split(',')
                beacons.add(Beacon(int(point[0]), int(point[1])))
            else:
                output.append(Scanner(scanner, beacons))
                scanner += 1
        output.append(Scanner(scanner, beacons))
    return output


def init_parser() -> str:
    parser = argparse.ArgumentParser(description="Advent of Code day 19 solution.")
    parser.add_argument('input', metavar='FILE', type=str, nargs=1, help="Path to input data.")
    args = parser.parse_args()
    return os.path.realpath(args.input[0])


if __name__ == "__main__":
    path = init_parser()
    scanners = read_input(path)

    for scanner in scanners:
        print(scanner)
        print(scanner.distances())
