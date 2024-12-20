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


def fuel(mass):
    return mass // 3 - 2


def recursive_fuel(mass):
    """Recursive fuel calculation for the fuel mass itself"""
    petrol = fuel(mass)
    if petrol > 0:
        return petrol + recursive_fuel(petrol)
    return 0


def part_1(source):
    return sum(fuel(mass) for mass in source)


def part_2(source):
    return sum(recursive_fuel(mass) for mass in source)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_ints(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_ints("""1969""")
        self.test_source2 = read_ints("""100756""")
        self.test_source3 = read_ints("""100756""")
        self.test_source4 = read_ints("""1969""")

    def test_example_data_part_1(self):
        self.assertEqual(654, part_1(self.test_source))
        self.assertEqual(33583, part_1(self.test_source2))

    def test_part_1(self):
        self.assertEqual(3432671, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(50346, part_2(self.test_source3))
        self.assertEqual(966, part_2(self.test_source4))

    def test_part_2(self):
        self.assertEqual(5146132, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
