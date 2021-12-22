import argparse
import os

from math import floor, ceil

from abc import ABC, abstractmethod

from dataclasses import dataclass


def read_input(filepath: str):
    with open(filepath, 'r') as f:
        return f.read()


def init_parser() -> str:
    parser = argparse.ArgumentParser(description="Advent of Code day 17 solution.")
    parser.add_argument('input', metavar='FILE', type=str, nargs=1, help="Path to input data.")
    args = parser.parse_args()
    return os.path.realpath(args.input[0])


class Element(ABC):

    @abstractmethod
    def _literals(self, acc) -> list['Literal']:
        pass

    @abstractmethod
    def split(self):
        pass

    @abstractmethod
    def can_explode(self) -> bool:
        pass


@dataclass
class SnailFishNumber(Element):
    l: Element
    r: Element

    def __repr__(self):
        return f"[{self.l}, {self.r}]"

    def _literals(self, acc):
        self.l._literals(acc)
        self.r._literals(acc)

    def add(self, other: Element) -> 'SnailFishNumber':
        result = SnailFishNumber(self, other)
        print(f"{self} + {other}")
        print(f"= {result}", end="\n\n")
        return SnailFishNumber(self, other)

    def reduce(self):
        """Reduces Snailfish number."""
        pass

    def apply_explode(self, value: tuple[int, int]):
        literals = get_literals(self)
        idx = literals.index(Literal(-1))
        if idx - 1 >= 0:
            literals[idx - 1].add(value[0])
        if idx + 1 < len(literals):
            literals[idx + 1].add(value[1])
        literals[idx].add(1)

    def explode(self, depth) -> tuple[int, int] | None:
        """
            Explodes left most explodeable value, returns (left,right) tuple
            if explode happened else None. (left,right) tuple must be applied
            via self.apply_explode before explode is complete.
        """
        # If a pair is nested in 4 pairs, the left pair explodes
        if depth >= 3 and self.l.can_explode():
            left = self.l.l.value
            right = self.l.r.value
            self.l = Literal(-1)
            return (left, right)
        elif depth >= 3 and self.r.can_explode():
            left = self.r.l.value
            right = self.r.r.value
            self.r = Literal(-1)
            return (left, right)
        if isinstance(self.l, SnailFishNumber):
            if done := self.l.explode(depth + 1):
                return done
        if isinstance(self.r, SnailFishNumber):
            if done := self.r.explode(depth + 1):
                return done
        return None

    def can_explode(self) -> bool:
        return isinstance(self.l, Literal) and isinstance(self.r, Literal)

    def split(self) -> bool:
        """Splits left most splittable value, returns True if split was made."""
        if isinstance(self.l, SnailFishNumber):
            if done := self.l.split():
                return done
        if isinstance(self.r, SnailFishNumber):
            if done := self.r.split():
                return done
        if isinstance(self.l, Literal) and self.l.value >= 10:
            self.l = self.l.split()
            return True
        if isinstance(self.r, Literal) and self.r.value >= 10:
            self.r = self.r.split()
            return True
        return False


@dataclass
class Literal(Element):
    value: int

    def __repr__(self):
        return str(self.value)

    def _literals(self, acc):
        acc.append(self)

    def can_explode(self) -> bool:
        return False

    def add(self, val: int):
        self.value += val

    def split(self) -> Element:
        if self.value < 10:
            return self
        half = self.value / 2
        left = floor(half)
        right = ceil(half)
        return SnailFishNumber(Literal(left), Literal(right))


def get_literals(s: SnailFishNumber) -> list[Literal]:
    acc = []
    s._literals(acc)
    return acc


if __name__ == "__main__":
    path = init_parser()
    # input_ = read_input(path)
    # print(input_)

    # [[[[[9, 8], 1], 2], 3], 4] => [[[[0,9],2],3],4]
    a = SnailFishNumber(
        SnailFishNumber(
            SnailFishNumber(
                SnailFishNumber(
                    SnailFishNumber(
                        Literal(9),
                        Literal(8)
                    ),
                    Literal(1)
                ),
                Literal(2)
            ), Literal(3)
        ), Literal(4)
    )

    # [7, [6, [5, [4, [3, 2]]]]] => [7,[6,[5,[7,0]]]]
    b = SnailFishNumber(
        Literal(7),
        SnailFishNumber(
            Literal(6),
            SnailFishNumber(
                Literal(5),
                SnailFishNumber(
                    Literal(4),
                    SnailFishNumber(
                        Literal(3),
                        Literal(2)
                    )
                )
            )
        )
    )

    # [[6, [5, [4, [3, 2]]]], 1] => [[6,[5,[7,0]]],3]
    c = SnailFishNumber(
        SnailFishNumber(
            Literal(6),
            SnailFishNumber(
                Literal(5),
                SnailFishNumber(
                    Literal(4),
                    SnailFishNumber(
                        Literal(3),
                        Literal(2)
                    )
                )
            )
        ),
        Literal(1)
    )

    # [[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]]
    # => [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]
    # => [[3, [2, [8, 0]]], [9, [5, [7, 0]]]]
    d = SnailFishNumber(
        SnailFishNumber(
            Literal(3),
            SnailFishNumber(
                Literal(2),
                SnailFishNumber(
                    Literal(1),
                    SnailFishNumber(
                        Literal(7),
                        Literal(3)
                    )
                )
            )
        ),
        SnailFishNumber(
            Literal(6),
            SnailFishNumber(
                Literal(5),
                SnailFishNumber(
                    Literal(4),
                    SnailFishNumber(
                        Literal(3),
                        Literal(2)
                    )
                )
            )
        )
    )

    for sn in (a, b, c):
        print(sn, end='')
        apply = sn.explode(0)
        sn.apply_explode(apply)
        print(f' => {sn}')

    print(d)
    apply = d.explode(0)
    if apply is not None:
        d.apply_explode(apply)
    print(f' => {d}')
    apply = d.explode(0)
    if apply is not None:
        d.apply_explode(apply)
    print(f' => {d}')




