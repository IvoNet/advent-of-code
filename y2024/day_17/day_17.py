#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2023 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
If a part of the code is not part of the post it is probably 
code I found reusable and I may have moved it to my 'ivonet' library.
you can find that here: https://github.com/IvoNet/advent-of-code/tree/master/ivonet
"""

import collections
import os
import sys
import unittest
from math import trunc
from pathlib import Path
from typing import Callable

import pyperclip

from ivonet.decorators import debug
from ivonet.decorators import timer
from ivonet.files import read_rows
from ivonet.iter import ints

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


class ChronospacialComputer:
    def __init__(self, source: list[str]) -> None:
        self.source = source
        self.a: int = 0
        self.b: int = 0
        self.c: int = 0
        self.program: list[int] = []
        self.combo = {
            0: self.lit_0,
            1: self.lit_1,
            2: self.lit_2,
            3: self.lit_3,
            4: self.reg_a,
            5: self.reg_b,
            6: self.reg_c,
            7: None
        }
        self.opcode: dict[int, Callable[[int], None]] = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv
        }
        self.instruction_pointer = 0
        self.instruction_pointer_advance = 2
        self.output = []
        self.parse_source()

    def lit_0(self) -> int:
        return 0

    def lit_1(self) -> int:
        return 1

    def lit_2(self) -> int:
        return 2

    def lit_3(self) -> int:
        return 3

    def reg_a(self) -> int:
        return self.a

    def reg_b(self) -> int:
        return self.b

    def reg_c(self) -> int:
        return self.c

    def __division(self, operand: int) -> int:
        return trunc(self.a // 2 ** self.combo[operand]())

    def adv(self, operand: int) -> None:
        """Division.
        The numerator is the value in the A register.
        The denominator is found by raising 2 to the power of the instruction's combo operand
        """
        self.a = self.__division(operand)
        p(f"{self.instruction_pointer:2}: adv: A -> A={self.a}, B={self.b}, c={self.c}, formula: a // 2 ** combo[{operand}]() -> {self.combo[operand]}")

    def bxl(self, operand: int) -> None:
        """calculates the bitwise XOR of register B and
        the instruction's literal operand, then stores the result in register B
        """
        self.b = self.b ^ operand
        p(f"{self.instruction_pointer:2}: blx: B -> A={self.a}, B={self.b}, c={self.c}, formula: b ^ {operand}")

    def bst(self, operand: int) -> None:
        """calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits),
        then writes that value to the B register
        """
        self.b = self.combo[operand]() % 8
        p(f"{self.instruction_pointer:2}: bst: B -> A={self.a}, B={self.b}, c={self.c}, formula: combo[{operand}]() % 8 -> {self.combo[operand]}")

    def jnz(self, operand: int) -> None:
        """
        Does nothing if the A register is 0. However, if the A register is not zero,
        it jumps by setting the instruction pointer to the value of its literal operand;
        if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.
        """
        if self.a != 0:
            self.instruction_pointer = operand - 2  # will result in not moving the instruction pointer
        p(f"{self.instruction_pointer:2}: jnz: IP {self.instruction_pointer}, A={self.a}, B={self.b}, c={self.c}, formula: A == 0")

    def bxc(self, operand: int) -> None:
        """calculates the bitwise XOR of register B and register C,
        then stores the result in register B.
        (For legacy reasons, this instruction reads an operand but ignores it.)
        """
        self.b = self.b ^ self.c
        p(f"{self.instruction_pointer:2}: bxc: B -> A={self.a}, B={self.b}, c={self.c}, formula: b ^ c")

    def out(self, operand: int) -> None:
        """calculates the value of its combo operand modulo 8, then outputs that value.
        (If a program outputs multiple values, they are separated by commas.)
        """
        output = self.combo[operand]() % 8
        self.output.append(output)
        p(f"{self.instruction_pointer:2}: out: {output}, formula: combo[{operand}]() % 8 -> {self.combo[operand]}")

    def bdv(self, operand: int) -> None:
        """works exactly like the adv instruction except that the result is stored in the B register.
        (The numerator is still read from the A register.)
        """
        self.b = self.__division(operand)
        p(f"{self.instruction_pointer:2}: bdv: B -> A={self.a}, B={self.b}, c={self.c}, formula: a // 2 ** combo[{operand}]() -> {self.combo[operand]}")

    def cdv(self, operand: int) -> None:
        """works exactly like the adv instruction except that the result is stored in the C register.
        (The numerator is still read from the A register.)
        """
        self.c = self.__division(operand)
        p(f"{self.instruction_pointer:2}: cdv: C -> A={self.a}, B={self.b}, c={self.c}, formula: a // 2 ** combo[{operand}]() -> {self.combo[operand]}")

    def run(self) -> None:
        """
        Executes the program loaded into the ChronospacialComputer.

        This method iterates through the program instructions, executing each one based on the current
        instruction pointer. The instruction pointer is advanced by a fixed amount after each instruction
        unless modified by specific instructions (e.g., jnz).

        The program consists of opcodes and operands:
        - opcode: Determines the operation to be performed.
        - operand: Provides additional data required for the operation.

        The method uses the opcode to look up the corresponding function in the self.opcode dictionary
        and executes it with the operand.

        Debugging information is printed if the DEBUG flag is set.
        """
        while self.instruction_pointer < len(self.program):
            opcode = self.program[self.instruction_pointer]
            operand = self.program[self.instruction_pointer + 1]
            p(f"IP: {self.instruction_pointer}, opcode: {opcode}, operand: {operand}")
            self.opcode[opcode](operand)
            self.instruction_pointer += self.instruction_pointer_advance

    def copy_self(self):
        """
        Finds the minimum solution offset that, when used as the initial value of register A,
        results in the program's output matching the last length elements of the program.

        The method works by iterating through all possible offsets (0 to 7) for each solution
        and checking if the output of the program matches the expected output. The offset solution
        works because the program operates in a three-bit system, meaning the values are constrained
        to a range of 0 to 7, allowing for efficient brute-force checking.
        """
        solutions = [0]
        for length in range(1, len(self.program) + 1):
            output = []
            for solution in solutions:
                for offset in range(8):
                    solution_offset = 8 * solution + offset
                    self.reset(solution_offset)
                    self.run()
                    if self.output == self.program[-length:]:
                        output.append(solution_offset)
            solutions = output
        if solutions:
            p(f"Solutions: {solutions}, min: {min(solutions)}")
            return min(solutions)
        return None

    def __str__(self):
        return ",".join(str(x) for x in self.output)

    def __repr__(self):
        return self.__str__()

    def reset(self, a):
        self.a = a
        self.b = 0
        self.c = 0
        self.instruction_pointer = 0
        self.output = []

    def parse_source(self):
        for line in self.source:
            if "A:" in line:
                self.a = ints(line)[0]
            if "B:" in line:
                self.b = ints(line)[0]
            if "C:" in line:
                self.c = ints(line)[0]
            if "Program:" in line:
                self.program = ints(line)


@debug
@timer
def part_1(source) -> str | None:
    pc = ChronospacialComputer(source)
    pc.run()
    answer = str(pc)
    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:
    """
    The brute force solution that will take a long time to complete.
    so we need to optimize this
    Observations about the formulae is the div 8 and the modulo 8
    and we only work in a three bit system, so we can optimize this somehow
    ---
    """
    pc = ChronospacialComputer(source)
    answer = pc.copy_self()
    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_examples_1(self):
        pc = ChronospacialComputer([])
        pc.a = 0
        pc.b = 0
        pc.c = 9
        pc.program = [2, 6]
        pc.run()
        self.assertEqual(1, pc.b)

    def test_examples_2(self):
        pc = ChronospacialComputer([])
        pc.a = 10
        pc.b = 0
        pc.c = 0
        pc.program = [5, 0, 5, 1, 5, 4]
        pc.run()
        self.assertEqual("0,1,2", str(pc))

    def test_examples_3(self):
        pc = ChronospacialComputer([])
        pc.a = 2024
        pc.b = 0
        pc.c = 0
        pc.program = [0, 1, 5, 4, 3, 0]
        pc.run()
        self.assertEqual("4,2,5,6,7,7,7,7,3,1,0", str(pc))

    def test_examples_4(self):
        pc = ChronospacialComputer([])
        pc.a = 0
        pc.b = 29
        pc.c = 0
        pc.program = [1, 7]
        pc.run()
        self.assertEqual(26, pc.b)

    def test_examples_5(self):
        pc = ChronospacialComputer([])
        pc.a = 0
        pc.b = 2024
        pc.c = 43690
        pc.program = [4, 0]
        pc.run()
        self.assertEqual(44354, pc.b)

    def test_example_data_part_1(self) -> None:
        self.assertEqual("4,6,3,5,6,3,5,2,1,0", part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual("7,6,1,5,3,1,4,2,6", part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(117440, part_2(self.test_source_1))

    def test_part_2(self) -> None:
        self.assertEqual(164541017976509, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")
        self.test_source_1 = read_rows(f"{folder}/test_{day}_1.input")


if __name__ == '__main__':
    # folder = os.path.dirname(os.path.realpath(__file__))
    # day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
    # source = read_rows(f"{folder}/day_{day}.input")
    # part_2(source)
    unittest.main()
