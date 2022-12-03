#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """"""

import math
import os
import sys
import unittest
from pathlib import Path

from ivonet.files import read_rows
from ivonet.grid import Location, manhattan_distance
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True

DIRECTIONS = {
    "U": Location(0, 1),
    "D": Location(0, -1),
    "L": Location(-1, 0),
    "R": Location(1, 0),
}


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def parse(value: str, delimiter: str = ",") -> list[Location]:
    """Parse the input into a list of lists of strings and ints"""
    base = Location(0, 0)
    all_locations = []
    for location, times in [(DIRECTIONS[x[0]], int(x[1:])) for x in value.split(delimiter)]:
        for __ in range(times):
            base += location
            all_locations.append(base)
    return all_locations


def part_1(source):
    md = manhattan_distance(Location(0, 0))
    line1 = parse(source[0])
    line2 = parse(source[1])
    return min(md(x) for x in set(line1).intersection(line2))


def part_2(source):
    line1 = parse(source[0])
    line2 = parse(source[1])
    intersections = set(line1).intersection(line2)
    current = math.inf
    for intersection in intersections:
        steps1 = line1.index(intersection) + 1
        steps2 = line2.index(intersection) + 1
        current = min(current, steps1 + steps2)
    return current


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""R8,U5,L5,D3
U7,R6,D4,L4""")
        self.test_source2 = read_rows("""R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83""")
        self.test_source3 = read_rows("""R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7""")

    def test_example_data_part_1(self):
        self.assertEqual(6, part_1(self.test_source))
        self.assertEqual(159, part_1(self.test_source2))
        self.assertEqual(135, part_1(self.test_source3))

    def test_part_1(self):
        self.assertEqual(403, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(30, part_2(self.test_source))
        self.assertEqual(610, part_2(self.test_source2))
        self.assertEqual(410, part_2(self.test_source3))

    def test_part_2(self):
        self.assertEqual(4158, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
