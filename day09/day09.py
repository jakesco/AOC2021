import argparse
import os

from dataclasses import dataclass


@dataclass
class Node:
    pos: (int, int)
    val: int


class Map:
    def __init__(self, data: list[list[int]]):
        self.rows = len(data)
        self.cols = len(data[0])
        self.data = data

    def elm(self, row: int, col: int) -> int:
        try:
            if row < 0 or col < 0:
                raise IndexError
            return self.data[row][col]
        except IndexError:
            return 10

    def is_local_min(self, row: int, col: int) -> bool:
        val = self.elm(row, col)
        return (
                val < self.elm(row + 1, col)
                and val < self.elm(row - 1, col)
                and val < self.elm(row, col + 1)
                and val < self.elm(row, col - 1)
        )

    def get_local_mins(self) -> list[Node]:
        local_mins = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.is_local_min(i, j):
                    local_mins.append(Node((i, j), self.elm(i, j)))
        return local_mins

    def is_boundry(self, row: int, col: int):
        return self.elm(row, col) >= 9


def calculate_risk(map_: Map) -> int:
    local_mins = [map_.elm(c.pos[0], c.pos[1]) for c in map_.get_local_mins()]
    return sum(local_mins) + len(local_mins)


def basin_size(map_: Map, row: int, col: int) -> int:
    """Calculates the size of the basin, given one point in the basin."""
    if map_.is_boundry(row, col):
        return 0
    return (1
            + basin_size(map_, row - 1, col -1)
            + basin_size(map_, row - 1, col)
            + basin_size(map_, row - 1, col + 1)
            + basin_size(map_, row, col -1)
            + basin_size(map_, row, col)
            + basin_size(map_, row, col + 1)
            + basin_size(map_, row + 1, col -1)
            + basin_size(map_, row + 1, col)
            + basin_size(map_, row + 1, col + 1)
            )


def read_input(filepath: str):
    map_ = []
    with open(filepath, 'r') as f:
        for line in f.readlines():
            map_.append([int(n) for n in line.rstrip()])
    return Map(map_)


def init_parser() -> str:
    parser = argparse.ArgumentParser(description="Advent of Code day 2 solution.")
    parser.add_argument('input', metavar='FILE', type=str, nargs=1, help="Path to input data.")
    args = parser.parse_args()
    return os.path.realpath(args.input[0])


if __name__ == "__main__":
    path = init_parser()
    map_ = read_input(path)

    print(f"Part 1: risk = {calculate_risk(map_)}")

    basins = map_.get_local_mins()
    print(basins)



