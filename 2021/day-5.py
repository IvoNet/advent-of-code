#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
"""

import sys
import unittest

from ivonet import read_data


def get_line(startx, starty, endx, endy):
    coords = []


def grid_adder(grid, x, y):
    try:
        grid[(x, y)] += 1
    except KeyError:
        grid[(x, y)] = 1


def parse(data):
    rows = data.split("\n")
    grid = {}
    for row in rows:
        start, end = row.split(" -> ")
        start_x, start_y = map(int, start.split(","))
        end_x, end_y = map(int, end.split(","))
        if not (start_x == end_x or start_y == end_y):
            print("diagonal:", start_x, start_y, end_x, end_y)
            continue
        if start_x == end_x:
            for y in range(start_y, end_y):
                grid_adder(grid, start_x, y)
        else:  # start_y == end_y
            for x in range(start_x, end_x):
                grid_adder(grid, x, start_y)
        grid_adder(grid, end_x, end_y)
        print(start_x, start_y, end_x, end_y, grid)
    count = 0
    for value in grid.values():
        if value >= 2:
            count += 1
    print(grid.values())
    print(count)
    sys.exit(1)
    return count


def part_1(data):
    return parse(data)


def part_2(data):
    pass


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
        self.assertEqual(part_1(source), 5)
        self.assertEqual(part_2(source), None)

    def test_part_1(self):
        self.assertEqual(part_1(self.source), 0)

    def test_part_2(self):
        self.assertEqual(part_2(self.source), 0)


if __name__ == '__main__':
    unittest.main()
