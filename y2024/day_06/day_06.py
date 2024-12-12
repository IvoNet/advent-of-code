#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2023 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
If a part of the code is not part of the post it is probably 
code I found reusable and I may have moved it to my 'ivonet' library.
you can find that here: https://github.com/IvoNet/advent-of-code/tree/master/ivonet
"""

import collections
import os
import unittest
from pathlib import Path

import pyperclip
import sys

from ivonet.decorators import debug
from ivonet.decorators import timer
from ivonet.files import read_rows
from ivonet.grid import north, east, south, west, Location
from ivonet.iter import ints

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True

OBSTACLE = "#"
FREE = "."
STARTERS = "^>v<"
WALKED = "X"
START = {
    "^": "N",
    ">": "E",
    "v": "S",
    "<": "W",
}

NEXT_DIRECTION = {
    "N": "E",
    "E": "S",
    "S": "W",
    "W": "N",
}

DIRECTION_FUNCTION = {
    "N": north,
    "E": east,
    "S": south,
    "W": west,
}


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def direction(start):
    while True:
        yield start
        start = NEXT_DIRECTION[start]




@debug
@timer
def part_1(source) -> int | None:
    grid = [list(row) for row in source]
    answer = 0
    loc: Location
    direction_gen: str
    for h, row in enumerate(source):
        for w, col in enumerate(row):
            if col in STARTERS:
                loc = Location(h, w)
                grid[h][w] = WALKED
                direction_gen = START[col]
                break

    for d in direction(direction_gen):
        to = DIRECTION_FUNCTION[d]
        loc, value = next(to(grid, loc, value=True))
        while value != OBSTACLE:
            if value == FREE:
                answer += 1
                grid[loc[0]][loc[1]] = WALKED
            last_loc = loc
            loc, value = next(to(grid, loc, value=True), (None, None))
            if value == OBSTACLE:
                loc = last_loc
            if not loc and not value:
                for row in grid:
                    print("".join(row))

                return sum([row.count(WALKED) for row in grid])






    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:
    answer = 0
    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(41, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(5153, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(None, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
