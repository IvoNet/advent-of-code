#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import os
import sys
import unittest
from collections import Counter
from itertools import product, chain
from pathlib import Path
from typing import NamedTuple

from ivonet.files import read_rows
from ivonet.iter import ints, quantify

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Location(NamedTuple):
    col: int
    row: int


def parse(source):
    return sorted([Location(*ints(line)) for line in source], key=lambda x: (x.row, x.col), reverse=False)


def manhatten_distance(left: Location, right: Location) -> int:
    return abs(left.row - right.row) + abs(left.col - right.col)


def closest_to(given: Location, locations: list[Location]):
    """Find the points with the shortest distance to the given Location
    return None if distance not smaller
    """
    first, second = sorted(locations, key=lambda loc: manhatten_distance(loc, given))[:2]
    return first if manhatten_distance(first, given) < manhatten_distance(second, given) else None


def closest_counts(points: list[Location], margin=100):
    """What is the size of the largest area of closest points that isn't infinite?"""
    assert len(points) > 1
    xside = range(-margin, max(loc[0] for loc in points) + margin)
    yside = range(-margin, max(loc[1] for loc in points) + margin)
    box = product(xside, yside)
    # counts[point] = number of grid points in box that are closest to point
    counts = Counter(closest_to(Location(*p), points) for p in box)
    # Now delete the counts that are suspected to be infinite:
    for p in perimeter(xside, yside):
        c = closest_to(Location(*p), points)
        if c in counts:
            del counts[c]
    return counts


def perimeter(xside, yside):
    """The perimeter of a box with these sides."""
    return chain(((xside[0], y) for y in yside),
                 ((xside[-1], y) for y in yside),
                 ((x, yside[0]) for x in xside),
                 ((x, yside[-1]) for x in xside))


def total_distance(given: Location, points: list[Location]):
    """Total distance from one point to all provided points"""
    return sum(manhatten_distance(given, point) for point in points)


def part_1(source):
    coords = parse(source)
    counts = closest_counts(coords)
    return max(counts.values())


def part_2(source, dist=10000):
    coords = parse(source)
    max_row = max(loc.row for loc in coords)
    max_col = max(loc.col for loc in coords)
    box = product(range(max_col + 1), range(max_row + 1))
    return quantify(box, lambda p: total_distance(Location(*p), coords) < dist)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""1, 1
1, 6
8, 3
3, 4
5, 5
8, 9""")

    def test_example_data_part_1(self):
        self.assertEqual(17, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(3276, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(16, part_2(self.test_source, dist=32))

    def test_part_2(self):
        self.assertEqual(38380, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
