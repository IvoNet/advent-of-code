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
from typing import NamedTuple

from ivonet.files import read_rows
from ivonet.iter import ints, rangei

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


class ReservoirResearch:

    def __init__(self, source, init_spring: Point = Point(500, 0)) -> None:
        self.spring = init_spring
        self.source = source
        self.lowest_y = None
        self.highest_y = None
        self.flowing = set()
        self.still = set()
        self.to_fall = set()
        self.to_fill = set()
        self.clay = set()
        self.parse()
        self.UP = Point(0, -1)
        self.DOWN = Point(0, 1)
        self.LEFT = Point(-1, 0)
        self.RIGHT = Point(1, 0)

    def drip(self, pos, ly, clay, flowing):
        while pos.y < ly:
            posd = pos + self.DOWN
            if posd not in clay:
                flowing.add(posd)
                pos = posd
            elif posd in clay:
                return pos
        return None

    def fill(self, pos, clay, flowing, still):
        temp = set()
        pl = self.fill_r(pos, self.LEFT, clay, still, temp)
        pr = self.fill_r(pos, self.RIGHT, clay, still, temp)
        if not pl and not pr:
            still.update(temp)
        else:
            flowing.update(temp)
        return pl, pr

    def fill_r(self, pos, off, clay, still, temp):
        pos1 = pos
        while pos1 not in clay:
            temp.add(pos1)
            pos2 = pos1 + self.DOWN
            if pos2 not in clay and pos2 not in still:
                return pos1
            pos1 = pos1 + off
        return None

    def flow(self) -> ReservoirResearch:
        self.to_fall.add(self.spring)
        while self.to_fall or self.to_fill:
            while self.to_fall:
                tf = self.to_fall.pop()
                res = self.drip(tf, self.lowest_y, self.clay, self.flowing)
                if res:
                    self.to_fill.add(res)

            while self.to_fill:
                ts = self.to_fill.pop()
                rl, rr = self.fill(ts, self.clay, self.flowing, self.still)
                if not rr and not rl:
                    self.to_fill.add(ts + self.UP)
                else:
                    if rl:
                        self.to_fall.add(rl)
                    if rr:
                        self.to_fall.add(rr)
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
                return '.'

        both = self.flowing & self.still
        return '\n'.join(''.join(char(Point(x, y)) for x in rangei(300, 700)) for y in rangei(0, 1000))

    def parse(self):
        """Parse the input data to grid information
        """
        self.clay = set()
        for line in self.source:
            nums = ints(line)
            if line.startswith("x"):
                for y in rangei(nums[1], nums[2]):
                    self.clay.add(Point(nums[0], y))
            elif line.startswith("y"):
                for x in rangei(nums[1], nums[2]):
                    self.clay.add(Point(x, nums[0]))
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
