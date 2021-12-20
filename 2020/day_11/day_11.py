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

from ivonet.files import read_rows
from ivonet.grid import neighbors_defined_grid, directions

OCCUPIED_SEAT = '#'
EMPTY_SEAT = 'L'
GROUND = "."


def parse(data):
    matrix = {}
    for y, row in enumerate(data):
        for x, col in enumerate(row):
            matrix[(y, x)] = col
    return matrix


def print_matrix(matrix, grid=(99, 90), end=""):
    for y in range(grid[1]):
        for x in range(grid[0]):
            try:
                print(matrix[(x, y)], end=end)
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


def part_1(data):
    height = len(data)
    width = len(data[0])
    grid = (height, width)
    matrix = parse(data)
    running = True
    idx = 0
    while running:
        temp_matrix = deepcopy(matrix)
        idx += 1
        for coord in matrix:
            if matrix[coord] == GROUND:
                continue
            occupied = 0
            for nb in neighbors_defined_grid(coord, grid):
                seat = matrix[nb]
                if seat == OCCUPIED_SEAT:
                    occupied += 1
            if matrix[coord] == EMPTY_SEAT and occupied == 0:
                temp_matrix[coord] = OCCUPIED_SEAT
            if matrix[coord] == OCCUPIED_SEAT and occupied >= 4:
                temp_matrix[coord] = EMPTY_SEAT
        if temp_matrix == matrix:
            running = False
            print(f"Iteration: {idx}")
            print_matrix(matrix, grid)
        matrix = temp_matrix
    return sum(1 for x in matrix.values() if x == OCCUPIED_SEAT)


def part_2(data):
    height = len(data)
    width = len(data[0])
    grid = (height, width)
    matrix = parse(data)
    running = True
    idx = 0
    while running:
        idx += 1
        temp_matrix = deepcopy(matrix)
        for coord in matrix:
            if matrix[coord] == GROUND:
                continue
            occupied = 0
            dirs = directions(data, coord)
            for compass in dirs:
                for crd in dirs[compass]:
                    place = matrix[crd]
                    if place == GROUND:
                        continue
                    if place == OCCUPIED_SEAT:
                        occupied += 1
                        break
                    if place == EMPTY_SEAT:
                        break
            if matrix[coord] == EMPTY_SEAT and occupied == 0:
                temp_matrix[coord] = OCCUPIED_SEAT
            if matrix[coord] == OCCUPIED_SEAT and occupied >= 5:
                temp_matrix[coord] = EMPTY_SEAT
        if temp_matrix == matrix:
            running = False
            print(f"Iteration: {idx}")
            print_matrix(matrix, grid)
            # print(dict_compare(matrix, temp_matrix))
        matrix = temp_matrix
    return sum(1 for x in matrix.values() if x == OCCUPIED_SEAT)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        self.source = read_rows("day_11.input")
        self.test_source = read_rows("""L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL""")

    def test_example_data_part_1(self):
        self.assertEqual(37, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(2324, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(26, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(2068, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
