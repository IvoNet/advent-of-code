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
from collections import defaultdict
from itertools import product
from pathlib import Path
from typing import NamedTuple, Iterable, Optional

from ivonet import infinite
from ivonet.files import read_data
from ivonet.iter import ints, rangei

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Coord(NamedTuple):
    x: int
    y: int


def power_level(loc: tuple[int, int], grid_serial_nr=8868):
    x, y = loc
    rack_id = x + 10
    level = (rack_id * y + grid_serial_nr) * rack_id
    return (level // 100) % 10 - 5


def grid_iter(width=300, height=300, size=3):
    for r in rangei(1, height - size):
        for c in rangei(1, width - size):
            yield range(r, r + size), range(c, c + size)


def total_power_v1(rows: Iterable, cols: Iterable, grid_serial_nr) -> int:
    return sum(power_level(Coord(r, c), grid_serial_nr) for r in rows for c in cols)


def total_power(top_left: tuple[int, int], size=3):
    x, y = top_left
    square = product(range(x, x + size), range(y, y + size))
    return sum(map(power_level, square))


def summed_area(side, key):
    "A summed-area table."
    sa = defaultdict(int)
    for x, y in product(side, side):
        sa[x, y] = key((x, y)) + sa[x, y - 1] + sa[x - 1, y] - sa[x - 1, y - 1]
    return sa


class PowerGrid:

    def __init__(self, serial_number=8868) -> None:
        self.width = 300
        self.height = 300
        self.serial = int(serial_number)
        self.grid = [[power_level(Coord(c, r), self.serial) for c in rangei(0, self.width)]
                     for r in rangei(0, self.height)]
        self.highest = -infinite
        self.top_x = 0
        self.top_y = 0
        self.size = 0

    def total_power_v1(self, rows: Iterable, cols: Iterable) -> int:
        return sum(self.grid[r][c] for r in rows for c in cols)

    def highest_power(self):
        """First version"""
        highest: int = -infinite
        top_left: Optional[Coord] = None
        for rows, cols in grid_iter():
            power = self.total_power_v1(rows, cols)
            if power > highest:
                top_left = Coord(cols[0], rows[0])
                highest = power
        return top_left

    def total_power_v2(self, top_left: tuple[int, int], size=3):
        x, y = top_left
        square = product(range(x, x + size), range(y, y + size))
        return sum(map(power_level, square))

    def max_power(self, size=3):
        top_lefts = product(rangei(1, self.width - size), repeat=2)
        return max((self.total_power(top_left, size), top_left, size) for top_left in top_lefts)

    def highest_any_grid(self):
        highest: int = -infinite
        top_left: Optional[Coord] = None
        top_grid_size: int = -infinite
        for size in rangei(300, 1, -1):
            for rows, cols in grid_iter(size=size):
                power = self.total_power(rows, cols)
                if power > highest:
                    top_left = Coord(r=rows[0], c=cols[0])
                    highest = power
                    top_grid_size = size
                    _(size, highest, top_left)
        return top_left.x, top_left.y, top_grid_size

    def total_power(self, topleft, width=3, sa=summed_area(rangei(1, 300), power_level)):
        "Total power in square with given topleft corner and width (from `sa`)."
        x, y = topleft
        xmin, ymin, xmax, ymax = x - 1, y - 1, x + width - 1, y + width - 1
        return sa[xmin, ymin] + sa[xmax, ymax] - sa[xmax, ymin] - sa[xmin, ymax]


def part_1(source):
    # return PowerGrid(source).highest_power()
    return PowerGrid(source).max_power()[1]


def part_2(source):
    """Way to slow :-) But how to optimize?
    - caching? precalculating?
    """
    return PowerGrid(source).highest_any_grid()


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")

    def test_hundreds(self):
        self.assertEqual(9, hundreds_digit(949))
        self.assertEqual(7, hundreds_digit(123456789))
        self.assertEqual(0, hundreds_digit(99))
        self.assertEqual(1, hundreds_digit(100))

    def test_power_level(self):
        self.assertEqual(-5, power_level(Coord(c=122, r=79), grid_serial_nr=57))
        self.assertEqual(0, power_level(Coord(c=217, r=196), grid_serial_nr=39))
        self.assertEqual(4, power_level(Coord(c=101, r=153), grid_serial_nr=71))

    def test_example_data_part_1(self):
        self.assertEqual((33, 45), part_1(18))

    def test_example_data_2_part_1(self):
        self.assertEqual((21, 61), part_1(42))

    def test_part_1(self):
        self.assertEqual((241, 40), part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual((90, 269, 16), part_2(18))

    def test_example_data_2_part_2(self):
        self.assertEqual((21, 61), part_2(42))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
