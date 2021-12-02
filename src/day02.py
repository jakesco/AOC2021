import argparse
import os


def read_input(filepath: str):
    with open(filepath, 'r') as f:
        yield from f.read().splitlines()


def do_the_thing(filepath: str):
    pass


def init_parser() -> str:
    parser = argparse.ArgumentParser(description="Advent of Code day 2 solution.")
    parser.add_argument('input', metavar='FILE', type=str, nargs=1, help="Path to input data.")
    args = parser.parse_args()
    return os.path.realpath(args.input[0])


if __name__ == "__main__":
    path = init_parser()
    data = read_input(path)
    print(list(data))
