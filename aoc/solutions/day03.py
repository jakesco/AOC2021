import argparse
import os

from functools import reduce


def frequency(input_: list[str]) -> list[int]:
    wordsize = len(input_[0])
    freq = [0] * wordsize

    for measure in input_:
        for i in range(wordsize):
            freq[i] += int(measure[i])

    return freq


def part1(input_) -> tuple[int, int]:
    freq = frequency(input_)

    threshold = len(input_) / 2

    gamma = ["1" if x >= threshold else "0" for x in freq]
    epsilon = ["0" if x >= threshold else "1" for x in freq]

    return (int("".join(gamma), 2), int("".join(epsilon), 2))


def filter(input_: list[str], filter_: list[str]) -> int:
    print(filter_)
    for i in range(len(filter_)):
        input_ = [x for x in input_ if x[i] == filter_[i]]
        print(input_)
        if len(input_) == 1:
            break
    return int(input_[0], 2)


def filter(input_: list[str], index: int, most: bool) -> list[str]:
    freq = 0
    for m in input_:
        freq += int(m[index])
    if most:
        filter_ = "1" if freq >= len(input_) / 2 else "0"
    else:
        filter_ = "0" if freq >= len(input_) / 2 else "1"
    return [x for x in input_ if x[index] == filter_]


def part2(input_) -> tuple[int, int]:
    wordsize = len(input_[0])

    o2 = input_.copy()
    for i in range(wordsize):
        o2 = filter(o2, i, True)
        if len(o2) == 1:
            break

    co2 = input_.copy()
    for i in range(wordsize):
        co2 = filter(co2, i, False)
        if len(co2) == 1:
            break

    return (int(o2[0], 2), int(co2[0], 2))


def read_input(filepath: str):
    with open(filepath, "r") as f:
        return [line.rstrip("\n") for line in f.readlines()]


def init_parser() -> str:
    parser = argparse.ArgumentParser(description="Advent of Code day 3 solution.")
    parser.add_argument(
        "input", metavar="FILE", type=str, nargs=1, help="Path to input data."
    )
    args = parser.parse_args()
    return os.path.realpath(args.input[0])


if __name__ == "__main__":
    path = init_parser()

    input_ = read_input(path)

    rates = part1(input_)

    print(f"Part 1:")
    print(f"γ: {rates[0]} - 22")
    print(f"ε: {rates[1]} - 9")
    print(f"Power Consumption: {rates[0] * rates[1]} - 198")

    lf = part2(input_)

    print(f"\nPart 2:")
    print(f"O2: {lf[0]} - 23")
    print(f"CO2: {lf[1]} - 10")
    print(f"Life Support: {lf[0] * lf[1]} - 230")

def main(_): raise NotImplementedError
