#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import unittest
from copy import deepcopy
from itertools import product

from ivonet.files import read_rows

EMPTY = 0
FILLED = 1
GROUND = -1
NEIGHBORS = [x for x in product([-1, 0, 1], repeat=2) if x != (0, 0)]


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


def parse(data):
    matrix = {}
    for y, row in enumerate(data):
        for x, col in enumerate(row):
            matrix[(x, y)] = 0 if col == 'L' else -1
    return matrix


def print_matrix(matrix, grid=(99, 90), end=""):
    for y in range(grid[1]):
        for x in range(grid[0]):
            try:
                value = matrix[(x, y)]
                if value == -1:
                    print(".", end=end)
                elif value == 0:
                    print("L", end=end)
                else:
                    print("#", end=end)
            except KeyError:
                print(f"key error x={x}, y={y}")
        print()


def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    shared_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o: (d1[o], d2[o]) for o in shared_keys if d1[o] != d2[o]}
    same = set(o for o in shared_keys if d1[o] == d2[o])
    return added, removed, modified, same


def part_1(data, grid=(99, 90)):
    matrix = parse(data)
    running = True
    idx = 0
    print(f"Iteration: {idx}")
    # print_matrix(matrix, grid)
    while running:
        temp_matrix = deepcopy(matrix)
        idx += 1
        for coord in matrix:
            if matrix[coord] == -1:
                continue
            occupied = 0
            for nb in neighbors(coord, grid):
                try:
                    seat = matrix[nb]
                    if seat == 1:
                        occupied += 1
                except KeyError:
                    pass
            if matrix[coord] == 0 and occupied == 0:
                temp_matrix[coord] = 1
            if matrix[coord] == 1 and occupied >= 4:
                temp_matrix[coord] = 0
        if temp_matrix == matrix:
            running = False
            print(f"Iteration: {idx}")
            print_matrix(matrix, grid)
            # print(dict_compare(matrix, temp_matrix))
        matrix = temp_matrix
    return sum(1 for x in matrix.values() if x == 1)


def part_2(data, grid=(99, 90)):
    matrix = parse(data)
    running = True
    idx = 0
    print(f"Iteration: {idx}")
    # print_matrix(matrix, grid)
    while running:
        temp_matrix = deepcopy(matrix)
        idx += 1
        for coord in matrix:
            if matrix[coord] == -1:
                continue
            occupied = 0
            for nb in neighbors(coord, grid):
                try:
                    seat = matrix[nb]
                    if seat == 1:
                        occupied += 1
                except KeyError:
                    pass
            if matrix[coord] == 0 and occupied == 0:
                temp_matrix[coord] = 1
            if matrix[coord] == 1 and occupied >= 5:
                temp_matrix[coord] = 0
        if temp_matrix == matrix:
            running = False
            # print(dict_compare(matrix, temp_matrix))
        matrix = temp_matrix
        print(f"Iteration: {idx}")
        print_matrix(matrix, grid)
    return sum(1 for x in matrix.values() if x == 1)


class UnitTests(unittest.TestCase):
    source = read_rows("day_11.txt")
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
        self.assertEqual(37, part_1(self.test_source, grid=(10, 10)))

    def test_example_data_part_2(self):
        self.assertEqual(26, part_2(self.test_source, grid=(10, 10)))

    def test_part_1(self):
        self.assertEqual(2324, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
