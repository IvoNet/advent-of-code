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

from ivonet.grid import transpose

collections.Callable = collections.abc.Callable

import sys

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def p(grid):
    if DEBUG:
        for row in grid:
            print("".join(row))
        print()


def parse(source):
    return [list(row) for row in source]


class SpinCycle:

    def __init__(self, source):
        self.source = source
        self.grid = source

    def flip(self):
        """
        This method performs a flip operation on the grid. The steps are as follows:

        1. Transpose the grid: This is done because it's easier to work with rows than columns.
        2. Sort each group in each row: The grid is iterated row by row. Each row is split into groups by the "#" character.
         Each group is sorted in descending order and then joined back together with the "#" character.
        3. Transpose the grid back: The grid is transposed back to its original orientation.
        4. Calculate and return the score: The score is calculated as the sum of the count of "O" characters in each row,
         multiplied by the difference between the total number of rows and the current row index.

        :return: The score after performing the cycle operation.
        """

        # Transpose the grid because it is easier ti work with rows than cols
        self.grid = transpose(self.grid)

        # Sort each group in each row
        for i in range(len(self.grid)):
            row = "".join(self.grid[i]).split("#")
            sorted_row = []
            for group in row:
                sorted_group = "".join(sorted(list(group), reverse=True))
                sorted_row.append(sorted_group)
            self.grid[i] = "#".join(sorted_row)

        # Transpose the grid back
        self.grid = transpose(self.grid)

        return sum(row.count("O") * (len(self.grid) - r) for r, row in enumerate(self.grid))


def part_1(source):
    return SpinCycle(source).flip()


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""")
        self.test_source2 = read_rows("""""")

    def test_example_data_part_1(self):
        self.assertEqual(136, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(110821, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(64, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
