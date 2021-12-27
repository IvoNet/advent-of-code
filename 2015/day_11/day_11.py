#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from itertools import groupby
from pathlib import Path

from ivonet.alphabet import alphabet
from ivonet.files import read_data
from ivonet.iter import ints, consecutive_element_pairing

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def straight_three(source) -> bool:
    letters = list(alphabet(upper=False))
    for three in consecutive_element_pairing(letters, consecutive_element=3, map_to_func=lambda x: "".join(x)):
        if three in source:
            return True
    return False


def double_double(source: str) -> bool:
    found = 0
    for label, group in groupby(source):
        g = list(group)
        if len(g) >= 2:
            found += 1
    return found >= 2


def part_1(source):
    return 0


def part_2(source):
    return 0


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"day_{day.zfill(2)}.input")
        self.test_source = read_data("""hijklmmn""")
        self.test_source_1 = read_data("""abbceffg""")

    def test_straight_three(self):
        self.assertTrue(straight_three(self.test_source))
        self.assertFalse(straight_three(self.test_source_1))

    def test_double_letters(self):
        self.assertFalse(double_double(self.test_source))
        self.assertTrue(double_double(self.test_source_1))

    def test_part_1(self):
        self.assertEqual(None, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
