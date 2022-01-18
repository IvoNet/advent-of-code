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

from ivonet.files import read_ints, read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Coord(NamedTuple):
    c: int
    r: int


def hundreds_digit(nr: int) -> int:
    if nr < 100:
        return 0
    return int(str(nr // 100)[-1])


def power_level(loc: Coord, grid_serial_nr=8868, plus=10):
    rack_id = loc.c + plus
    return hundreds_digit(((rack_id * loc.r) + grid_serial_nr) * rack_id) - 5


def part_1(source, width=300, height=300):
    return None


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_ints(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")[0]
        self.test_source = read_data("""""")

    def test_hundreds(self):
        self.assertEqual(9, hundreds_digit(949))
        self.assertEqual(7, hundreds_digit(123456789))
        self.assertEqual(0, hundreds_digit(99))
        self.assertEqual(1, hundreds_digit(100))

    def test_power_level(self):
        self.assertEqual(-5, power_level(Coord(122, 79), grid_serial_nr=57))
        self.assertEqual(0, power_level(Coord(217, 196), grid_serial_nr=39))
        self.assertEqual(4, power_level(Coord(101, 153), grid_serial_nr=71))

    def test_example_data_part_1(self):
        self.assertEqual(None, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(None, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
