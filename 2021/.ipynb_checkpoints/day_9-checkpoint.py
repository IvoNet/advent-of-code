#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import sys

from ivonet.calc import prod
from ivonet.files import read_int_matrix
from ivonet.grid import neighbors
from ivonet.iter import lmap

sys.dont_write_bytecode = True

import unittest


def parse(data):
    ret = []
    for x in data:
        ret.append(lmap(int, list(x)))
    return ret


def part_1(data, grid=(100, 100)):
    som = 0
    smallest_points = []
    for i, row in enumerate(data):
        for j, x in enumerate(row):
            nb = neighbors((j, i), grid=grid, diagonal=False)
            smallest = True
            for a, b in nb:
                if data[b][a] <= x:
                    smallest = False
            if smallest:
                som += 1 + x
                smallest_points.append((j, i))
    return som, smallest_points


def part_2(data, grid=(100, 100)):
    """
    21XXX43210
    3X878X4X21
    X85678X8X2
    87678X678X
    X8XXX65678
    """
    cache = []
    source = parse(data)
    smallest_points = part_1(data, grid=grid)[1]
    print(smallest_points)
    for coord in smallest_points:
        # print(f"{coord} - ", end="")
        nb = neighbors(coord, grid, diagonal=False)
        queue = nb.copy()
        basin = [coord, ]
        running = True
        while running:
            try:
                x, y = queue.pop()
                # print(f"({x}, {y}) - ", end="")
                if source[y][x] != 9 and (x, y) not in basin:
                    basin.append((x, y))
                    nb2 = neighbors((x, y), grid, diagonal=False)
                    [queue.append(n) for n in nb2 if n not in queue]
            except IndexError:
                running = False
            if basin not in cache:
                cache.append(basin)
        # print(basin)
    return prod(len(x) for x in sorted(cache, key=len, reverse=True)[0:3])


class UnitTests(unittest.TestCase):
    source = read_int_matrix("day_9.txt")
    test_source = read_int_matrix("""2199943210
3987894921
9856789892
8767896789
9899965678""")

    def test_example_data_part_1(self):
        self.assertEqual(15, part_1(self.test_source, grid=(10, 5))[0])

    def test_example_data_part_2(self):
        self.assertEqual(1134, part_2(self.test_source, grid=(10, 5)))

    def test_part_1(self):
        self.assertEqual(500, part_1(self.source, grid=(100, 100))[0])

    def test_part_2(self):
        self.assertEqual(970200, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
