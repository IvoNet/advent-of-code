#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
I made multiple failed versions before finally getting it right. Reading is an art :-)
I found this one very frustrating!
"""

import os
import sys
import unittest
from pathlib import Path
from typing import NamedTuple

from ivonet.files import read_rows
from ivonet.iter import ints, rangei

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Location(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Location(self.x + other.x, self.y + other.y)


UP = Location(0, -1)
DOWN = Location(0, 1)
LEFT = Location(-1, 0)
RIGHT = Location(1, 0)


class ReservoirResearch:

    def __init__(self, source, init_spring: Location = Location(500, 0)) -> None:
        self.spring = init_spring
        self.source = source
        self.lowest_y = None
        self.highest_y = None
        self.flowing = set()
        self.still = set()
        self.to_drip = set()
        self.to_fill = set()
        self.clay = set()
        self.parse()

    def drip(self, loc: Location):
        while loc.y < self.lowest_y:
            loc_down = loc + DOWN
            if loc_down not in self.clay:
                self.flowing.add(loc_down)
                loc = loc_down
            elif loc_down in self.clay:
                return loc
        return None

    def fill(self, loc: Location):
        water_to_be_determined = set()

        def fill_row(loc, direction):
            """Fills a row in a left of right direction"""
            pos = loc
            while pos not in self.clay:
                water_to_be_determined.add(pos)
                tst_loc = pos + DOWN
                if tst_loc not in self.clay and tst_loc not in self.still:
                    return pos
                pos = pos + direction
            return None

        loc_left = fill_row(loc, LEFT)
        loc_right = fill_row(loc, RIGHT)
        if not loc_left and not loc_right:
            self.still.update(water_to_be_determined)
        else:
            self.flowing.update(water_to_be_determined)
        return loc_left, loc_right

    def flow(self) -> ReservoirResearch:
        self.to_drip.add(self.spring)
        while self.to_drip or self.to_fill:
            while self.to_drip:
                tf = self.to_drip.pop()
                res = self.drip(tf)
                if res:
                    self.to_fill.add(res)

            while self.to_fill:
                ts = self.to_fill.pop()
                row_left, row_right = self.fill(ts)
                if not row_right and not row_left:
                    self.to_fill.add(ts + UP)
                else:
                    if row_left:
                        self.to_drip.add(row_left)
                    if row_right:
                        self.to_drip.add(row_right)
        return self

    def part_1(self):
        return len([p for p in (self.flowing | self.still) if p.y >= self.highest_y])

    def part_2(self):
        return len([p for p in self.still if p.y >= self.highest_y])

    def __repr__(self) -> str:
        """Tuned this to the range important to this puzzle. The area was too big."""

        def char(p):
            if p == self.spring:
                return '+'
            elif p in self.clay:
                return '#'
            elif p in both:
                return '$'
            elif p in self.still:
                return '~'
            elif p in self.flowing:
                return '|'
            else:
                return ' '

        both = self.flowing & self.still
        return '\n'.join(''.join(char(Location(x, y)) for x in rangei(300, 700)) for y in rangei(0, 1600))

    def parse(self):
        """Parse the input data to grid information
        """
        self.clay = set()
        for line in self.source:
            nums = ints(line)
            if line.startswith("x"):
                for y in rangei(nums[1], nums[2]):
                    self.clay.add(Location(nums[0], y))
            elif line.startswith("y"):
                for x in rangei(nums[1], nums[2]):
                    self.clay.add(Location(x, nums[0]))
        self.lowest_y = max(p.y for p in self.clay)
        self.highest_y = min(p.y for p in self.clay)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.rr = ReservoirResearch(self.source).flow()

    def test_part_1(self):
        _(self.rr)
        self.assertEqual(30737, self.rr.part_1())

    def test_part_2(self):
        _(self.rr)
        self.assertEqual(24699, self.rr.part_2())


if __name__ == '__main__':
    unittest.main()
