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
from itertools import count
from pathlib import Path

from ivonet.files import read_ints
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def part_1(source):
    border = len(source)
    i = 0
    for steps in count(1):
        jmp = source[i]
        source[i] += 1
        i += jmp
        if i >= border or i < 0:
            return steps


def part_2(source):
    border = len(source)
    i = 0
    for steps in count(1):
        jmp = source[i]
        source[i] += -1 if jmp >= 3 else 1
        i += jmp
        if i >= border or i < 0:
            return steps


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_ints(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_ints("""0
3
0
1
-3""")

    def test_example_data_part_1(self):
        self.assertEqual(5, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(376976, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(10, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(29227751, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
