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

from ivonet.files import read_ints
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


# noinspection DuplicatedCode
class IntCodeComputer(object):
    ADD = 1
    MULTIPLY = 2
    HALT = 99
    INSTRUCTIONS = {
        ADD: lambda left, right: left + right,
        MULTIPLY: lambda left, right: left * right,
    }

    def __init__(self, source, noun=None, verb=None) -> None:
        self.source = source.copy()
        self.noun = noun
        self.verb = verb
        self.halt = False
        self.instruction_pointer = 0
        self.memory = None
        self.reset(self.noun, self.verb)

    def run(self) -> IntCodeComputer:
        while not self.halt:
            self.step()
        return self

    def step(self):
        opcode = self.address(self.instruction_pointer)
        if opcode == IntCodeComputer.HALT:
            self.halt = True
            self.instruction_pointer += 1
            return
        left = self.memory[self.memory[self.instruction_pointer + 1]]
        right = self.memory[self.memory[self.instruction_pointer + 2]]
        position = self.memory[self.instruction_pointer + 3]
        self.memory[position] = IntCodeComputer.INSTRUCTIONS[opcode](left, right)
        self.instruction_pointer += 4

    def address(self, position: int, indexed=0) -> int:
        return self.memory[position - indexed]

    def match(self, value: int, noun: int, verb: int) -> bool:
        try:
            self.reset(noun, verb).run()
        except KeyError:
            return False
        return self.memory[0] == value

    def reset(self, noun=None, verb=None) -> IntCodeComputer:
        self.memory = self.source.copy()
        self.instruction_pointer = 0
        self.halt = False
        self.memory[1] = noun if noun is not None else self.memory[1]
        self.memory[2] = verb if verb is not None else self.memory[2]
        return self


def part_1(source):
    return None


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_ints(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input", delimiter=",")
        self.test_source = read_ints("""1101,100,-1,4,0""", delimiter=",")

    def test_example_data_part_1(self):
        self.assertEqual(None, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(None, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
