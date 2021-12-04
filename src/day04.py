import argparse
import os

class Board:
    pass

def mark(board, number):
    pass

def check_horizontal(board):
    pass


def check_vertical(board):
    pass

def check_win(board):
    pass

def calculate_score(board):
    pass

def read_input(filepath: str):
    with open(filepath, 'r') as f:
        return [line.rstrip('\n') for line in f.readlines()]


def init_parser() -> str:
    parser = argparse.ArgumentParser(description="Advent of Code day 2 solution.")
    parser.add_argument('input', metavar='FILE', type=str, nargs=1, help="Path to input data.")
    args = parser.parse_args()
    return os.path.realpath(args.input[0])


if __name__ == "__main__":
    path = init_parser()

    input_ = read_input(path)

    print(input_)

