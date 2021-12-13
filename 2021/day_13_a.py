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
from pathlib import Path

from ivonet.files import read_rows
from ivonet.grid import Matrix
from ivonet.iter import ints

sys.dont_write_bytecode = True


def parse(source) -> (Matrix, list):
    matrix = Matrix()
    instructions = []
    for line in source:
        if "," in line:
            matrix[tuple(ints(line))] = 1
            continue
        if "=" in line:
            d, value = line.replace("fold along ", "").split("=")
            instructions.append((d, int(value)))
    return matrix, instructions


def part_1(source):
    matrix, instructions = parse(source)
    i, v = instructions[0]
    if i == "y":
        matrix = matrix.fold_horizontal(v)
    else:  # x
        matrix = matrix.fold_vertical(v)
    return matrix.total()


def part_2(source):
    matrix, instructions = parse(source)
    for i, v in instructions:
        if i == "y":
            matrix = matrix.fold_horizontal(v)
        else:
            matrix = matrix.fold_vertical(v)
    matrix.print()
    return "FJAHJGAH"


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = ints(Path(__file__).name)[0]
        self.source = read_rows(f"day_{day}.txt")
        self.test_source = read_rows("""6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5""")

    def test_example_data_part_1(self):
        self.assertEqual(17, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(785, part_1(self.source))

    def test_part_2(self):
        self.assertEqual("FJAHJGAH", part_2(self.source))


if __name__ == '__main__':
    unittest.main()
