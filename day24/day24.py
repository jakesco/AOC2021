import argparse
import os

from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class Instruction:
    op: str
    a: str
    b: str | int

    @staticmethod
    def from_str(line: str) -> 'Instruction':
        line = line.split()
        if len(line) == 2:
            return Instruction(line[0], line[1], '')

        try:
            b = int(line[-1])
        except ValueError:
            b = line[-1]
        return Instruction(line[0], line[1], b)


class ALU:
    def __init__(self):
        self.registers: dict[str, int] = {'w': 0, 'x': 0, 'y': 0, 'z': 0}

    def __repr__(self):
        return f"ALU(w={self.registers['w']}, x={self.registers['x']}, y={self.registers['y']}, z={self.registers['z']})"

    def __check_b(self, b: int | str):
        return b if isinstance(b, int) else self.registers[b]

    def inp(self, r: str, input_: deque[int]):
        self.registers[r] = input_.popleft()

    def add(self, a: str, b: str | int):
        self.registers[a] = self.registers[a] + self.__check_b(b)

    def mul(self, a: str, b: str | int):
        self.registers[a] = self.registers[a] * self.__check_b(b)

    def div(self, a: str, b: str | int):
        self.registers[a] = self.registers[a] // self.__check_b(b)

    def mod(self, a: str, b: str | int):
        self.registers[a] = self.registers[a] % self.__check_b(b)

    def eql(self, a: str, b: str | int):
        self.registers[a] = 1 if self.registers[a] == self.__check_b(b) else 0


def run(alu: ALU, program: list[Instruction], input_: deque[int]):
    for op in program:
        match op:
            case Instruction('inp', a): alu.inp(a, input_)
            case Instruction('add', a, b): alu.add(a, b)
            case Instruction('mul', a, b): alu.mul(a, b)
            case Instruction('div', a, b): alu.div(a, b)
            case Instruction('mod', a, b): alu.mod(a, b)
            case Instruction('eql', a, b): alu.eql(a, b)


def read_input(filepath: str) -> list[Instruction]:
    output = list()
    with open(filepath, 'r') as f:
        for line in f.readlines():
            output.append(Instruction.from_str(line.strip()))
    return output


def init_parser() -> str:
    parser = argparse.ArgumentParser(description="Advent of Code day 24 solution.")
    parser.add_argument('input', metavar='FILE', type=str, nargs=1, help="Path to input data.")
    args = parser.parse_args()
    return os.path.realpath(args.input[0])


if __name__ == "__main__":
    path = init_parser()
    program = read_input(path)
    input_ = deque([5])
    alu = ALU()

    print(alu)
    run(alu, program, input_)
    print(alu)



