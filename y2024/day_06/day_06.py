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

DEBUG = True

OBSTACLE = ["#", "O"]
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


def parse_source(source):
    grid = [list(row) for row in source]
    for h, row in enumerate(source):
        for w, col in enumerate(row):
            if col in STARTERS:
                start = Location(h, w)
                grid[h][w] = WALKED
                direction_gen = START[col]
                break
    return grid, direction_gen, start


@debug
@timer
def part_1(source) -> int | None:
    answer = 0
    grid, direction_gen, loc = parse_source(source)

    visited = set()
    visited.add(loc)
    for d in direction(direction_gen):
        to = DIRECTION_FUNCTION[d]
        loc, value = next(to(grid, loc, value=True))
        while value not in OBSTACLE:
            visited.add(loc)
            if value == FREE:
                answer += 1
                # grid[loc[0]][loc[1]] = WALKED
            last_loc = loc
            loc, value = next(to(grid, loc, value=True), (None, None))
            if value in OBSTACLE:
                loc = last_loc
            if not loc and not value:
                return len(visited)
                # return sum([row.count(WALKED) for row in grid])


@debug
@timer
def part_2(source) -> int | None:
    """
    So I think that the extra obstacle we need to place must always lead to a parallelogram of obstacles
    That means that the opposite sides of the parallelogram must be parallel and of equal length
    in this case it can not be a square as the turn is 1 before the actual obstacle.
    so it must be a parallelogram with only 1 column off kilter as the loop must be closed
    That would mean possible locations must already have three obstacles in place that adhere to the above
    so how to determine the possible locations?
    look at all obstacles and determine if they are part of an incomplete parallelogram
    so how to do that?
    - find all obstacles
    - iterate over the obstacles
    - it must have at least one obstacle in the grid either 1 row above or below or 1 column left or right
    - but we are looking at the obstacles that have two obstacles 1 row above or below or 1 column left or right
    - then we can determine the 4th obstacle
    kooking at the test_06.input we see that the obstacles are at: (0,4), (1,9), (3,2), (4,7), (6,1), (7,8), (8,0), (9,6)
    - (0,4) has (1,9) one below and x to the right but no other adhering to the rules
    - (1,9) has (0,4) one above and x to the left and (7,8) one to the left and y down. so this is a possible parallelogram
    - what would be the 4th obstacle then? it should be a parallelogram so it must also be one above (7,8) and x to the left (same as (0,4))
    - that would mean (6,4)
    do this for all obstacles, and you have the possible locations
    Some extra rules:
    - the possible location must not be off the border
    - the possible location must not be an obstacle
    - the possible location must not be the start location

    hmm did not work out as expected too many options.

    brute force approach:
    - iterate over all rows then over all cols and change that coord to an obstacle and then see of it looped

    """
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
    loc: Location = start
    visited = set()
    visited.add(((start.row, start.col), direction_gen))
    for d in direction(direction_gen):
        to = DIRECTION_FUNCTION[d]
        loc, value = next(to(grid, loc, value=True))
        while value not in OBSTACLE:
            if (loc, d) in visited:
                return True
            visited.add((loc, d))
            grid[loc[0]][loc[1]] = d
            last_loc = loc
            loc, value = next(to(grid, loc, value=True), (None, None))
            if value in OBSTACLE:
                loc = last_loc
            if not loc and not value:
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
        self.assertEqual(None, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
