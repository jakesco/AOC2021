from collections import deque


def read_input(filepath: str):
    with open(filepath, 'r') as f:
        while line := f.readline():
            try:
                yield int(line)
            except ValueError:
                yield -1


def part1(filepath: str):
    count = 0
    with open(filepath, "r") as f:
        prev = int(f.readline())
        for n in f.readlines():
            num = int(n)
            if num > prev:
                count += 1
            prev = num
    return count


def part2(filepath: str):
    deck = deque(maxlen=3)
    first = True
    count = 0
    prev = 0

    for n in read_input(filepath):
        deck.append(n)
        if len(deck) < 3:
            continue
        window = sum(deck)
        if first:
            prev = window
            first = False
            continue
        if window > prev:
            count += 1
        prev = window
    return count


if __name__ == "__main__":
    # print(f"Part 1: {part1()}")
    print(f"Part 2: {part2('./input1.txt')}")
