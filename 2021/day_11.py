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
from ivonet.iter import max_2d

sys.dont_write_bytecode = True


def mp(matrix):
    for h in matrix:
        for w in h:
            print(f"{w:<2}", end="")
        print()
    print()


def step_matrix(matrix):
    height = len(matrix)
    width = len(matrix[0])
    flash_q = []
    for h in range(height):
        for w in range(width):
            matrix[h][w] = matrix[h][w] + 1
            if matrix[h][w] > 9:
                flash_q.append((h, w))
    return flash_q


def step_neighbors(matrix, h, w):
    to_flash = []
    nb = [x for x in neighbors(matrix, (h, w), diagonal=True) if matrix[x[0]][x[1]] != 0 and matrix[x[0]][x[1]] < 10]
    for h, w in nb:
        matrix[h][w] += 1
        if matrix[h][w] > 9:
            to_flash.append((h, w))
    return to_flash


def part_1(source):
    flashes = 0
    matrix = source.copy()
    for _ in range(100):
        flashes, matrix = flash_it(flashes, matrix)
    return flashes


def flash_it(flashes, matrix):
    flash_q = step_matrix(matrix)
    while len(flash_q) != 0:
        h, w = flash_q.pop()
        matrix[h][w] = 0
        flashes += 1
        flash_q.extend(step_neighbors(matrix, h, w))
    return flashes, matrix


def part_2(source):
    flashes = 0
    matrix = source.copy()
    running = True
    step = 0
    while running:
        step += 1
        flashes, matrix = flash_it(flashes, matrix)
        if max_2d(matrix) == 0:
            return step
    return flashes


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        self.source = read_int_matrix("day_11.txt")
        self.test_source = read_int_matrix("""5483143223
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

    def test_part_1(self):
        self.assertEqual(1652, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(195, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(220, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
