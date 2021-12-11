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

from ivonet.files import read_int_matrix
from ivonet.grid import neighbors

sys.dont_write_bytecode = True


def mp(matrix):
    for h in matrix:
        for w in h:
            if w >= 10:
                print("-", end="")
            else:
                print(w, end="")
        print()
    print()


def step_matrix(source):
    matrix = source.copy()
    height = len(matrix)
    width = len(matrix[0])
    flash_q = []
    for h in range(height):
        for w in range(width):
            matrix[h][w] = matrix[h][w] + 1
            if matrix[h][w] > 9:
                flash_q.append((h, w))
    return matrix, flash_q


def flash(grid, h, w):
    matrix = grid.copy()
    matrix[h][w] += 1
    nb = [x for x in neighbors(matrix, (h, w), diagonal=True)]
    # simultanious flash
    for hh, ww in nb:
        matrix[hh][ww] = matrix[hh][ww] + 1
    for hh, ww in nb:
        if matrix[hh][ww] == 10:
            nb2 = [x for x in neighbors(matrix, (hh, ww), diagonal=True) if matrix[x[0]][x[1]] < 10]
            for hhh, www in nb2:
                flash(matrix, h, w)
    return matrix


def reset_matrix(grid):
    matrix = grid.copy()
    height = len(matrix)
    width = len(matrix[0])
    flashes = 0
    for h in range(height):
        for w in range(width):
            if matrix[h][w] >= 10:
                flashes += 1
                matrix[h][w] = 0
    return matrix, flashes


def part_1(source):
    flashes = 0
    matrix = source.copy()
    for step in range(10):
        print("Step", step + 1)
        matrix, flash_q = step_matrix(matrix)
        mp(matrix)
        # print("!!!", flash_q)
        for h, w in flash_q:
            matrix = flash(matrix, h, w)

        matrix, flashed = reset_matrix(matrix)
        flashes += flashed
        print("Stepped", step + 1)
        mp(matrix)
    return flashes


def part_2(matrix):
    pass


class UnitTests(unittest.TestCase):
    source = read_int_matrix("day_11.txt")
    test_source_1 = read_int_matrix("""11111
19991
19191
19991
11111""")
    test_source = read_int_matrix("""5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526""")

    def test_example_data_part_1(self):
        self.assertEqual(1656, part_1(self.test_source))

    def test_example_data_part_1_small(self):
        self.assertEqual(1656, part_1(self.test_source_1))

    def test_part_1(self):
        self.assertEqual(None, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
