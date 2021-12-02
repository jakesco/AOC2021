import argparse
import os

from dataclasses import dataclass


@dataclass
class Move:
    direction: str
    distance: int

    @staticmethod
    def from_input(input: str):
        dir_, dist = input.split(' ')
        return Move(dir_, int(dist))


@dataclass
class Position:
    distance: int = 0
    depth: int = 0
    aim: int = 0

    def product(self):
        return self.distance * self.depth

    def move(self, movement: Move):
        # Dataclass automatically provides __match_args__
        match movement:
            case Move('forward', distance):
                self.distance += distance
                self.depth += self.aim * distance
            case Move('up', distance):
                self.aim -= distance
            case Move('down', distance):
                self.aim += distance


def read_input(filepath: str):
    with open(filepath, 'r') as f:
        yield from (line.rstrip('\n') for line in f.readlines())


def init_parser() -> str:
    parser = argparse.ArgumentParser(description="Advent of Code day 2 solution.")
    parser.add_argument('input', metavar='FILE', type=str, nargs=1, help="Path to input data.")
    args = parser.parse_args()
    return os.path.realpath(args.input[0])


if __name__ == "__main__":
    path = init_parser()

    movements = [Move.from_input(x) for x in read_input(path)]

    position = Position()
    for m in movements:
        position.move(m)

    print(f"Position: {position.distance}")
    print(f"Depth: {position.depth}")
    print(f"Answer: {position.product()}")
