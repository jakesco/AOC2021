import argparse
import os

from collections import Counter

def split_template(template: str) -> list[str]:
    return [
        template[i: i + 2]
        for i in range(len(template) - 1)
    ]


def apply_rules(template: str, rules: dict[str, str]) -> str:
    pairs = split_template(template)

    for i in range(len(pairs)):
        pair = pairs[i]
        pair = pair[0] + rules[pair] + pair[1]
        pairs[i] = pair

    new_template = [pair[:-1] for pair in pairs]
    new_template.append(template[-1])

    return ''.join(new_template)


def template_score(template: str) -> int:
    c = Counter(template)
    common = c.most_common()
    most = common[0][1]
    least = common[-1][1]
    return most - least


def read_input(filepath: str) -> (str, dict[str, str]):
    rules = dict()
    with open(filepath, 'r') as f:
        template = f.readline().rstrip()
        f.readline()
        for line in f.readlines():
            data = line.split('->')
            rules[data[0].strip()] = data[1].strip()
    return template, rules


def init_parser() -> str:
    parser = argparse.ArgumentParser(description="Advent of Code day 2 solution.")
    parser.add_argument('input', metavar='FILE', type=str, nargs=1, help="Path to input data.")
    args = parser.parse_args()
    return os.path.realpath(args.input[0])


if __name__ == "__main__":
    path = init_parser()
    template, rules = read_input(path)
    steps = 40
    for i in range(steps):
        print(i)
        template = apply_rules(template, rules)
    print(f"Part 1: {template_score(template)}")

