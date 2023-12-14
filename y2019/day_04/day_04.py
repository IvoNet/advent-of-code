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
from ivonet.iter import ints, rangei, lmap

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def is_valid_password(password: int, simple=True) -> bool:
    digits = lmap(int, str(password))
    current = digits[0]
    adjacent = 1
    double = False
    for digit in digits[1:]:
        if digit < current:
            return False
        if not double:
            if digit == current:
                adjacent += 1
            if digit > current:
                if not simple and adjacent == 2:
                    double = True
                adjacent = 1
            if simple and adjacent >= 2:
                double = True
        current = digit
    return double or (not simple and adjacent == 2)


def part_1(source, simple=True):
    valids = []
    for i in rangei(source[0], source[1]):
        if is_valid_password(i, simple):
            valids.append(i)
    return len(valids)


def part_2(source):
    return part_1(source, False)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_ints(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input", delimiter="-")
        self.test_source = read_ints("""111111-111111""", delimiter="-")
        self.test_source2 = read_ints("""223450-223450""", delimiter="-")
        self.test_source3 = read_ints("""112233-112233""", delimiter="-")
        self.test_source4 = read_ints("""123444-123444""", delimiter="-")
        self.test_source5 = read_ints("""111122-111122""", delimiter="-")

    def test_example_data_part_1(self):
        self.assertEqual(1, part_1(self.test_source))
        self.assertEqual(0, part_1(self.test_source2))

    def test_part_1(self):
        self.assertEqual(1605, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(1, part_2(self.test_source3))
        self.assertEqual(0, part_2(self.test_source4))
        self.assertEqual(1, part_2(self.test_source5))

    def test_part_2(self):
        self.assertEqual(1102, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
