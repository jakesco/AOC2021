import argparse
import os

from math import sqrt, trunc
from decimal import Decimal
from itertools import combinations, permutations
from functools import reduce
from collections import Counter


from dataclasses import dataclass

from pprint import pprint


PRECISION = Decimal('1.00')


@dataclass(frozen=True)
class Q:
    w: Decimal
    x: Decimal
    y: Decimal
    z: Decimal

    def __repr__(self):
        return f"Q({self.w}, {self.x}, {self.y}, {self.z})"

    @staticmethod
    def from_tuple(t: tuple):
        return Q(
            Decimal(t[0]),
            Decimal(t[1]),
            Decimal(t[2]),
            Decimal(t[3]),
        )

    @property
    def mag(self) -> Decimal:
        return reduce(lambda x, y: x + y ** 2, self.__dict__.values(), Decimal(0)).sqrt()

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

    def div(self, scalar: Decimal) -> 'Q':
        return Q(
            self.w / scalar,
            self.x / scalar,
            self.y / scalar,
            self.z / scalar,
            )

    def mul(self, other: 'Q') -> 'Q':
        """Hamilton product"""
        return Q(
            self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z,
            self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y,
            self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x,
            self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w,
        )

    def apply_rotation(self, rotation: 'Q') -> 'Q':
        return rotation.mul(self).mul(rotation.inv()).quantize(PRECISION)

    def quantize(self, *args, **kwargs) -> 'Q':
        return Q(
            self.w.quantize(*args, **kwargs),
            self.x.quantize(*args, **kwargs),
            self.y.quantize(*args, **kwargs),
            self.z.quantize(*args, **kwargs),
        )

    def normalize(self) -> 'Q':
        mag = self.mag
        return Q(
            self.w / mag,
            self.x / mag,
            self.y / mag,
            self.z / mag,
            )

    def distance(self, other: 'Q') -> Decimal:
        dx = other.x - self.x
        dy = other.y - self.y
        dz = other.z - self.z
        return (dx ** 2 + dy ** 2 + dz ** 2).sqrt()


@dataclass(frozen=True)
class Orientation:
    translation: Q = Q.from_tuple((0, 0, 0, 0))
    rotation: Q = Q.from_tuple((0, 0, 0, 0))


@dataclass(frozen=True)
class Scanner:
    id: int
    beacons: set[Q]

    @property
    def distances(self) -> set[Decimal]:
        """Calculates the distances of all the beacons from each other."""
        return {a.distance(b) for a, b in combinations(self.beacons, 2)}


def centroid(beacons: set[Q]) -> Q:
    """Calculates the centroid of beacons."""
    return reduce(lambda x, y: x.add(y), beacons).div(Decimal(len(beacons)))


def rotate(beacons: set[Q], rotation: Q) -> set[Q]:
    return {b.apply_rotation(rotation) for b in beacons}


def translate(beacons: set[Q], translation: Q) -> set[Q]:
    return {b.add(translation) for b in beacons}


def transform(beacons: set[Q], orientation: Orientation) -> set[Q]:
    return translate(rotate(beacons, orientation.rotation), orientation.translation)


def cal_translation(q0: Q, q1: Q) -> Q:
    return q0.sub(q1)


def find_best_match(scanner: Scanner, scanners: list[Scanner]) -> int:
    """Returns index of best matching scanner."""
    dist1 = scanner.distances
    best = (scanner.id, 0)
    for s in scanners:
        if s == scanner:
            continue

        dist2 = s.distances
        common = len(dist1.intersection(dist2))
        if common > best[1]:
            best = (s.id, common)
    return best[0]


def find_orientation(scanner0: Scanner, scanner1: Scanner) -> Orientation:
    best_transform = ("", 0, Orientation())
    for label, rot in UNIQUE_ROTATIONS.items():
        r = rotate(scanner0.beacons, rot)
        c = Counter()
        for beacon in r:
            c += Counter([cal_translation(o, beacon) for o in scanner1.beacons])
        most_common = c.most_common(1)[0]
        if most_common[1] > best_transform[1]:
            best_transform = (label, most_common[1], Orientation(most_common[0], rot))
    return best_transform[2]


def deduplicate_beacons(scanners: list[Scanner]) -> set[Q]:
    overlap_map = dict()
    for scanner in scanners[1:]:
        overlap_map[scanner.id] = find_best_match(scanner, scanners)

    transform_map = dict()
    for scanner in scanners[1:]:
        transform_map[scanner.id] = find_orientation(scanner, scanners[overlap_map[scanner.id]])

    pprint(overlap_map)

    new_sets = [origin.beacons]
    for scanner in scanners[1:]:
        t = transform(scanner.beacons, transform_map[scanner.id])
        next = overlap_map[scanner.id]
        while next != 0:
            t = transform(t, transform_map[next])
            next = overlap_map[next]
        new_sets.append(t)

    unique_beacons = reduce(lambda a, b: a.union(b), new_sets)

    return unique_beacons


def read_input(filepath: str) -> list[Scanner]:
    output = list()
    scanner = 0
    with open(filepath, 'r') as f:
        for line in (l.strip() for l in f.readlines()):
            if line.startswith("---"):
                beacons = set()
            elif line != '':
                point = line.split(',')
                beacons.add(Q.from_tuple((0, float(point[0]), float(point[1]), float(point[2]))).quantize(PRECISION))
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
    ROOT_2_OVER_2 = Decimal(2).sqrt() / 2
    X_90 = Q.from_tuple((ROOT_2_OVER_2, ROOT_2_OVER_2, 0, 0))
    Y_90 = Q.from_tuple((ROOT_2_OVER_2, 0, ROOT_2_OVER_2, 0))
    Z_90 = Q.from_tuple((ROOT_2_OVER_2, 0, 0, ROOT_2_OVER_2))
    UNIQUE_ROTATIONS = {
        'I': Q.from_tuple((1, 0, 0, 0)),
        'X': X_90,
        'Y': Y_90,
        'Z': Z_90,
        'XX': X_90.mul(X_90),
        'XY': X_90.mul(Y_90),
        'XZ': X_90.mul(Z_90),
        'YX': Y_90.mul(X_90),
        'YY': Y_90.mul(Y_90),
        'ZY': Z_90.mul(Y_90),
        'ZZ': Z_90.mul(Z_90),
        'XXX': X_90.mul(X_90).mul(X_90),
        'XXY': X_90.mul(X_90).mul(Y_90),
        'XXZ': X_90.mul(X_90).mul(Z_90),
        'XYX': X_90.mul(Y_90).mul(X_90),
        'XYY': X_90.mul(Y_90).mul(Y_90),
        'XZZ': X_90.mul(Z_90).mul(Z_90),
        'YXX': Y_90.mul(X_90).mul(X_90),
        'YYY': Y_90.mul(Y_90).mul(Y_90),
        'ZZZ': Z_90.mul(Z_90).mul(Z_90),
        'XXXY': X_90.mul(X_90).mul(X_90).mul(Y_90),
        'XXYX': X_90.mul(X_90).mul(Y_90).mul(X_90),
        'XYXX': X_90.mul(Y_90).mul(X_90).mul(X_90),
        'XYYY': X_90.mul(Y_90).mul(Y_90).mul(Y_90),
    }

    path = init_parser()
    scanners = read_input(path)
    origin = scanners[0]
    scanner = scanners[1]

    unique_beacons = deduplicate_beacons(scanners)

    print(f"Part 1: {len(unique_beacons)}")




