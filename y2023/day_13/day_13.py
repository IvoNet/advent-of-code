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
from typing import Any

from ivonet.grid import transpose

collections.Callable = collections.abc.Callable

import sys

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def parse(source) -> list[list[list[Any]]]:
    grids = []
    for block in source.split("\n\n"):
        grid = []
        for row in block.split("\n"):
            grid.append(list(row))
        grids.append(grid)
    return grids


def mirror_loc(grid: list[list[str]]) -> int:
    """
    This function finds the row index where the top and bottom halves of the grid mirror each other.
    If no such row is found, it returns 0.

    :param grid: A 2D list of strings representing the grid.
    :return: The row index where the top and bottom halves of the grid mirror each other.
    """
    row_index: int
    for row_index in range(1, len(grid)):
        bottom, top = extract_top_bottom(grid, row_index)

        if top == bottom:
            return row_index
    return 0


def extract_top_bottom(grid: list[list[str]], row_index: int) -> tuple[list[list[str]], list[list[str]]]:
    """
    This function extracts the top and bottom halves of the grid at the given row index.
    The top half is reversed to facilitate mirror checking.

    :param grid: A 2D list of strings representing the grid.
    :param row_index: The index at which to split the grid.
    :return: A tuple containing the top and bottom parts of same size of the grid.
    """
    top: list[list[str]] = grid[:row_index][::-1]
    bottom: list[list[str]] = grid[row_index:]

    # Make sure the top and bottom halves are the same size
    top = top[:len(bottom)]
    bottom = bottom[:len(top)]
    return bottom, top


def mirror_loc_smudged(grid: list[list[str]]) -> int:
    """
    This function finds the row index where the top and bottom halves of the grid mirror each other,
    allowing for a single discrepancy (smudge). If no such row is found, it returns 0.

    :param grid: A 2D list of strings representing the grid.
    :return: The row index where the top and bottom halves of the grid mirror each other.
    """
    for row_index in range(1, len(grid)):
        bottom, top = extract_top_bottom(grid, row_index)

        # Calculate the number of discrepancies between the top and bottom halves
        discrepancies = 0
        for i in range(len(top)):
            for j in range(len(top[i])):
                if top[i][j] != bottom[i][j]:
                    discrepancies += 1

        # If there's only one discrepancy, return the current row index
        if discrepancies == 1:
            return row_index
    return 0


def process(source: str, func: callable) -> int:
    """
    This function processes the source string with the provided function.
    It parses the source into grids, applies the function to each grid, and sums the results.

    :param source: A string representing the source data.
    :param func: A function to apply to each grid.
    :return: The sum of the results of applying the function to each grid.
    """
    total: int = 0
    for grid in parse(source):
        horizontal: int = func(grid)
        vertical: int = func(transpose(grid))
        total += horizontal * 100 + vertical
    return total


def part_1(source):
    return process(source, func=mirror_loc)


def part_2(source):
    return process(source, func=mirror_loc_smudged)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_data("""#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""")
        self.test_source2 = read_data("""""")

    def test_example_data_part_1(self):
        self.assertEqual(405, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(29846, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(400, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(25401, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
