#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from copy import deepcopy
from pathlib import Path

from ivonet.files import read_rows
from ivonet.grid import neighbors
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def flip_lights(source):
    matrix = deepcopy(source)
    for h, row in enumerate(source):
        for w, col in enumerate(row):
            nb_on = sum(1 for x, y in neighbors(source, (h, w), diagonal=True) if source[x][y] == "#")
            if source[h][w] == "#":
                if nb_on not in [2, 3]:
                    matrix[h][w] = "."
            else:  # of
                if nb_on == 3:
                    matrix[h][w] = "#"
    return matrix


def count_lights(matrix):
    return sum(1 for h, row in enumerate(matrix) for w, col in enumerate(row) if matrix[h][w] == "#")


def part_1(source, steps=100):
    matrix = [list(row) for row in source]
    for _ in range(steps):
        matrix = flip_lights(matrix)
    return count_lights(matrix)


def part_2(source):
    return 0


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"day_{day.zfill(2)}.input")
        self.test_source = read_rows(""".#.#.#
...##.
#....#
..#...
#.#..#
####..""")

    def test_example_data_part_1(self):
        self.assertEqual(4, part_1(self.test_source, steps=4))

    def test_part_1(self):
        self.assertEqual(None, part_1(self.source, steps=100))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
