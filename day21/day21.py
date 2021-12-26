import argparse
import os

from collections import deque
from dataclasses import dataclass


class Die:
    def __init__(self):
        self.__gen = deque(range(1, 101))
        self.__rolls = 0

    @property
    def rolls(self) -> int:
        return self.__rolls

    def roll(self):
        self.__rolls += 1
        if len(self.__gen) <= 0:
            self.__gen = deque(range(1, 101))
        return self.__gen.popleft()


@dataclass
class Player:
    position: int
    points: int = 0

    def roll(self, die: Die):
        move = 0
        for i in range(3):
            move += die.roll()
        self.position = ((self.position - 1 + move) % 10) + 1
        self.points += self.position

    def winner(self) -> bool:
        return self.points >= 1000


def read_input(filepath: str) -> (Player, Player):
    with open(filepath, 'r') as f:
        start1 = int(f.readline().split(':')[1].strip())
        start2 = int(f.readline().split(':')[1].strip())
    return Player(start1), Player(start2)


def init_parser() -> str:
    parser = argparse.ArgumentParser(description="Advent of Code day 21 solution.")
    parser.add_argument('input', metavar='FILE', type=str, nargs=1, help="Path to input data.")
    args = parser.parse_args()
    return os.path.realpath(args.input[0])


if __name__ == "__main__":
    path = init_parser()
    player1, player2 = read_input(path)

    die = Die()

    while True:
        player1.roll(die)
        if player1.winner():
            break
        player2.roll(die)
        if player2.winner():
            break

    loser = player1 if player2.winner() else player2
    print(f"Part 1: {loser.points * die.rolls}")