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
from itertools import combinations
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def part_1(source):
    tot = 0
    for line in source:
        nrs = ints(line)
        tot += max(nrs) - min(nrs)
    return tot


def part_2(source):
    tot = 0
    for line in source:
        nrs = ints(line)
        for x, y in combinations(nrs, 2):
            _(x, y)
            if x % y == 0:
                tot += x // y
            elif y % x == 0:
                tot += y // x
    return tot


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""5 9 2 8
9 4 7 3
3 8 6 5""")

    def test_part_1(self):
        self.assertEqual(50376, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(9, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(267, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
