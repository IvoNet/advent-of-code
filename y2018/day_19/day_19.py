#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """"""

import os
import sys
import unittest
from pathlib import Path
from typing import NamedTuple

from ivonet.files import read_rows
from ivonet.iter import ints, rangei

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Instruction(NamedTuple):
    opcode: str
    a: int
    b: int
    output: int  # register


class ChronalClassification:

    def __init__(self, source, instruction_pointer: int = 0, r0=0) -> None:
        self.source = source
        self.instructions: list[Instruction] = []
        self.bound_reg = None
        self.instruction_pointer: int = instruction_pointer
        self.parse(self.source)
        self.registers = {0: r0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        self.all_ops = {
            "addr": self.addr,
            "addi": self.addi,
            "mulr": self.mulr,
            "muli": self.muli,
            "banr": self.banr,
            "bani": self.bani,
            "borr": self.borr,
            "bori": self.bori,
            "setr": self.setr,
            "seti": self.seti,
            "gtir": self.gtir,
            "gtri": self.gtri,
            "gtrr": self.gtrr,
            "eqir": self.eqir,
            "eqri": self.eqri,
            "eqrr": self.eqrr
        }

    def parse(self, source):
        self.bound_reg = ints(source[0])[0]
        opcodes = [line.split()[0] for line in source[1:]]
        numbers = [ints(line) for line in source[1:]]
        self.instructions = [Instruction(op, *nrs) for op, nrs in zip(opcodes, numbers)]

    def background_process(self, reg=0):
        while True:
            try:
                cmd = self.instructions[self.instruction_pointer]
            except IndexError:
                break
            self.registers[self.bound_reg] = self.instruction_pointer
            self.all_ops[cmd.opcode](cmd)
            self.instruction_pointer = self.registers[self.bound_reg]
            _(f"{self.instruction_pointer:<3}, {list(self.registers.values())}")
            self.instruction_pointer += 1
        return self.registers[reg]

    def addr(self, cmd: Instruction):
        self.registers[cmd.output] = self.registers[cmd.a] + self.registers[cmd.b]

    def addi(self, cmd: Instruction):
        self.registers[cmd.output] = self.registers[cmd.a] + cmd.b

    def mulr(self, cmd: Instruction):
        self.registers[cmd.output] = self.registers[cmd.a] * self.registers[cmd.b]

    def muli(self, cmd: Instruction):
        self.registers[cmd.output] = self.registers[cmd.a] * cmd.b

    def banr(self, cmd: Instruction):
        self.registers[cmd.output] = self.registers[cmd.a] & self.registers[cmd.b]

    def bani(self, cmd: Instruction):
        self.registers[cmd.output] = self.registers[cmd.a] & cmd.b

    def borr(self, cmd: Instruction):
        self.registers[cmd.output] = self.registers[cmd.a] | self.registers[cmd.b]

    def bori(self, cmd: Instruction):
        self.registers[cmd.output] = self.registers[cmd.a] | cmd.b

    def setr(self, cmd: Instruction):
        self.registers[cmd.output] = self.registers[cmd.a]

    def seti(self, cmd: Instruction):
        self.registers[cmd.output] = cmd.a

    def gtir(self, cmd: Instruction):
        self.registers[cmd.output] = 1 if cmd.a > self.registers[cmd.b] else 0

    def gtri(self, cmd: Instruction):
        self.registers[cmd.output] = 1 if self.registers[cmd.a] > cmd.b else 0

    def gtrr(self, cmd: Instruction):
        self.registers[cmd.output] = 1 if self.registers[cmd.a] > self.registers[cmd.b] else 0

    def eqir(self, cmd: Instruction):
        self.registers[cmd.output] = 1 if cmd.a == self.registers[cmd.b] else 0

    def eqri(self, cmd: Instruction):
        self.registers[cmd.output] = 1 if self.registers[cmd.a] == cmd.b else 0

    def eqrr(self, cmd: Instruction):
        self.registers[cmd.output] = 1 if self.registers[cmd.a] == self.registers[cmd.b] else 0


def part_1(source):
    # return sum([i for i in rangei(1, 1017) if 1017 % i == 0])
    return ChronalClassification(source).background_process()


def part_2(source):
    """Again slow!!
    return ChronalClassification(source, r0=1).background_process() won't really work so analyse

    - piece of the output
    - significant = 10551417
    - every time reg 2 hits 3 reg 4 adds one
    - 10551417 % 3 == 0... does this mean anything?
    - Should I look for devisors?
    - all devisors for 10551417 are [1, 3, 3517139, 10551417]
    - sum of those?
    - Analysing output of part_1 confirms this but then with a much smaller number 1017
       [1, 3, 9, 113, 339, 1017] halfway through its run reg 0 had value 126 which is the sum of 1,3,9,113... try!
    - works :-)
    """
    # return ChronalClassification(source, r0=1).background_process()
    return sum([i for i in rangei(1, 10551417) if 10551417 % i == 0])


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5""")

    def test_example_data_part_1(self):
        self.assertEqual(6, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(1482, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(14068560, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
