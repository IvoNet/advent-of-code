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
import unittest
from pathlib import Path

import pyperclip
import sys
from ivonet.decorators import debug
from ivonet.decorators import timer
from ivonet.files import read_rows
from ivonet.grid import Location, neighbor_values
from ivonet.iter import ints

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def get_removable_rolls(grid) -> list[Location]:
    ret = []
    for x, row in enumerate(grid):
        for y, col in enumerate(row):
            if col == "@":
                values = neighbor_values(grid, Location(x, y))
                count = values.count("@")
                if count < 4:
                    ret.append((x, y))
    return ret


def process_rolls_of_paper(source):
    grid = [list(row) for row in source]
    count = 0
    while True:
        removable = get_removable_rolls(grid)
        if not removable:
            break
        count += len(removable)
        for x, y in removable:
            grid[x][y] = "."
    return count


@debug
@timer
def part_1(source) -> int | None:
    grid = [list(row) for row in source]
    answer = len(get_removable_rolls( grid))
    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:
    answer = process_rolls_of_paper( source)
    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(13, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(1395, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(43, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(8451, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = Path(__file__).resolve().parent
        day = f"{ints(Path(__file__).stem)[0]:02}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
