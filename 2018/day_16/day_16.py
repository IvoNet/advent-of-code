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
from pathlib import Path
from typing import NamedTuple

from ivonet.files import read_rows
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


class ChronalClassification:

    def __init__(self, source, end_test: int = 3103, start_program: int = 3106) -> None:
        self.source = [ints(line) for line in source]
        self.ins = self.source[:end_test:4]
        self.ops = [Instruction(*o) for o in self.source[1:end_test:4]]
        self.outs = self.source[2:end_test:4]
        self.program = [Instruction(*o) for o in self.source[start_program:]]
        self.test_set = zip(self.ins, self.ops, self.outs)
        self.registers = {0: 0, 1: 0, 2: 0, 3: 0, }
        self.all_ops = [self.addr, self.addi, self.mulr, self.muli, self.banr, self.bani,
                        self.borr, self.bori, self.setr, self.seti, self.gtir, self.gtri,
                        self.gtrr, self.eqir, self.eqri, self.eqrr]

        self.opcodes = {}

    def possible_ops(self, i, op, o):
        ret = set()
        for cb in self.all_ops:
            self.registers = {k: v for k, v in enumerate(i)}
            cb(op)
            if self.registers == {k: v for k, v in enumerate(o)}:
                ret.add(cb)
        return ret

    def part_1(self):
        return sum(len(self.possible_ops(*tst)) >= 3 for tst in self.test_set)

    def deduce_opcodes(self):
        possibles = defaultdict(set)
        for i, op, o in self.test_set:
            res = self.possible_ops(i, op, o)
            possibles[op.opcode] = possibles[op.opcode].union(res)

        while len(self.opcodes) != 16:
            for k, v in possibles.items():
                if len(v) == 1:
                    code = v.pop()
                    self.opcodes[k] = code
                    for vals in possibles.values():
                        vals.discard(code)

    def part_2(self):
        self.deduce_opcodes()
        self.registers = {0: 0, 1: 0, 2: 0, 3: 0, }
        for i in self.program:
            self.opcodes[i.opcode](i)
        return self.registers[0]

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
    return ChronalClassification(source).part_1()


def part_2(source):
    return ChronalClassification(source).part_2()


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")

    def test_part_1(self):
        self.assertEqual(612, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(485, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
