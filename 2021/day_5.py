#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
"""

import unittest
from collections import defaultdict

from ivonet import read_rows


def count_crossing_lines(grid: defaultdict) -> int:
    """Count all crossing lines in the grid."""
    return sum(i >= 2 for i in grid.values())


def range_maker(starting_point: int, stopping_point: int) -> range:
    """Create a range taking up and down into account"""
    if starting_point > stopping_point:
        return range(starting_point, stopping_point - 1, -1)
    return range(starting_point, stopping_point + 1)


def grid_maker(grid: defaultdict, startx: int, starty: int, stopx: int, stopy: int, diagonal: bool = False):
    """Draws a line in the grid based on the given starting and stopping coordinates.
    You can choose to allow diagonal lines or not.
    """
    if startx == stopx:
        yrange = range_maker(starty, stopy)
        for y in yrange:
            grid[(startx, y)] += 1
    elif starty == stopy:
        xrange = range_maker(startx, stopx)
        for x in xrange:
            grid[(x, starty)] += 1
    elif diagonal:
        xrange = range_maker(startx, stopx)
        yrange = range_maker(starty, stopy)
        for x, y in zip(xrange, yrange):
            grid[(x, y)] += 1


def process_coordinates(data: list[str], diagonal) -> int:
    """Build the grid based on the given data and count the crossing lines."""
    grid = defaultdict(int)
    for row in data:
        start, end = row.split(" -> ")
        start_x, start_y = map(int, start.split(","))
        end_x, end_y = map(int, end.split(","))
        grid_maker(grid, start_x, start_y, end_x, end_y, diagonal=diagonal)
    return count_crossing_lines(grid)


def part_1(data: list[str], diagonal=False):
    return process_coordinates(data, diagonal)


def part_2(data: list[str], diagonal=True):
    return process_coordinates(data, diagonal)


class UnitTests(unittest.TestCase):
    source = read_rows("day_5.txt")

    def test_example_data(self):
        source = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2""".split("\n")
        self.assertEqual(5, part_1(source))
        self.assertEqual(12, part_2(source))

    def test_part_1(self):
        self.assertEqual(5306, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(17787, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
