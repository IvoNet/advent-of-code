#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from collections import defaultdict
from pathlib import Path

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def presents(match, nr_of_presents=10, nr_of_houses=float("inf")):
    gifts = defaultdict(int)
    max_elves = match // 10
    for elf in range(1, max_elves):
        for house in range(elf, min(max_elves, elf * nr_of_houses), elf):
            gifts[house] += elf * nr_of_presents
    return min([x for x in gifts.items() if x[1] >= match], key=lambda x: x[0])[0]


def part_1(source):
    return presents(int(source))


def part_2(source):
    return presents(int(source), nr_of_presents=11, nr_of_houses=50)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"day_{day.zfill(2)}.input")

    def test_part_1(self):
        self.assertEqual(776160, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(786240, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
