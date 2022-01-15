#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """"""

import os
import sys
import unittest
from pathlib import Path
from typing import TypeVar

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True
T = TypeVar('T')

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def parse(source):
    return [(a, b) if a < b else (b, a) for a, b in [ints(line) for line in source]]


def extend(bridge, blocks):
    unused = list(filter(lambda b: b not in bridge and b[::-1] not in bridge, blocks))
    for block in unused:
        if bridge[-1][1] == block[0]:
            yield bridge + [block]
        elif bridge[-1][1] == block[1]:
            yield bridge + [block[::-1]]


def bridge_strength(bridge):
    return sum(map(sum, bridge))


def astar(magnets):
    new_bridges = [[magnet] for magnet in magnets if 0 in magnet]  # Need to start with 0
    strongest = 0
    longest_strength = 0
    while new_bridges:
        bridges = new_bridges
        new_bridges = []
        for bridge in bridges:
            new_bridges.extend(list(extend(bridge, magnets)))
        if new_bridges:
            longest_strength = max(bridge_strength(bridge) for bridge in new_bridges)
            strongest = max(strongest, longest_strength)
    return strongest, longest_strength


def part_1(source):
    magnets = parse(source)
    strongest, _ = astar(magnets)
    return strongest


def part_2(source):
    magnets = parse(source)
    _, longest_strength = astar(magnets)
    return longest_strength


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10""")

    def test_example_data_part_1(self):
        self.assertEqual(31, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(1868, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(1841, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
