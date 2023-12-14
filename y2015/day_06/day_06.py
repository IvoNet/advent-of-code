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

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Coord(NamedTuple):
    x: int
    y: int


def turn_1(grid: dict, start: Coord, stop: Coord, state=True):
    for x in range(start.x, stop.x + 1):
        for y in range(start.y, stop.y + 1):
            grid[Coord(x, y)] = state


def toggle_1(grid: dict, start: Coord, stop: Coord):
    for x in range(start.x, stop.x + 1):
        for y in range(start.y, stop.y + 1):
            grid[Coord(x, y)] = not grid[Coord(x, y)]


def process_1(source):
    grid = defaultdict(bool)
    for line in source:
        x1, y1, x2, y2 = ints(line)
        _(x1, y1, x2, y2)
        start = Coord(x1, y1)
        stop = Coord(x2, y2)
        if "turn on" in line:
            turn_1(grid, start, stop, state=True)
            continue
        if "turn off" in line:
            turn_1(grid, start, stop, state=False)
            continue
        if "toggle" in line:
            toggle_1(grid, start, stop)
    return grid


def turn_2(grid: dict, start: Coord, stop: Coord, state=1):
    for x in range(start.x, stop.x + 1):
        for y in range(start.y, stop.y + 1):
            grid[Coord(x, y)] += state
            if grid[Coord(x, y)] < 0:
                grid[Coord(x, y)] = 0


def process_2(source):
    grid = defaultdict(int)
    for line in source:
        x1, y1, x2, y2 = ints(line)
        start = Coord(x1, y1)
        stop = Coord(x2, y2)
        if "turn on" in line:
            turn_2(grid, start, stop, state=1)
            continue
        if "turn off" in line:
            turn_2(grid, start, stop, state=-1)
            continue
        if "toggle" in line:
            turn_2(grid, start, stop, state=2)
    return grid


def part_1(source):
    grid = process_1(source)
    return sum(1 for v in grid.values() if v is True)


def part_2(source):
    grid = process_2(source)
    return sum(v for v in grid.values())


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}.input")))

    def test_part_1(self):
        self.assertEqual(377891, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(14110788, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
