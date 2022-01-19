import argparse
import os

from collections.abc import Callable
from dataclasses import dataclass
from functools import reduce
from pprint import pprint


UNIQUE_ROTATIONS = (
    'X', 'Y', 'Z', 'XX', 'XY', 'XZ', 'YX', 'YY', 'ZY', 'ZZ',
    'XXX', 'XXY', 'XXZ', 'XYX', 'XYY', 'XZZ', 'YXX', 'YYY',
    'ZZZ', 'XXXY', 'XXYX', 'XYXX', 'XYYY'
)


@dataclass(frozen=True)
class Beacon:
    x: int = 0
    y: int = 0
    z: int = 0

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def translate(self, reference: 'Beacon') -> 'Beacon':
        return Beacon(
            reference.x - self.x,
            reference.y - self.y,
            reference.z - self.z
        )


def rotate_beacon_x(b: Beacon) -> Beacon:
    """Rotates beacon 90deg around x-axis"""
    return Beacon(b.x, -b.z, b.y)


def rotate_beacon_y(b: Beacon) -> Beacon:
    """Rotates beacon 90deg around y-axis"""
    return Beacon(b.z, b.y, -b.x)


def rotate_beacon_z(b: Beacon) -> Beacon:
    """Rotates beacon 90deg around z-axis"""
    return Beacon(-b.y, b.x, b.z)


def rotation_factory(rotations: str) -> Callable:
    """
    Take a sequnce of rotation axes and returns a function that performs
    those rotations.
    Possible rotations 'x', 'y', 'z'

    Usage: rotation_factory('xxyz')
        returns a function to rotate a beacon twice around x,
        once around y and once around z
    """
    rotation_map = {
        'x': rotate_beacon_x,
        'y': rotate_beacon_y,
        'z': rotate_beacon_z,
    }

    def compose(f, g):
        return lambda x: f(g(x))
    functions = [rotation_map[r] for r in rotations.lower()]
    return reduce(compose, functions, lambda x: x)


def all_rotations(b: Beacon) -> set[Beacon]:
    rotations = {b}
    for r in UNIQUE_ROTATIONS:
        rotations.add(rotation_factory(r)(b))
    return rotations


@dataclass
class Scanner:
    id: int
    beacons: set[Beacon]

    def rotations(self):
        pass


def mdistance(b0: Beacon, b1: Beacon) -> int:
    return abs(b0.x - b1.x) + abs(b0.y - b1.y) + abs(b0.z - b1.z)


def read_input(filepath: str) -> list[Scanner]:
    output = list()
    scanner = 0
    with open(filepath, 'r') as f:
        for line in (l.strip() for l in f.readlines()):
            if line.startswith("---"):
                beacons = set()
            elif line != '':
                point = [int(x) for x in line.split(',')]
                beacons.add(Beacon(point[0], point[1], point[2]))
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

    b = Beacon(1, 2, 3)
    pprint(all_rotations(b))
