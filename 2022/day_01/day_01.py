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

from ivonet.files import read_data, read_ints
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def sum_foods(source) -> list[int]:
    return [sum(read_ints(calories)) for calories in source.split("\n\n")]


def part_1(source):
    return max(sum_foods(source))


def part_2(source):
    foods = sorted(sum_foods(source))
    return sum(foods[-3:])


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_data("""1000
2000
3000

4000

5000
6000

7000
8000
9000

10000""")

    def test_example_data_part_1(self):
        self.assertEqual(24000, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(70369, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(45000, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(203002, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
