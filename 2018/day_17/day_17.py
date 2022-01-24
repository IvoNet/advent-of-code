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
from enum import Enum
from pathlib import Path
from typing import Callable, Any, NamedTuple

from ivonet.files import read_rows
from ivonet.iter import ints, rangei

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Cell(str, Enum):
    SAND = "."
    CLAY = "#"
    SETTLED_WATER = "~"
    FLOWING_WATER = "|"
    SPRING_OF_WATER = "+"
    GOAL = "G"

    def __repr__(self) -> str:
        return self.value

    def __str__(self) -> str:
        return repr(self)


class Location(NamedTuple):
    row: int
    col: int


class ReservoirResearch:

    def __init__(self, source, init_spring: Location = Location(0, 500)) -> None:
        self.source = source
        self.rows: int = 0
        self.min_rows: int = 0
        self.cols: int = 0
        self.grid = []
        self.clay: list[int, int] = []
        self.init()
        self.springs: list[Location] = [init_spring]
        self.settled_water: set[Location] = set()
        self.flowing_water: set[Location] = set()
        self.settled_springs: set[Location] = set()

    def init(self):
        start: Callable[[Any], list[list[int]]] = lambda i: [ints(line) for line in self.source if line.startswith(i)]
        y_start = start("y")
        x_start = start("x")
        self.rows = max(max(y_start, key=lambda x: x[0])[0], max(x_start, key=lambda x: x[2])[0])
        self.min_rows = min(min(y_start, key=lambda x: x[0])[0], min(x_start, key=lambda x: x[1])[1])
        self.cols = max(max(y_start, key=lambda x: x[2])[0], max(x_start, key=lambda x: x[0])[0])
        self.grid = [[Cell.SAND for _ in rangei(0, self.cols)] for _ in rangei(0, self.rows)]
        yx = [[y, range(b, c)] for y, b, c in y_start]
        for r, cr in yx:
            for c in cr:
                self.grid[r][c] = Cell.CLAY
                self.clay.append((r, c))
        xy = [[x, range(b, c)] for x, b, c in x_start]
        for c, yr in xy:
            for r in yr:
                self.grid[r][c] = Cell.CLAY
                self.clay.append((r, c))

    def mark(self):
        for f in self.springs:
            self.grid[f.row][f.col] = Cell.SPRING_OF_WATER
        for f in self.settled_water:
            self.grid[f.row][f.col] = Cell.SETTLED_WATER
        for f in self.flowing_water:
            self.grid[f.row][f.col] = Cell.FLOWING_WATER

    def clear(self):
        for f in self.springs:
            self.grid[f.row][f.col] = Cell.SAND
        for f in self.settled_water:
            self.grid[f.row][f.col] = Cell.SAND
        for f in self.flowing_water:
            self.grid[f.row][f.col] = Cell.SAND

    def is_clay(self, loc: Location) -> bool:
        return self.grid[loc.row][loc.col] == Cell.CLAY

    def is_clay(self, r: int, c: int) -> bool:
        return self.grid[r][c] == Cell.CLAY

    def is_settled_or_sand(self, loc: Location):
        return self.grid[loc.row][loc.col] in [Cell.SAND, Cell.SETTLED_WATER]

    def is_settled_or_sand(self, r: int, c: int):
        return self.grid[r][c] in [Cell.SAND, Cell.SETTLED_WATER]

    def flow(self, spring: Location):
        """Let the water flow...
        what are the steps in which water flows?
        - we have to start with 1 spring of water (0,500)
        - water flows down
        - it will hit a bottom
        - it fills from the bottom outwards till it hits a wall or can flow down again (if now wall)
        - if a wall it fills the next row up again outwards till it hits a wall or can flow
        - when it can flow again that will be counted as on or more new spring(s) for the next step
        - this way we may be able to iterate flow steps?!
        - as a step as described above would not change anymore it can be counted for all the watter (|,~)
        - Stepping stops when the water goes above 0 or below max y
        """

        new_springs = set()
        loc = spring
        r = loc.row
        c = loc.col
        # walk down
        while not self.is_clay(loc):
            if loc.row >= self.min_rows:
                self.flowing_water.add(loc)
            if loc.row >= self.rows:
                return new_springs
            r += 1
            loc = Location(r, c)
        while True:
            r -= 1
            nloc = {Location(r, c)}
            cleft = c
            has_wall_left = False
            while self.is_settled_or_sand(r, cleft):
                cleft -= 1
                ...

    def flowing(self):
        """While we have springs we need to keep flowing"""
        while self.springs:
            spring = self.springs.pop(0)
            if spring in self.settled_springs:
                continue
            self.settled_springs.add(spring)
            new_springs = self.flow(spring)
        ...

    def __repr__(self) -> str:
        return "\n".join("".join(c for c in row) for row in self.grid)


def part_1(source):
    rr = ReservoirResearch(source)
    # _(rr)
    return rr.flowing()


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
