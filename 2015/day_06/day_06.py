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
from typing import NamedTuple

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Coord(NamedTuple):
    x: int
    y: int


def turn(grid: dict, start: Coord, stop: Coord, state=True):
    for x in range(start.x, stop.x + 1):
        for y in range(start.y, stop.y + 1):
            grid[Coord(x, y)] = state


def toggle(grid: dict, start: Coord, stop: Coord):
    for x in range(start.x, stop.x + 1):
        for y in range(start.y, stop.y + 1):
            grid[Coord(x, y)] = not grid[Coord(x, y)]


def process(source):
    grid = defaultdict(bool)
    # instructions = []
    for line in source:
        x1, y1, x2, y2 = ints(line)
        _(x1, y1, x2, y2)
        start = Coord(x1, y1)
        stop = Coord(x2, y2)
        if "turn on" in line:
            # instructions.append(("on", start, stop))
            turn(grid, start, stop, state=True)
            continue
        if "turn off" in line:
            # instructions.append(("off", start, stop))
            turn(grid, start, stop, state=False)
            continue
        if "toggle" in line:
            # instructions.append(("toggle", start, stop))
            toggle(grid, start, stop)
    return grid  # , instructions


def part_1(source):
    grid = process(source)
    return sum(1 for v in grid.values() if v is True)


def part_2(source):
    # Should calculate not do!!
    return 0


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"day_{day.zfill(2)}.input")
        self.test_source = read_rows("""""")

    def test_example_data_part_1(self):
        self.assertEqual(None, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(377891, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
