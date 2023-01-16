import argparse
import sys
import traceback
from pathlib import Path

from downloader import download_input
from solutions import solve

parser = argparse.ArgumentParser(
    prog="aoc",
    description="Solutions for Advent of Code 2021",
)

parser.add_argument("day", type=int, help="Solution day to run, between 1 and 25.")
parser.add_argument(
    "filename",
    type=Path,
    nargs="?",
    help="Path to puzzle input file. Input will be downloaded if no path is given.",
)

args = parser.parse_args()

if __name__ == "__main__":
    try:
        filename = args.filename

        if filename is None:
            filename = download_input(args.day)

        if not filename.exists():
            raise FileNotFoundError("input file does not exist: '%s'" % args.filename)

        with args.filename.open() as f:
            input_ = f.read().splitlines()

        solution = solve(args.day, input_)
        print(solution)
    except FileNotFoundError as e:
        sys.stderr.write("aoc: error: %s\n" % e)
        sys.exit(1)
    except IndexError as e:
        sys.stderr.write("aoc: error: %s\n" % e)
        sys.exit(2)
    except Exception as e:
        sys.stderr.write("aoc: error: %s\n" % e)
        traceback.print_exc()
        sys.exit(3)
