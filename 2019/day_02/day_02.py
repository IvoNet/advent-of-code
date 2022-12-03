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

ADD = 1
MULTIPLY = 2
HALT = 99


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def program(source):
    for instruction in range(0, len(source), 4):
        opcode, left, right, position = source[instruction:instruction + 4]
        if opcode == HALT:
            break
        if opcode == ADD:
            source[position] = source[left] + source[right]
        if opcode == MULTIPLY:
            source[position] = source[left] * source[right]
        _(source)
    return source[0]


def part_1(source):
    source[1] = 12
    source[2] = 2
    return program(source)


def part_2(source):
    return None


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
        self.assertEqual(3500, program(self.test_source))
        self.assertEqual(2, program(self.test_source2))
        self.assertEqual(2, program(self.test_source3))
        self.assertEqual(2, program(self.test_source4))
        self.assertEqual(30, program(self.test_source5))

    def test_part_1(self):
        self.assertEqual(None, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
