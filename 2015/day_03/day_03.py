#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from collections import defaultdict
from pathlib import Path

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def parse(source):
    ...


class Santa:

    def __init__(self) -> None:
        self.locations = defaultdict(int)
        self.north = 0
        self.east = 0
        self.south = 0
        self.west = 0
        self.locations[(0, 0, 0, 0)] = 1

    def go(self, c: str):
        if c == "^":
            if self.south > 0:
                self.south -= 1
            else:
                self.north += 1
        elif c == "v":
            if self.north > 0:
                self.north -= 1
            else:
                self.south += 1
        elif c == "<":
            if self.east > 0:
                self.east -= 1
            else:
                self.west += 1
        elif c == ">":
            if self.west > 0:
                self.west -= 1
            else:
                self.east += 1
        else:
            raise ValueError(f"Unknown direction [{c}]")
        self.locations[(self.north, self.east, self.south, self.west)] += 1


def part_1(source):
    locations = defaultdict(int)
    north = 0
    east = 0
    south = 0
    west = 0
    locations[(0, 0, 0, 0)] = 1
    for c in source:
        if c == "^":
            if south > 0:
                south -= 1
            else:
                north += 1
        elif c == "v":
            if north > 0:
                north -= 1
            else:
                south += 1
        elif c == "<":
            if east > 0:
                east -= 1
            else:
                west += 1
        elif c == ">":
            if west > 0:
                west -= 1
            else:
                east += 1
        else:
            raise ValueError(f"Unknown direction [{c}]")
        locations[(north, east, south, west)] += 1
    _(locations)
    return len(locations)


def part_2(source):
    santa = Santa()
    robo_santa = Santa()
    flip = True
    for c in source:
        if flip:
            santa.go(c)
        else:
            robo_santa.go(c)
        flip = not flip
    locations = santa.locations
    for k, v in robo_santa.locations.items():
        locations[k] += v
    return len(locations)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"day_{day.zfill(2)}.input")
        self.test_source = read_data("""^>v<""")

    def test_example_data_part_1(self):
        self.assertEqual(4, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(2572, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(3, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(2631, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
