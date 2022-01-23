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
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from typing import NamedTuple

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Instruction(NamedTuple):
    opcode: int
    a: int
    b: int
    output: int  # register


def parse(source):
    first, second = source.split("\n\n\n\n")
    first = first.split("\n\n")
    second = second.splitlines()
    testset = []
    instructions = []
    for bia in first:
        ts = []
        before, inst, after = bia.splitlines()
        ts.append({k: v for k, v in enumerate(ints(before))})
        ts.append(Instruction(*ints(inst)))
        ts.append({k: v for k, v in enumerate(ints(after))})
        testset.append(ts)
    for cmd in second:
        instructions.append(Instruction(*ints(cmd)))
    return testset, instructions


class ChronalClassification:

    def __init__(self, source) -> None:
        self.source = source
        self.testset, self.instructions = parse(self.source)
        self.registers = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
        }

        self.commands = {
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
            "eqrr": self.eqrr,
        }

        self.opcodes = {
            4: self.eqrr
        }

    def cmd_executor(self):
        three_or_more = defaultdict(list)
        opcodes = defaultdict(list)
        for before, cmd, after in self.testset:
            correct = defaultdict(list)
            for name, method in self.commands.items():
                self.registers = deepcopy(before)
                _("Before  :", before.values())
                _(cmd)
                method(cmd)
                _("after   :", self.registers.values())
                _("Expected:", after.values())
                if self.registers == after:
                    correct[cmd].append(name)
                    opcodes[cmd.opcode].append(name)
            if len(correct[cmd]) == 1:
                self.opcodes[cmd.opcode] = self.commands[correct[cmd][0]]
            if len(correct[cmd]) >= 3:
                three_or_more[tuple(before.values()), cmd, tuple(after.values())] = correct[cmd]

        return len(three_or_more)

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
    return ChronalClassification(source).cmd_executor()


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_data("""Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]



9 2 0 1""")

    def test_parse(self):
        parse(self.source)

    def test_example_data_part_1(self):
        self.assertEqual(1, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(612, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
