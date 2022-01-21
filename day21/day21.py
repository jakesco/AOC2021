import argparse
import os

from collections import deque
from dataclasses import dataclass
from itertools import permutations

DIRAC = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}

ROLL_COMBOS = list(permutations(DIRAC.keys(), 2))

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


@dataclass(frozen=True)
class Game:
    p1_pos: int
    p2_pos: int
    p1_score: int = 0
    p2_score: int = 0
    universes: int = 0

    @property
    def winner(self) -> int:
        if self.p1_score >= 21:
            return 1
        if self.p2_score >= 21:
            return 2
        return 0


def roll(game: Game, p1_roll: int, p2_roll: int) -> Game:
    p1_pos = ((game.p1_pos - 1 + p1_roll) % 10) + 1
    p2_pos = ((game.p2_pos - 1 + p2_roll) % 10) + 1
    p1_score = game.p1_score + game.p1_pos
    p2_score = game.p2_score + game.p2_pos
    universes = game.universes + DIRAC[p1_roll] + DIRAC[p2_roll]
    return Game(p1_pos, p2_pos, p1_score, p2_score, universes)


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


def part1(p1: Player, p2: Player) -> int:
    die = Die()
    while True:
        p1.roll(die)
        if p1.winner():
            break
        p2.roll(die)
        if p2.winner():
            break
    loser = p1 if p2.winner() else p2
    return loser.points * die.rolls


def part2(p1: Player, p2: Player) -> dict[int, int]:
    wins = {1: 0, 2: 0}
    q = deque([Game(p1.position, p2.position)])

    while q:
        game = q.popleft()
        for p1_roll, p2_roll in ROLL_COMBOS:
            new_game = roll(game, p1_roll, p2_roll)
            if (w := new_game.winner) != 0:
                wins[w] += game.universes
            else:
                q.append(new_game)

    return wins


if __name__ == "__main__":
    path = init_parser()
    player1, player2 = read_input(path)

    print(f"Part 1: {part1(player1, player2)}")

    wins = part2(player1, player2)
    print(f"Part 2: p1={wins[1]}, p2={wins[2]}")
    # player1: 444356092776315
    # player2: 341960390180808
