import argparse
import os
import re

from math import sqrt
from itertools import combinations


from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __repr__(self):
        return f"({self.x}, {self.y})"


@dataclass(frozen=True)
class Beacon(Point):
    def distance(self, other: 'Beacon') -> float:
        return sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)


@dataclass
class Scanner:
    id: int
    pos: Point
    beacons: set[Beacon]

    def distances(self) -> dict[tuple[Beacon], float]:
        return {(a, b): a.distance(b) for a, b in combinations(self.beacons, 2)}




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
                output.append(Scanner(scanner, Point(0, 0), beacons))
                scanner += 1
        output.append(Scanner(scanner, Point(0, 0), beacons))
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

    positions = {s.id: Point(0, 0) for s in scanners}
    print(positions)
