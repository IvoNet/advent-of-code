#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints, permutations

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def prepare_graph(source):
    cities = set()
    weights = {}
    for line in source:
        city1, to, city2, equal, distance = line.split()
        cities.add(city1)
        cities.add(city2)
        weights[city1, city2] = int(distance)
        weights[city2, city1] = int(distance)
    return list(cities), weights


def part_1(source):
    cities, weights = prepare_graph(source)
    shortest = float("inf")  # https://stackoverflow.com/questions/13795758/what-is-sys-maxint-in-python-3
    for places in permutations(cities):
        length = sum(weights[places[i], places[i + 1]] for i in range(len(places) - 1))
        shortest = min(shortest, length)
    return shortest


def part_2(source):
    cities, weights = prepare_graph(source)
    longest = float("-inf")  # https://stackoverflow.com/questions/13795758/what-is-sys-maxint-in-python-3
    for places in permutations(cities):
        length = sum(weights[places[i], places[i + 1]] for i in range(len(places) - 1))
        longest = max(longest, length)
    return longest


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"day_{day.zfill(2)}.input")
        self.test_source = read_rows("""London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141""")

    def test_example_data_part_1(self):
        self.assertEqual(605, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(251, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(982, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(898, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
