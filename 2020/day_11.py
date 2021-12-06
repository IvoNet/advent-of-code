#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import unittest
from itertools import product

from more_itertools import chunked

from ivonet import get_data

EMPTY = 0
FILLED = 1
GROUND = -1
NEIGHBORS = [x for x in product([-1, 0, 1], repeat=2) if x != (0, 0)]


def parse(data):
    matrix = {}
    for y, row in enumerate(data):
        for x, col in enumerate(row):
            matrix[(x, y)] = 0 if col == 'L' else -1
    return matrix


def neighbors(coord: tuple, grid=(99, 90)):
    width = grid[0] - 1
    height = grid[1] - 1
    retx, rety = coord
    adjacent = []
    for x, y in NEIGHBORS:
        xx = retx + x
        yy = rety + y
        if xx < 0 or xx > width or yy < 0 or yy > height:
            # not in boundaries
            continue
        adjacent.append((xx, yy))
    return adjacent


def print_matrix_0(matrix, width=99):
    printable = []
    for x in matrix.values():
        if x == -1:
            printable.append(".")
        elif x == 0:
            printable.append("L")
        else:
            printable.append("#")
    printer = chunked(printable, width)
    for x in printer:
        print("".join(x))


def print_matrix(matrix, grid=(99, 90)):
    for y in range(grid[0]):
        for x in range(grid[1]):
            try:
                value = matrix[(x, y)]
                if value == -1:
                    print(".", end="")
                elif value == 0:
                    print("L", end="")
                else:
                    print("#", end="")
            except KeyError:
                print(f"key error x={x}, y={y}")
        print()


def part_1(data, grid=(99, 90)):
    matrix = parse(data)
    # apply_rules(matrix)
    temp_matrix = matrix.copy()
    running = True
    while running:
        for coord in matrix:
            occupied = 0
            for nb in neighbors(coord, grid):
                try:
                    seat = matrix[nb]
                    if seat == 1:
                        occupied += 1
                except KeyError:
                    pass
            if not matrix[coord] and not occupied:
                # print("occupying:", str(coord))
                temp_matrix[coord] = 1
            elif matrix[coord] and occupied >= 4:
                # print("leaving:", str(coord))
                temp_matrix[coord] = 0
        if temp_matrix == matrix:
            running = False
            # print("same")
            # print(matrix)
            # pprint(temp_matrix)
        matrix = temp_matrix
        print_matrix(matrix, grid)
    return sum(1 for x in matrix.values() if x == 1)


def part_2(data):
    pass


class UnitTests(unittest.TestCase):
    source = get_data("day_11.txt")
    test_source = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL""".split("\n")

    def test_example_data_part_1(self):
        self.assertEqual(37, part_1(self.test_source, (10, 10)))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_1(self):
        self.assertEqual(None, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
