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


def part_1(data):
    rows = data.split("\n")
    grid = {}
    for row in rows:
        start, end = row.split(" -> ")
        start_x, start_y = map(int, start.split(","))
        end_x, end_y = map(int, end.split(","))
        if not (start_x == end_x or start_y == end_y):
            # print("diagonal:", start_x, start_y, end_x, end_y)
            continue
        step = 1
        if start_x == end_x:
            if start_y > end_y:
                step = -1
            for y in range(start_y, end_y, step):
                grid_adder(grid, start_x, y)
        else:  # start_y == end_y:
            if start_x > end_x:
                step = -1
            for x in range(start_x, end_x, step):
                grid_adder(grid, x, start_y)
        grid_adder(grid, end_x, end_y)
        # print(start_x, start_y, end_x, end_y, grid)
    count = 0
    for value in grid.values():
        if value >= 2:
            count += 1
    return count


def part_2(data):
    rows = data.split("\n")
    grid = {}
    for row in rows:
        start, end = row.split(" -> ")
        start_x, start_y = map(int, start.split(","))
        end_x, end_y = map(int, end.split(","))
        step = 1
        if start_x == end_x:
            if start_y > end_y:
                step = -1
            for y in range(start_y, end_y, step):
                grid_adder(grid, start_x, y)
            grid_adder(grid, end_x, end_y)
        elif start_y == end_y:
            if start_x > end_x:
                step = -1
            for x in range(start_x, end_x, step):
                grid_adder(grid, x, start_y)
            grid_adder(grid, end_x, end_y)
        else:  # diagonale
            pass
        # print(start_x, start_y, end_x, end_y, grid)
    count = 0
    for value in grid.values():
        if value >= 2:
            count += 1
    return count


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
        self.assertEqual(part_2(self.source), 0)


if __name__ == '__main__':
    unittest.main()
