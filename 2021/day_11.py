#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import sys
from pprint import pprint
from queue import Queue

from ivonet.files import read_int_matrix

sys.dont_write_bytecode = True

import unittest


def step_matrix(source):
    matrix = source.copy()
    height = len(matrix)
    width = len(matrix[0])
    flash_q = Queue()
    for h in range(height):
        for w in range(width):
            matrix[h][w] = matrix[h][w] + 1
            if matrix[h][w] > 9:
                flash_q.put((h, w))
    return matrix, flash_q


def part_1(source):
    flashes = 0
    matrix = source.copy()
    height = len(matrix)
    width = len(matrix[0])
    for step in range(100):
        matrix, flash_q = step_matrix(matrix)
        pprint(matrix)
        while not flash_q.empty():
            h, w = flash_q.get()
            nb =


def part_2(matrix):
    pass


class UnitTests(unittest.TestCase):
    source = read_int_matrix("day_11.txt")
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

    def test_part_1(self):
        self.assertEqual(None, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
