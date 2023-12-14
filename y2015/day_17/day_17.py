#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from itertools import combinations
from pathlib import Path

from ivonet.files import read_ints
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def containers(liters, source, shortest=False):
    count = 0
    combi = []
    for i in range(2, len(source)):
        if shortest and combi:
            break
        for x in combinations(source, i):
            if sum(x) == liters:
                _(x, "->", 150)
                combi.append(x)
                count += 1
    return combi, count


def part_1(source, liters=150):
    combi, count = containers(liters, source)
    return count


def part_2(source, liters=150):
    combi, count = containers(liters, source, shortest=True)
    return count


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_ints(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}.input")))
        self.test_source = read_ints("""20
15
10
5
5""")

    def test_example_data_part_1(self):
        self.assertEqual(4, part_1(self.test_source, liters=25))

    def test_part_1(self):
        self.assertEqual(1304, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(18, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
