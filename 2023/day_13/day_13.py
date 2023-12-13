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

p1.
123456789
    ><   
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
    ><   
123456789


p2:
1 #...##..# 1
2 #....#..# 2
3 ..##..### 3
4v#####.##.v4
5^#####.##.^5
6 ..##..### 6
7 #....#..# 7

. = ash
# = rock


between line 5 and 6 when mirrored we get a perfect mirror if we ignore the surplus columns to the left

how do we find the perfect mirror? either on col or on row
rulez deduced from the example:
- if we split on columns we need to invert check from the end to the beginning for the left split and from start to end for the right split
- if we split on rows we need to invert check from buttom up for top split and from top down for bottom split
- first check vertically then horizontally
- if we start vertically:
    - starting with 1 col left and in example p1 8 cols to the right
    - we have a perfect mirror if every row in left matches right[0]
    if not we move the left col one to the right and now have 2 cols left and 7 cols right
    - we now have a perfect mirror if left[1]left[0] == right[0]right[1] (reverse left and normal right)
      - the remaining 5 cols do not need to be checked as they fall outside the scopt because left is smaller than right
    - if not we move the left col one to the right and now have 3 cols left and 6 cols right
    - we now have a perfect mirror if left[2]left[1]left[0] == right[0]right[1]right[2] (reverse left and normal right)
      - the remaining 4 cols do not need to be checked as they fall outside the scopt because left is smaller than right
    - if not we move the left col one to the right and now have 4 cols left and 5 cols right
    - we now have a perfect mirror if left[3]left[2]left[1]left[0] == right[0]right[1]right[2]right[3] (reverse left and normal right)
      - the remaining 3 cols do not need to be checked as they fall outside the scopt because left is smaller than right
    - if not we move the left col one to the right and now have 5 cols left and 4 cols right
    - we now have a perfect mirror if left[3]left[2]left[1]left[0] == right[0]right[1]right[2]right[4] (reverse left and normal right)
      - the remaining 2 cols do not need to be checked as they fall outside the scopt because left is smaller than right
      - the difference here is that the right side is now shorter than the left side
      - so we start ignoring a column on the left side
      - that would mean the mirror mirrors to the other side (right to left)
    - if not we move the left col one to the right and now have 6 cols left and 3 cols right
    - we now have a perfect mirror if left[2]left[1]left[0] == right[0]right[1]right[3] (reverse left and normal right)
      - the remaining left cols do not need to be checked as they fall outside the scopt because left is larger than right 
    - and so on until we have 8 cols left and 1 col right
    
    more precise
    - the grid is rows a rectangle of x rows by y cols
    - how to put that into a formula for vertical?
    - for vertical checking:
    - width is len(row)
    - height is len(grid)
    - if col_to_check < width - col_to_check: # left side is smaller than right side 
         - check if left[0:col_to_check][::-1] == right[0:col_to_check] for every row

for r, row in enumerate(grid):
   for c, col in enumerate(row):
      

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


class ValleyOf:
    ASH = '.'  # False / 0
    ROCK = '#'  # True / 1


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
