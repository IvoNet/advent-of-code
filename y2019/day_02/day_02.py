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

DEBUG = False


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
    return IntCodeComputer(source, noun=12, verb=2).run().address(0)


def part_2(source, value=19690720):
    intcode = IntCodeComputer(source)
    for noun in range(100 if len(source) > 100 else len(source)):
        for verb in range(100 if len(source) > 100 else len(source)):
            if intcode.match(value, noun, verb):
                _(noun, verb)
                return 100 * noun + verb
    raise ValueError("No match found")


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_ints(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input", delimiter=",")
        self.test_source = read_ints("""1,9,10,3,2,3,11,0,99,30,40,50""", delimiter=",")
        self.test_source2 = read_ints("""1,0,0,0,99,0,0,0""", delimiter=",")
        self.test_source3 = read_ints("""2,3,0,3,99,0,0,0""", delimiter=",")
        self.test_source4 = read_ints("""2,4,4,5,99,0,0,0""", delimiter=",")
        self.test_source5 = read_ints("""1,1,1,4,99,5,6,0,99,0,0,0""", delimiter=",")

    def test_example_data_part_1(self):
        self.assertEqual(3500, IntCodeComputer(self.test_source).run().address(0))
        self.assertEqual(2, IntCodeComputer(self.test_source2).run().address(0))
        self.assertEqual(2, IntCodeComputer(self.test_source3).run().address(0))
        self.assertEqual(2, IntCodeComputer(self.test_source4).run().address(0))
        self.assertEqual(30, IntCodeComputer(self.test_source5).run().address(0))

    def test_part_1(self):
        self.assertEqual(10566835, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertTrue(1202, part_2(self.source, 10566835))

    def test_part_2(self):
        self.assertEqual(2347, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
