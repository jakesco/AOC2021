from __future__ import annotations
import argparse
import os


def read_input(filepath: str) -> (int, int):
    with open(filepath, 'r') as f:
        for line in f.readlines():
            segments, digits = line.split('|')
            yield segments.split(), digits.split()


def init_parser() -> str:
    parser = argparse.ArgumentParser(description="Advent of Code day 2 solution.")
    parser.add_argument('input', metavar='FILE', type=str, nargs=1, help="Path to input data.")
    args = parser.parse_args()
    return os.path.realpath(args.input[0])


def count_easy_digits(digits: list[str]) -> int:
    count = 0
    for d in digits:
        if len(d) in (2, 3, 4, 7):
            count += 1
    return count


if __name__ == "__main__":
    path = init_parser()
    input_ = read_input(path)

    count = 0
    for _, digits in input_:
        count += count_easy_digits(digits)

    print(f"Count of 1, 4, 7, 8: {count}")



