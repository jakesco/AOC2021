import argparse
import os
from pprint import pprint


class Board:
    def __init__(self, numbers: list[int]):
        self.numbers = numbers
        self.marked = [False] * len(numbers)
        self.width = 5
        self.win = False

    def mark(self, number: int):
        try:
            self.marked[self.numbers.index(number)] = True
        except ValueError:
            pass

    def check_horizontal(self):
        for row in range(5):
            pos = row * self.width
            if all(self.marked[pos : pos + self.width]):
                return True
        return False

    def check_vertical(self):
        for col in range(5):
            if all(
                [
                    self.marked[col],
                    self.marked[col + 5],
                    self.marked[col + 10],
                    self.marked[col + 15],
                    self.marked[col + 20],
                ]
            ):
                return True
        return False

    def check_win(self):
        self.win = self.check_horizontal() or self.check_vertical()
        return self.win

    def score(self, last_num: int):
        both = zip(self.numbers, self.marked)
        unmarked = [int(n) for n, m in both if not m]
        return sum(unmarked) * int(last_num)

    def __str__(self):
        output = []
        i = 0
        for n in self.numbers:
            if i % 5 == 0:
                output.append("\n")
            output.append(str(n))
            i += 1

        i = 0
        for m in self.marked:
            if i % 5 == 0:
                output.append("\n")
            output.append("x" if m else "o")
            i += 1
        return " ".join(output)

    def __repr__(self):
        return f"Board({self.numbers}, {self.marked})"


def read_input(filepath: str) -> (list[int], list[Board]):
    with open(filepath, "r") as f:
        deck = f.readline().rstrip("\n").split(",")
        boards = []

        f.readline()

        acc = []
        while line := f.readline():
            l = line.split()
            if l:
                acc = acc + l
            else:
                boards.append(Board(acc))
                acc = []
        boards.append(Board(acc))

    return (deck, boards)


def init_parser() -> str:
    parser = argparse.ArgumentParser(description="Advent of Code day 4 solution.")
    parser.add_argument(
        "input", metavar="FILE", type=str, nargs=1, help="Path to input data."
    )
    args = parser.parse_args()
    return os.path.realpath(args.input[0])


if __name__ == "__main__":
    path = init_parser()

    deck, boards = read_input(path)

    for n in deck:
        print(f"Call: {n}")
        for b in boards:
            b.mark(n)
            print(b)
            b.check_win()
            if all([w.win for w in boards]):
                print(f"Win: {b.score(n)}")
                exit()


def main(_):
    raise NotImplementedError
