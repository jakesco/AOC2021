import argparse
import os

from math import sqrt, trunc
from itertools import combinations, permutations
from functools import reduce


from dataclasses import dataclass


ROOT_2_OVER_2 = sqrt(2) / 2


@dataclass(frozen=True)
class Q:
    w: float
    x: float
    y: float
    z: float

    def __repr__(self):
        return f"Q({trunc(self.w)}, {trunc(self.x)}, {trunc(self.y)}, {trunc(self.z)})"

    @property
    def mag(self) -> float:
        return sqrt(
            reduce(lambda x, y: x + y ** 2, self.__dict__.values(), 0)
        )

    def inv(self) -> 'Q':
        return Q(self.w, -self.x, -self.y, -self.z)

    def add(self, other: 'Q') -> 'Q':
        return Q(
            self.w + other.w,
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )

    def sub(self, other: 'Q') -> 'Q':
        return Q(
            self.w - other.w,
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
            )

    def mul(self, other: 'Q') -> 'Q':
        """Hamilton product"""
        return Q(
            self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z,
            self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y,
            self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x,
            self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w,
        )

    def rot(self, rotation: 'Q') -> 'Q':
        return rotation.mul(self).mul(rotation.inv())


@dataclass(frozen=True)
class Scanner:
    id: int
    beacons: set[Q]

    @property
    def distances(self) -> dict[tuple[Q], float]:
        """Calculates the distances of all the beacons from each other."""
        return {(a, b): a.distance(b) for a, b in combinations(self.beacons, 2)}


def centroid(beacons: set[Q]) -> Q:
    """Calculates the centroid of beacons."""
    return reduce(lambda x, y: x.add(y), beacons).div(len(beacons))


def translation(s0: Scanner, s1: Scanner) -> Q | None:
    """
    Returns a translation vector to move scanner 0 to scanner 1.
    This requires at least 12 beacons are known to overlap.
    """
    x = centroid(s0.beacons)
    y = centroid(s1.beacons)
    return x.sub(y)

def rotation(s0: Scanner, s1: Scanner) -> Q:
    """
    Returns a rotation matrix to align scanner 0 to scanner 1.
    This requires at least 12 beacons are known to overlap.
    """
    pass


def generate_rotations() -> set[Q]:
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
                beacons.add(Q(0, int(point[0]), int(point[1]), int(point[2])))
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

    ROT_90 = Q(ROOT_2_OVER_2, ROOT_2_OVER_2, 0, 0)

    for beacon in origin.beacons:
        print(f"Original: {beacon}")
        print(f"Rotate (90, 0, 0): {beacon.rot(ROT_90)}")

