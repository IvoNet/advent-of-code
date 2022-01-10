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

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def parse(source):
    instructions = [x.split() for x in source]
    for cmd in instructions:
        cmd[2] = int(cmd[2])
        cmd[-1] = int(cmd[-1])
    return instructions


class Interpreter:

    def __init__(self, source) -> None:
        self.instructions = parse(source)
        self.registers = defaultdict(int)
        self.operator_functions = {
            "!=": lambda left, right: left != right,
            "==": lambda left, right: left == right,
            ">=": lambda left, right: left >= right,
            ">": lambda left, right: left > right,
            "<": lambda left, right: left < right,
            "<=": lambda left, right: left <= right,
        }
        self.command_functions = {
            "inc": lambda left, right: left + right,
            "dec": lambda left, right: left - right,
        }
        self.max_memory = float("-inf")

    def evaluate(self) -> Interpreter:
        for c_reg, cmd, c_val, _, o_reg, op, o_val in self.instructions:
            if self.operator_functions[op](self.registers[o_reg], o_val):
                self.registers[c_reg] = self.command_functions[cmd](self.registers[c_reg], c_val)
                self.reg_mem()
        return self

    def largest_register(self):
        return max(self.registers.values())

    def reg_mem(self):
        self.max_memory = max(self.max_memory, self.largest_register())
        return self.max_memory


def part_1(source):
    return Interpreter(source).evaluate().largest_register()


def part_2(source):
    return Interpreter(source).evaluate().reg_mem()


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10""")

    def test_example_data_part_1(self):
        self.assertEqual(1, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(5143, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(10, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(6209, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
