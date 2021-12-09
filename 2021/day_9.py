#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import sys

sys.dont_write_bytecode = True

import unittest
from ivonet import read_rows, neighbors, lmap


def parse(data):
    ret = []
    for x in data:
        ret.append(lmap(int, list(x)))
    return ret


def part_1(data, grid=(100, 100)):
    som = 0
    source = parse(data)
    # pprint(source)
    for i, row in enumerate(source):
        for j, x in enumerate(row):
            print(f"({j},{i}) - ", end="")
            nb = neighbors((j, i), grid=grid, diagonal=False)
            print(nb, end=" - ")
            smallest = True
            for a, b in nb:
                print(f"[{b},{a}] - /{source[b][a]}/ - {x}", end=" ")
                if source[b][a] <= x:
                    smallest = False
            if smallest:
                print("YES", end="")
                som += 1 + x
            print()
    return som


def part_2(data, grid=(100, 100)):
    som = 0
    source = parse(data)
    for i, row in enumerate(source):
        for j, x in enumerate(row):
            print(f"({j},{i}) - ", end="")
            nb = neighbors((j, i), grid=grid, diagonal=False)
            print(nb, end=" - ")
            smallest = True
            for a, b in nb:
                print(f"[{b},{a}] - /{source[b][a]}/ - {x}", end=" ")
                if source[b][a] <= x:
                    smallest = False
            if smallest:
                print("YES", end="")
                som += 1 + x
            print()
    return som


class UnitTests(unittest.TestCase):
    source = read_rows("day_9.txt")
    test_source = """2199943210
3987894921
9856789892
8767896789
9899965678""".split("\n")

    def test_example_data_part_1(self):
        self.assertEqual(15, part_1(self.test_source, grid=(10, 5)))

    def test_example_data_part_2(self):
        self.assertEqual(1134, part_2(self.test_source))

    def test_part_1(self):
        self.assertEqual(500, part_1(self.source, grid=(100, 100)))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
