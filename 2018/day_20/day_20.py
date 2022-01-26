#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """Keywords:
Parsing without recursion!
regex like
brackets
Open and closing
"""

import os
import sys
import unittest
from collections import defaultdict
from pathlib import Path

from ivonet.files import read_data
from ivonet.grid import Location, DIRECTIONS
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class ARegularMap:

    def __init__(self, source) -> None:
        self.source = source[1:-1]
        self.positions: list[Location] = []
        self.start = Location(0, 0)
        self.distances = defaultdict(int)
        self.process()

    def process(self):
        previous = current = self.start
        for c in self.source:
            if c == "(":
                self.positions.append(current)
            elif c == ")":
                current = self.positions.pop()
            elif c == "|":
                current = self.positions[-1]
            else:
                current += DIRECTIONS[c]
                if self.distances[current] == 0:
                    self.distances[current] = self.distances[previous] + 1
            previous = current

    def shortest_longest_path(self) -> int:
        return max(self.distances.values())

    def doors(self, min_nr_of_doors: int) -> int:
        return len([x for x in self.distances.values() if x >= min_nr_of_doors])


def part_1(source):
    return ARegularMap(source).shortest_longest_path()


def part_2(source):
    return ARegularMap(source).doors(1000)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}_test_a.input")
        self.test_source2 = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}_test_b.input")

    def test_example_data_part_1(self):
        self.assertEqual(3, part_1("^WNE$"))
        self.assertEqual(10, part_1("^ENWWW(NEEE|SSE(EE|N))$"))
        self.assertEqual(18, part_1("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"))
        self.assertEqual(23, part_1("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"))
        self.assertEqual(31, part_1("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$"))

    def test_other_official_set(self):
        self.assertEqual(3806, part_1(self.test_source))
        self.assertEqual(8354, part_2(self.test_source))

    def test_other_official_set_2(self):
        self.assertEqual(3879, part_1(self.test_source2))
        self.assertEqual(8464, part_2(self.test_source2))

    def test_part_1(self):
        self.assertEqual(3755, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(8627, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
