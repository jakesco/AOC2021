import argparse
import os

from math import sqrt, trunc
from decimal import Decimal
from itertools import combinations, permutations
from functools import reduce
from collections import Counter


from dataclasses import dataclass


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
    return reduce(lambda x, y: x.add(y), beacons).div(Decimal(len(beacons)))


def rotate(beacons: set[Q], rotation: Q) -> set[Q]:
    return {b.apply_rotation(rotation) for b in beacons}


def translate(beacons: set[Q], translation: Q) -> set[Q]:
    return {b.add(translation) for b in beacons}


def cal_translation(q0: Q, q1: Q) -> Q:
    return q0.sub(q1)


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

    # Test 4, 10 beacons
    orientations = dict()
    for scanner in scanners:
        best = ("", 0, Q.from_tuple((0, 0, 0, 0)), Q.from_tuple((0, 0, 0, 0)))
        for label, rot in UNIQUE_ROTATIONS.items():
            r = rotate(scanner.beacons, rot)
            c = Counter()
            for beacon in r:
                c += Counter([cal_translation(o, beacon) for o in origin.beacons])
            most_common = c.most_common(1)[0]
            if most_common[1] > best[1]:
                best = (label, most_common[1], rot, most_common[0])
        orientations[scanner.id] = (best[2], best[3])

    new_sets = [origin.beacons]
    for scanner in scanners[1:]:
        transform = orientations[scanner.id]
        new_sets.append(translate(rotate(scanner.beacons, transform[0]), transform[1]))

    unique_beacons = reduce(lambda a, b: a.union(b), new_sets)

    print(len(unique_beacons))




