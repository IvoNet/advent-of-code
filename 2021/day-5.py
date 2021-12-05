#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
"""

import unittest

from ivonet import read_data


def grid_adder(grid, x, y):
    try:
        grid[(x, y)] += 1
    except KeyError:
        grid[(x, y)] = 1


def count_crossing_lines(grid):
    count = 0
    for value in grid.values():
        if value >= 2:
            count += 1
    return count


def grid_maker(grid, startx, starty, stopx, stopy, diagonal=False):
    xrange = range_maker(startx, stopx)
    yrange = range_maker(starty, stopy)

    if startx == stopx:
        for y in yrange:
            grid_adder(grid, startx, y)
    elif starty == stopy:
        for x in xrange:
            grid_adder(grid, x, starty)
    elif diagonal:
        for x, y in zip(xrange, yrange):
            grid_adder(grid, x, y)


def range_maker(startpoint, stoppoint):
    if startpoint > stoppoint:
        return range(startpoint, stoppoint - 1, -1)
    return range(startpoint, stoppoint + 1)


def process_coordinates(data, diagonal):
    rows = data.split("\n")
    grid = {}
    for row in rows:
        start, end = row.split(" -> ")
        start_x, start_y = map(int, start.split(","))
        end_x, end_y = map(int, end.split(","))
        grid_maker(grid, start_x, start_y, end_x, end_y, diagonal=diagonal)
    return count_crossing_lines(grid)


def part_1(data, diagonal=False):
    return process_coordinates(data, diagonal)


def part_2(data, diagonal=True):
    return process_coordinates(data, diagonal)


class UnitTests(unittest.TestCase):
    source = read_data("day-5.txt")

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
5,5 -> 8,2"""
        self.assertEqual(5, part_1(source))
        self.assertEqual(12, part_2(source))

    def test_part_1(self):
        self.assertEqual(5306, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(17787, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
