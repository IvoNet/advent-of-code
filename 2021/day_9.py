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
from ivonet.grid import neighbors, neighbor_values
from ivonet.iter import lmap

sys.dont_write_bytecode = True

import unittest


def parse(data):
    ret = []
    for x in data:
        ret.append(lmap(int, list(x)))
    return ret


def part_1(matrix):
    som = 0
    smallest_points = []
    for h, row in enumerate(matrix):
        for w, x in enumerate(row):
            nb = neighbors(matrix, (h, w), diagonal=False)
            smallest = True
            for a, b in nb:
                if matrix[a][b] <= x:
                    smallest = False
            if smallest:
                som += 1 + x
                smallest_points.append((h, w))
    return som, smallest_points


def part_1a(matrix):
    points = 0
    smallest_points = []
    for h in range(len(matrix)):
        for w in range(len(matrix[0])):
            me = matrix[h][w]
            nb = neighbor_values(matrix, (h, w), diagonal=False)
            if me < min(nb):
                points += 1 + me
                smallest_points.append((h, w))
    return points, smallest_points


def part_2(matrix):
    cache = []
    smallest_points = part_1a(matrix)[1]
    for coord in smallest_points:
        queue = neighbors(matrix, coord, diagonal=False)
        basin = [coord, ]
        running = True
        while running:
            try:
                h, w = queue.pop()
                if matrix[h][w] != 9 and (h, w) not in basin:
                    basin.append((h, w))
                    nb2 = neighbors(matrix, (h, w), diagonal=False)
                    [queue.append(n) for n in nb2 if n not in queue and n not in basin]
            except IndexError:
                running = False
            if basin not in cache:
                cache.append(basin)
    return prod(len(x) for x in sorted(cache, key=len, reverse=True)[0:3])


class UnitTests(unittest.TestCase):
    source = read_int_matrix("day_9.txt")
    test_source = read_int_matrix("""2199943210
3987894921
9856789892
8767896789
9899965678""")

    def test_example_data_part_1(self):
        self.assertEqual(15, part_1(self.test_source)[0])

    def test_example_data_part_2(self):
        self.assertEqual(1134, part_2(self.test_source))

    def test_part_1(self):
        self.assertEqual(500, part_1(self.source)[0])

    def test_part_1a(self):
        self.assertEqual(500, part_1a(self.source)[0])

    def test_part_1a2(self):
        self.assertEqual(part_1(self.source)[1], part_1a(self.source)[1])

    def test_part_2(self):
        self.assertEqual(970200, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
