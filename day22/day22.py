import argparse
import os

from itertools import product

class Grid:
    def __init__(self):
        self.__on_nodes = set()

    @property
    def cubes_on(self):
        return len(self.__on_nodes)

    def switch(self, x_range: range, y_range: range, z_range: range, on: bool = True):
        if any([
            x_range.start < -50, x_range.stop > 51,
            y_range.start < -50, y_range.stop > 51,
            z_range.start < -50, z_range.stop > 51
        ]):
            return
        if on:
            for node in product(x_range, y_range, z_range, repeat=1):
                self.__on_nodes.add(node)
        else:
            for node in product(x_range, y_range, z_range, repeat=1):
                self.__on_nodes.discard(node)


def make_range(input_: str) -> range:
    x = input_.split("=")[1]
    a, b = x.split("..")
    a = int(a)
    b = int(b)
    start = min(a, b)
    end = max(a, b)
    return range(int(start), int(end) + 1)


def read_input(filepath: str) -> list[str]:
    with open(filepath, 'r') as f:
        for line in f.readlines():
            on_off, ranges = line.strip().split()
            dims = ranges.split(",")
            x = make_range(dims[0])
            y = make_range(dims[1])
            z = make_range(dims[2])
            yield on_off, x, y, z



def init_parser() -> str:
    parser = argparse.ArgumentParser(description="Advent of Code day 17 solution.")
    parser.add_argument('input', metavar='FILE', type=str, nargs=1, help="Path to input data.")
    args = parser.parse_args()
    return os.path.realpath(args.input[0])


if __name__ == "__main__":
    path = init_parser()

    grid = Grid()

    for instruction, x, y, z in read_input(path):
        grid.switch(x, y, z, instruction == "on")
        print(f"Instruction Executed: {instruction} {x} {y} {z}")

    print(grid.cubes_on)
