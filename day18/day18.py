import argparse
import os

from dataclasses import dataclass


def read_input(filepath: str):
    with open(filepath, 'r') as f:
        return f.read()


def init_parser() -> str:
    parser = argparse.ArgumentParser(description="Advent of Code day 17 solution.")
    parser.add_argument('input', metavar='FILE', type=str, nargs=1, help="Path to input data.")
    args = parser.parse_args()
    return os.path.realpath(args.input[0])


class Element:
    pass


@dataclass(frozen=True)
class Literal(Element):
    value: int

    def __repr__(self):
        return str(self.value)


@dataclass(frozen=True)
class SnailFishNumber(Element):
    l: Element
    r: Element

    def __repr__(self):
        return f"[{self.l}, {self.r}]"

    def add(self, other: Element) -> Element:
        result = SnailFishNumber(self, other)
        print(f"{self} + {other}")
        print(f"= {result}", end="\n\n")
        return SnailFishNumber(self, other)


if __name__ == "__main__":
    path = init_parser()
    # input_ = read_input(path)
    # print(input_)

    a = Literal(1)
    b = Literal(2)
    c = Literal(3)
    d = Literal(4)
    e = Literal(5)

    x = SnailFishNumber(a, b)
    y = SnailFishNumber(c, d)
    z = SnailFishNumber(y, e)

    x.add(z)


