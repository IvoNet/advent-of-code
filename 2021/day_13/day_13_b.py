#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from collections import defaultdict
from pathlib import Path

from ivonet.files import read_rows
from ivonet.grid import fold_horizontal, fold_vertical, max_width, max_height
from ivonet.iter import ints

sys.dont_write_bytecode = True


def parse(source):
    matrix = defaultdict(int)
    instructions = []
    for line in source:
        if not line:
            continue
        if "," in line:
            matrix[tuple(ints(line))] = 1
            continue
        if "fold" in line:
            i = line.split("fold along ")[1]
            d, value = i.split("=")
            instructions.append((d, int(value)))
    return matrix, instructions, max_width(matrix), max_height(matrix)


def print_matrix(matrix, grid=(99, 90), end="", console=False):
    ret = []
    for y in range(grid[1]):
        row = []
        for x in range(grid[0]):
            try:
                row.append(matrix[(x, y)])
                if console:
                    print("#" if matrix[(x, y)] == 1 else " ", end=end)
            except KeyError:
                print(f"key error x={x}, y={y}")
        if console:
            print()
        ret.append(row)
    return ret


def part_1(source):
    matrix, instructions, max_w, max_h = parse(source)
    i, v = instructions[0]
    if i == "y":
        matrix = fold_horizontal(matrix, v)
        max_h = v
    else:  # x
        matrix = fold_vertical(matrix, v)
        max_w = v
    total = 0
    for x in range(max_w):
        for y in range(max_h):
            total += matrix[(x, y)]
    return total


def part_2(source):
    matrix, instructions, max_w, max_h = parse(source)
    for i, v in instructions:
        if i == "y":
            matrix = fold_horizontal(matrix, v)
            max_h = v
        else:
            matrix = fold_vertical(matrix, v)
            max_w = v
    print("-" * 50)
    print_matrix(matrix, grid=(max_w, max_h), console=True)
    print("-" * 50)
    return "FJAHJGAH"


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}.input")))
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
