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

from ivonet.files import read_data
from ivonet.iter import ints, rangei

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class PowerGrid:
    """Implemented in a class as to save state like a cache and the serial number and not having to pass them around
    ugly like"""

    def __init__(self, serial_number=8868, grid_size=300) -> None:
        self.grid_size = grid_size
        self.serial = int(serial_number)
        self.cache = defaultdict(int)
        self.sa = self.cache_area(rangei(1, self.grid_size))

    def power_level(self, loc: tuple[int, int]):
        """The actual power grid rules"""
        x, y = loc
        rack_id = x + 10
        level = (rack_id * y + self.serial) * rack_id
        return (level // 100) % 10 - 5

    def cache_area(self, side):
        """A table of areas already summed up
        - build a cached power grid by calculating what is new and adding what was behind
        """
        for x, y in list(product(side, side)):
            self.cache[x, y] = self.power_level((x, y)) + \
                               self.cache[x, y - 1] + self.cache[x - 1, y] - self.cache[x - 1, y - 1]
        return self.cache

    def total_power(self, top_left, size=3):
        """Total power calculated from the top left corner of a size*size"""
        x, y = top_left
        x_min, y_min, x_max, y_max = x - 1, y - 1, x + size - 1, y + size - 1
        return self.sa[x_min, y_min] + self.sa[x_max, y_max] - self.sa[x_max, y_min] - self.sa[x_min, y_max]

    def max_power(self, size=3):
        top_lefts = product(rangei(1, self.grid_size - size), repeat=2)
        return max((self.total_power(top_left, size), top_left, size) for top_left in top_lefts)

    def max_power_any_size(self):
        """Get the max power level of any size square within the grid"""
        return max(self.max_power(size=x) for x in range(300))


def part_1(source):
    total, top_left, size = PowerGrid(source).max_power()
    return ",".join(str(a) for a in top_left)


def part_2(source):
    total, top_left, size = PowerGrid(source).max_power_any_size()
    x, y = top_left
    return ",".join(str(a) for a in [x, y, size])


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")

    def test_example_data_part_1(self):
        self.assertEqual("33,45", part_1(18))

    def test_example_data_2_part_1(self):
        self.assertEqual("21,61", part_1(42))

    def test_part_1(self):
        self.assertEqual("241,40", part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual("90,269,16", part_2(18))

    def test_example_data_2_part_2(self):
        self.assertEqual("232,251,12", part_2(42))

    def test_part_2(self):
        self.assertEqual("166,75,12", part_2(self.source))


if __name__ == '__main__':
    unittest.main()
