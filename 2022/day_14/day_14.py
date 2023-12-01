#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2022 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
If a part of the code is not part of the post it is probably 
code I found reusable and I may have moved it to my 'ivonet' library.
you can find that here: https://github.com/IvoNet/advent-of-code/tree/master/ivonet
"""

import os
import unittest
from pathlib import Path

import sys

from ivonet.files import read_rows
from ivonet.grid import Matrix
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def create_matrix(source):
    """Create a matrix with the source data.
    Every line of the source represents a line of rocks in the matrix.
    The rocks are represented by 1's and the empty spaces with 0's.
    """
    matrix = Matrix()
    for line in source:
        previous = None
        for dot in line.split(" -> "):
            col, row = ints(dot)
            if previous:
                delta_col = col - previous[0]
                delta_row = row - previous[1]
                length = max(abs(delta_col), abs(delta_row))
                for i in range(length + 1):
                    c = previous[0] + i * (1 if delta_col > 0 else (-1 if delta_col < 0 else 0))
                    r = previous[1] + i * (1 if delta_row > 0 else (-1 if delta_row < 0 else 0))
                    matrix[c, r] = 1
            previous = (col, row)
    return matrix


def part_1(source, part2=False):
    matrix = create_matrix(source)
    floor = matrix.max_h + 2
    _("floor:", floor)
    _("max_width:", matrix.max_w)
    for x in range(0, matrix.max_w + 200):
        matrix[x, floor] = 1
    if DEBUG:
        matrix.print()
    i = 0
    while True:
        col, row = (500, 0)
        while True:
            if row + 1 >= floor and not part2:
                if DEBUG:
                    matrix.print_sand()
                return i
            if matrix[col, row + 1] == 0:
                row += 1
            elif matrix[col - 1, row + 1] == 0:
                col -= 1
                row += 1
            elif matrix[col + 1, row + 1] == 0:
                col += 1
                row += 1
            else:
                break
        matrix[(col, row)] = 2
        i += 1
        if col == 500 and row == 0:
            if DEBUG:
                matrix.print_sand()
            return i


def part_2(source):
    return part_1(source, True)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9""")

    def test_example_data_part_1(self):
        self.assertEqual(24, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(793, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(93, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(24166, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
