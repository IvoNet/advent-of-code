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

from ivonet.files import read_rows
from ivonet.grid import Location, DIRECTIONS
from ivonet.iter import ints, rangei

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class ModeMaze:

    def __init__(self, source: list[str]) -> None:
        self.depth = ints(source[0])[0]
        col, row = ints(source[1])
        self.target = Location(row, col)
        self.start = Location(0, 0)
        self.cache = {}

    def geologic_index(self, loc: Location):
        if loc in self.cache:
            return self.cache[loc]
        if loc in [self.start, self.target]:
            ret = 0
        elif loc.row == 0:
            ret = loc.col * 16807
        elif loc.col == 0:
            ret = loc.row * 48271
        else:
            ret = self.erosion_level(loc + DIRECTIONS["W"]) * self.erosion_level(loc + DIRECTIONS["N"])
        self.cache[loc] = ret
        return ret

    def erosion_level(self, loc: Location):
        """A region's erosion level is its geologic index plus the cave system's depth, all modulo 20183."""
        return (self.geologic_index(loc) + self.depth) % 20183

    def region_type(self, loc: Location):
        """The region type
        If the erosion level modulo 3 is 0, the region's type is rocky.
        If the erosion level modulo 3 is 1, the region's type is wet.
        If the erosion level modulo 3 is 2, the region's type is narrow.
        """
        return self.erosion_level(loc) % 3

    def risk_level_smallest_rectangle(self):
        return sum(self.region_type(Location(row, col)) for col in rangei(0, self.target.col) for row in
                   rangei(0, self.target.row))

    def is_allowed_tool(self, loc: Location, tool):
        ...


def part_1(source):
    return ModeMaze(source).risk_level_smallest_rectangle()


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")

    def test_part_1(self):
        self.assertEqual(None, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
