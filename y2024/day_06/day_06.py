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
from copy import deepcopy
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

DEBUG = False

OBSTACLE = ["#", "O"]
FREE = "B"
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


def parse_source(source):
    grid = [list(row.replace(".", "B")) for row in source]
    for h, row in enumerate(source):
        for w, col in enumerate(row):
            if col in STARTERS:
                start = (h, w)
                grid[h][w] = WALKED
                direction_gen = START[col]
                break
    return grid, direction_gen, start


@debug
@timer
def part_1(source) -> int | None:
    answer = 0
    grid, direction_gen, start = parse_source(source)

    visited = set()
    visited.add(start)
    loc = Location(*start)
    for d in direction(direction_gen):
        to = DIRECTION_FUNCTION[d]
        loc, value = next(to(grid, loc, value=True))
        while value not in OBSTACLE:
            visited.add(loc)
            if value == FREE:
                answer += 1
                grid[loc[0]][loc[1]] = WALKED
            last_loc = loc
            loc, value = next(to(grid, loc, value=True), (None, None))
            if value in OBSTACLE:
                loc = last_loc
            if not loc and not value:
                return len(visited)



@debug
@timer
def part_2(source) -> int | None:
    answer = 0
    grid, direction_gen, loc = parse_source(source)

    for h, row in enumerate(grid):
        for w, col in enumerate(row):
            if col != FREE:
                continue
            grid[h][w] = "O"
            if looped(direction_gen, deepcopy(grid), loc):
                answer += 1
            grid[h][w] = "."

    pyperclip.copy(str(answer))
    return answer


def looped(direction_gen: str, grid: list[list[str]], start: Location):
    loc = start
    visited = set()
    visited.add((start, direction_gen))
    for d in direction(direction_gen):

        to = DIRECTION_FUNCTION[d]
        last_loc = loc
        loc, value = next(to(grid, loc, value=True))
        if value in OBSTACLE:
            loc = last_loc
        while value not in OBSTACLE:
            if (loc, d) in visited:
                p(visited)
                if DEBUG:
                    for row in grid:
                        p("".join(row))
                return True
            visited.add((loc, d))
            grid[loc[0]][loc[1]] = d
            last_loc = loc
            loc, value = next(to(grid, loc, value=True), (None, None))
            if value in OBSTACLE:
                loc = last_loc
            if not loc and not value:
                if DEBUG:
                    for row in grid:
                        p("".join(row))
                return False


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(41, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(5153, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(6, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(1711, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
