import argparse
import os
from collections import deque


def read_input(filepath: str):
    with open(filepath, 'r') as f:
        while line := f.readline():
            try:
                yield int(line)
            except ValueError:
                yield -1


def count_increases(filepath: str, window: int):
    deck = deque(maxlen=window)
    first = True
    count = 0
    prev = 0

    for n in read_input(filepath):
        deck.append(n)
        if len(deck) < window:
            continue
        total = sum(deck)
        if first:
            prev = total
            first = False
            continue
        if total > prev:
            count += 1
        prev = total
    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code day 1 solution.")
    parser.add_argument('input', metavar='FILE', type=str, nargs=1, help="Path to input data.")
    args = parser.parse_args()

    filepath = os.path.realpath(args.input[0])

    print(f"Part 1: {count_increases(filepath, 1)}")
    print(f"Part 2: {count_increases(filepath, 3)}")
