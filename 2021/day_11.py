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

PREVENT_ENDLESS_LOOP = 1000

sys.dont_write_bytecode = True


def mp(matrix, width=1):
    for h in matrix:
        for w in h:
            print(f"{w:<{width}}", end="")
        print()
    print()


def step_matrix(matrix):
    """Steps the complete matrix and creates a flash list"""
    height = len(matrix)
    width = len(matrix[0])
    to_flash = []
    for h in range(height):
        for w in range(width):
            matrix[h][w] = matrix[h][w] + 1
            if matrix[h][w] > 9:
                to_flash.append((h, w))
    return to_flash


def step_neighbors(matrix, h, w):
    """Steps the neighbors of a flash and create a flash queue following these steps
    - Neighbors can only step if they did not do it yet or have not jet passed the threshold of 9
    - Neighbors that reach the threshold of >9 are added to the to_flash list and returned for later
      processing
    """
    to_flash = []
    for h, w in [x for x in neighbors(matrix, (h, w), diagonal=True) if
                 matrix[x[0]][x[1]] != 0 and matrix[x[0]][x[1]] < 10]:
        matrix[h][w] += 1
        if matrix[h][w] > 9:
            to_flash.append((h, w))
    return to_flash


def flash_it(matrix):
    """Do one full iteration of a flash step.
    - start with incrementing all positions
    - while the flash list has items
        - reset the octopus
        - increment the flashes count
        - step its neighbors and extend the flash list if those had flash-ables in there
    - give back the totals
    """
    to_flash = step_matrix(matrix)
    flashes = 0
    while len(to_flash) != 0:
        h, w = to_flash.pop()
        matrix[h][w] = 0
        flashes += 1
        to_flash.extend(step_neighbors(matrix, h, w))
    return flashes


def part_1(matrix):
    flashes = 0
    for _ in range(100):
        flashes += flash_it(matrix)
    print("Flashes:", flashes)
    mp(matrix)
    return flashes


def part_2(matrix):
    step = 0
    while step < PREVENT_ENDLESS_LOOP:  # Change this constant if you need more iterations
        step += 1
        flash_it(matrix)
        if max_2d(matrix) == 0:
            print("Step:", step)
            mp(matrix)
            return step
    raise ValueError("Too many iterations")


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
