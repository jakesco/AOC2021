import argparse
import os
import re

from math import sqrt
from itertools import combinations
from functools import reduce


from dataclasses import dataclass


@dataclass(frozen=True)
class Vector:
    x: float
    y: float
    z: float

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def add(self, other: 'Vector') -> 'Vector':
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def sub(self, other: 'Vector') -> 'Vector':
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def mul(self, scalar: float) -> 'Vector':
        return Vector(self.x * scalar, self.y * scalar, self.x * scalar)

    def div(self, scalar: float) -> 'Vector':
        return Vector(self.x / scalar, self.y / scalar, self.x / scalar)


@dataclass(frozen=True)
class Rotation:
    a: Vector
    b: Vector
    c: Vector

    def apply(self, vec: Vector) -> Vector:
        return Vector(
            self.a.x * vec.x + self.a.y * vec.y + self.a.z * vec.z,
            self.b.x * vec.x + self.b.y * vec.y + self.b.z * vec.z,
            self.c.x * vec.x + self.c.y * vec.y + self.c.z * vec.z,
        )


@dataclass(frozen=True)
class Beacon(Vector):
    def distance(self, other: 'Beacon') -> float:
        return sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)


@dataclass(frozen=True)
class Scanner:
    id: int
    beacons: set[Beacon]

    @property
    def distances(self) -> dict[tuple[Beacon], float]:
        """Calculates the distances of all the beacons from each other."""
        return {(a, b): a.distance(b) for a, b in combinations(self.beacons, 2)}


def centroid(beacons: set[Vector]) -> Vector:
    """Calculates the centroid of beacons."""
    return reduce(lambda x, y: x.add(y), beacons).div(len(beacons))


def translation(s0: Scanner, s1: Scanner) -> Vector | None:
    """
    Returns a translation vector to move scanner 0 to scanner 1.
    This requires at least 12 beacons are known to overlap.
    """
    x = centroid(s0.beacons)
    y = centroid(s1.beacons)
    return x.sub(y)

def rotation(s0: Scanner, s1: Scanner) -> Rotation:
    """
    Returns a rotation matrix to align scanner 0 to scanner 1.
    This requires at least 12 beacons are known to overlap.
    """
    pass

def read_input(filepath: str) -> list[Scanner]:
    output = list()
    scanner = 0
    with open(filepath, 'r') as f:
        for line in (l.strip() for l in f.readlines()):
            if line.startswith("---"):
                beacons = set()
            elif line != '':
                point = line.split(',')
                beacons.add(Beacon(int(point[0]), int(point[1]), 0))
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
    origin = scanners[0]

    rot = Rotation(Vector(0, -1, 0), Vector(1, 0, 0), Vector(0, 0, 1))
    rot2 = Rotation(Vector(0, -1, 0), Vector(1, 0, 0), Vector(0, 0, 1))
    vec = Vector(1, 0, 0)
    print(vec)
    print(rot.apply(vec))
