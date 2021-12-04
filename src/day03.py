import argparse
import os

from functools import reduce


def generate_counter(word_size: int) -> dict[int, int]:
    counter = dict()
    for i in range(word_size):
        counter[i] = 0
    return counter


def count_ones(counter: dict[int, int], word: str):
    for i in counter.keys():
        counter[i] += int(word[i])



def calculate_rates(input_) -> tuple[int, int]:
    first_line = input_.__next__()

    total = 0
    counter = generate_counter(len(first_line))

    count_ones(counter, first_line)
    for line in input_:
        count_ones(counter, line)
        total += 1

    threshold = total / 2

    freq = [('1', '0') if x >= threshold else ('0', '1') for x in counter.values()]

    gamma = int(''.join([a for a, _ in freq]), 2)
    epsilon = int(''.join([b for _, b in freq]), 2)


    return (gamma, epsilon)


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

    input_ = read_input(path)

    rates = calculate_rates(input_)

    print(f"γ: {rates[0]}")
    print(f"ε: {rates[1]}")
    print(f"Power Consumption: {rates[0] * rates[1]}")


