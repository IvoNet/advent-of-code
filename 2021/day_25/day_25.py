#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """"""

import sys
import unittest
from copy import deepcopy
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints

CUCUMBER_RIGHT = ">"
OPEN_SPACE = "."
CUCUMBER_DOWN = "v"

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def move(sea_floor, cucumber):
    nsf = deepcopy(sea_floor)
    has_moved = False
    rows = len(sea_floor)
    cols = len(sea_floor[0])

    for row in range(rows):
        for col in range(cols):
            if cucumber != sea_floor[row][col]:
                continue
            if sea_floor[row][col] == CUCUMBER_DOWN:
                r = (row + 1) % rows
                c = col
            else:
                r = row
                c = (col + 1) % cols

            if sea_floor[r][c] == OPEN_SPACE:
                nsf[r][c] = sea_floor[row][col]
                nsf[row][col] = OPEN_SPACE
                has_moved = True
    return nsf, has_moved


def visualise(sea_floor):
    str = ""
    for r in sea_floor:
        str += "".join(r)
        str += "\n"
    return str


def part_1(source):
    sea_floor = [list(r) for r in source]
    steps = 0
    while steps < 10000:  # not an endless loop :-)
        sea_floor, has_moved_right = move(sea_floor, CUCUMBER_RIGHT)
        sea_floor, has_moved_down = move(sea_floor, CUCUMBER_DOWN)
        steps += 1
        if not (has_moved_right or has_moved_down):
            _(visualise(sea_floor))
            return steps
    return -1


def part_2(source):
    return 0


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"day_{day.zfill(2)}.input")
        self.test_source = read_rows("""v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>""")

    def test_example_data_part_1(self):
        self.assertEqual(58, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(509, part_1(self.source))


if __name__ == '__main__':
    unittest.main()
