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
import sys
import unittest
from collections import abc, defaultdict
from pathlib import Path

import pyperclip

from ivonet.decorators import debug
from ivonet.decorators import timer
from ivonet.files import read_rows
from ivonet.grid import Location
from ivonet.iter import ints

collections.Callable = abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def parse(source):
    antennas = defaultdict(list)
    grid = []
    for r, line in enumerate(source):
        grid.append(list(line))
        for c, ch in enumerate(line):
            if ch != '.':
                antennas[ch].append(Location(r, c))

    return grid, antennas, len(grid), len(grid[0])


@debug
@timer
def part_1(source) -> int | None:
    answer = antinode_processor(source)
    pyperclip.copy(str(answer))
    return answer


def antinode_processor(source, part2=False):
    answer = set()
    grid, antennas, height, width = parse(source)
    for r in range(height):
        for c in range(width):
            for _, values in antennas.items():  # _ = key unused, vs = values
                for (r1, c1) in values:
                    for (r2, c2) in values:
                        if (r1, c1) != (r2, c2):  # not the same antenna
                            d1 = abs(r - r1) + abs(c - c1)
                            d2 = abs(r - r2) + abs(c - c2)

                            dr1 = r - r1  # delta row
                            dc1 = c - c1  # delta column

                            dr2 = r - r2  # delta row
                            dc2 = c - c2  # delta column
                            if part2:
                                if 0 <= r < height:
                                    if 0 <= c < width:
                                        if dr1 * dc2 == dr2 * dc1:
                                            answer.add((r, c))
                            else:
                                if d1 == 2 * d2 or d1 * 2 == d2:  # must be twice the distance
                                    if 0 <= r < height:  # not above or below the grid
                                        if 0 <= c < width:  # not left or right of the grid
                                            if dr1 * dc2 == dr2 * dc1:
                                                answer.add((r, c))
    if DEBUG:
        for r, c in answer:
            grid[r][c] = '#'
        print("\n".join("".join(row) for row in grid))
    return len(answer)


@debug
@timer
def part_2(source) -> int | None:
    answer = antinode_processor(source, True)
    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(14, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(426, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(34, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(1359, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
