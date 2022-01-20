import argparse
import os

from collections.abc import Callable
from collections import deque, Counter
from dataclasses import dataclass
from functools import reduce, cache
from pprint import pprint

from itertools import combinations


UNIQUE_ROTATIONS = (
    'I', 'X', 'Y', 'Z', 'XX', 'XY', 'XZ', 'YX', 'YY', 'ZY',
    'ZZ', 'XXX', 'XXY', 'XXZ', 'XYX', 'XYY', 'XZZ', 'YXX',
    'YYY', 'ZZZ', 'XXXY', 'XXYX', 'XYXX', 'XYYY'
)

@cache
def rotation_factory(rotations: str) -> Callable:
    """
    Take a sequence of rotation axes and returns a function that performs
    those rotations.
    Possible rotations 'x', 'y', 'z'

    Usage: rotation_factory('xxyz')
        returns a function to rotate a beacon twice around x,
        once around y and once around z
    """
    rotation_map = {
        'i': lambda b: b,
        'x': lambda b: Beacon(b.x, -b.z, b.y),
        'y': lambda b: Beacon(b.z, b.y, -b.x),
        'z': lambda b: Beacon(-b.y, b.x, b.z),
    }

    def compose(f, g):
        return lambda x: f(g(x))
    functions = [rotation_map[r] for r in rotations.lower()]
    return reduce(compose, functions, lambda b: b)


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

    def add(self, other: 'Beacon') -> 'Beacon':
        return Beacon(self.x + other.x, self.y + other.y, self.z + other.z)

    def sub(self, other: 'Beacon') -> 'Beacon':
        return Beacon(self.x - other.x, self.y - other.y, self.z - other.z)


@dataclass(frozen=True)
class Orientation:
    rotation: str = ''
    translation: Beacon = Beacon()

    def __repr__(self):
        return f"O(r={self.rotation}, t={self.translation}"


@dataclass
class Scanner:
    id: int
    beacons: set[Beacon]
    match: 'Scanner' = None
    orientation: Orientation = Orientation()

    def __repr__(self):
        return f"Scanner(id={self.id}, match={self.match.id if self.match else 'None'}, o={self.orientation})"

    def rotate(self, rotations: str) -> set[Beacon]:
        return {rotation_factory(rotations)(b) for b in self.beacons}

    def apply_orientation(self, o: Orientation = None) -> set[Beacon]:
        orientation = o if o is not None else self.orientation
        rotated = self.rotate(orientation.rotation)
        translated = {b.add(orientation.translation) for b in rotated}
        return translated

    def distance_signature(self) -> dict[int, (Beacon, Beacon)]:
        self.relative_beacons = self.beacons.copy()
        sig = dict()
        for b in self.beacons:
            for a in self.beacons:
                sig[mdistance(b, a)] = (b, a)
        return sig


def mdistance(b0: Beacon, b1: Beacon) -> int:
    return abs(b0.x - b1.x) + abs(b0.y - b1.y) + abs(b0.z - b1.z)


def mdistance_between_scanners(s0: Scanner, s1: Scanner) -> int:
    b0 = s0.orientation.translation
    b1 = s1.orientation.translation
    return mdistance(b0, b1)


def transform_beacons(beacons: set[Beacon], orientation: Orientation) -> set[Beacon]:
    return {rotation_factory(orientation.rotation)(b).add(orientation.translation) for b in beacons}


def match_overlaping_scanner(scanners: list[Scanner]):
    q = deque(scanners)
    origin = q.popleft()
    locked = [origin]
    while q:
        found = False
        s = q.popleft()
        signature = s.distance_signature()
        for scanner in locked:
            s1dist = scanner.distance_signature()
            overlap = set(s1dist).intersection(set(signature))
            if len(overlap) < 66:
                continue
            locked.append(s)
            s.match = scanner
            found = True
            break
        if not found:
            q.append(s)


def best_translation(b0: set[Beacon], b1: set[Beacon]) -> (Beacon, int):
    c = Counter()
    for x in b1:
        for y in b0:
            t = x.translate(y)
            c[t] += 1
    return c.most_common(1)[0]


def match_scanners(s: Scanner):
    if s.match is None:
        return

    c = Counter()
    for rotation in UNIQUE_ROTATIONS:
        r = s.rotate(rotation)
        t = best_translation(s.match.beacons, r)
        if t[1] >= 12:
            s.orientation = Orientation(rotation, t[0])


def scanner_to_origin(s: Scanner) -> set[Beacon]:
    beacons = transform_beacons(s.beacons, s.orientation)
    next_ = s.match
    while next_:
        if next_.match is None:
            break
        beacons = transform_beacons(beacons, next_.orientation)
        next_ = next_.match
    return beacons


def calculate_absolute_position(s: Scanner) -> Beacon:
    return Beacon()


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

    match_overlaping_scanner(scanners)
    [match_scanners(s) for s in scanners]

    pprint(scanners)

    unique = reduce(lambda a, b: a.union(b), [scanner_to_origin(s) for s in scanners], set())
    print(f"Part 1: {len(unique)}(79)")

    for x, y in combinations(scanners, 2):
        print(f"{x.id} to {y.id}: {mdistance_between_scanners(x, y)}")













