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
    WATER = "|"
    FAUCET = "+"
    GOAL = "G"

    def __repr__(self) -> str:
        return self.value

    def __str__(self) -> str:
        return repr(self)


class Location(NamedTuple):
    row: int
    col: int


class ReservoirResearch:

    def __init__(self, source) -> None:
        self.source = source
        self.rows: int = 0
        self.cols: int = 0
        self.grid = []
        self.init()
        self.faucet = Location(0, 500)
        self.grid[self.faucet.row][self.faucet.col] = Cell.FAUCET

    def init(self):
        start: Callable[[Any], list[list[int]]] = lambda i: [ints(line) for line in self.source if line.startswith(i)]
        y_start = start("y")
        x_start = start("x")
        self.rows = max(max(y_start, key=lambda x: x[0])[0], max(x_start, key=lambda x: x[2])[0])
        self.cols = max(max(y_start, key=lambda x: x[2])[0], max(x_start, key=lambda x: x[0])[0])
        self.grid = [[Cell.SAND for _ in rangei(0, self.cols)] for _ in rangei(0, self.rows)]
        yx = [[y, range(b, c)] for y, b, c in y_start]
        for r, cr in yx:
            for c in cr:
                self.grid[r][c] = Cell.CLAY
        xy = [[x, range(b, c)] for x, b, c in x_start]
        for c, yr in xy:
            for r in yr:
                self.grid[r][c] = Cell.CLAY

    def __repr__(self) -> str:
        return "\n".join("".join(c for c in row) for row in self.grid)


def part_1(source):
    rr = ReservoirResearch(source)
    _(rr)
    return rr


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
