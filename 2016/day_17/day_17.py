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
from typing import NamedTuple, TypeVar

from ivonet.collection import Queue
from ivonet.files import read_data
from ivonet.hexadecimal import mdfive
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True

T = TypeVar("T")


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Location(NamedTuple):
    x: int
    y: int


def md5_four(passcode, pth):
    """Generate a digest based on the passcode and current path and return the first 4 chars."""
    return mdfive(f"{passcode}{pth}")[:4]


def is_door_open(passcode, pth) -> dict[[str], bool]:
    """See for all directions if the door can be opened based on the rules"""
    digest = md5_four(passcode, pth)
    return {k: digest[i] in "bcdef" for i, k in enumerate("UDLR")}


def surrounding(loc: Location, passcode: str, pth: str, goal):
    """Generates all locations that can be reached from the current location.
    The grid as described is just a simple 4x4 grid and not the "difficult" representation.
    working with the abstraction is way easier.
    """
    if loc == goal:
        return
    can_go = is_door_open(passcode, pth)
    if loc.x + 1 <= goal.x and can_go["R"]:
        yield Location(loc.x + 1, loc.y), "R"
    if loc.x - 1 >= 0 and can_go["L"]:
        yield Location(loc.x - 1, loc.y), "L"
    if loc.y + 1 <= goal.y and can_go["D"]:
        yield Location(loc.x, loc.y + 1), "D"
    if loc.y - 1 >= 0 and can_go["U"]:
        yield Location(loc.x, loc.y - 1), "U"


def solve(passcode, initial=Location(0, 0), goal=Location(3, 3), part1=True):
    """A BFS search.
    in this puzzle it is not important if you have already been to a certain location as doors can open and close
    becoming "walls" op open spaces again.
    This algorithm is interested in the actual path being walked.
    The bfs had to be adjusted to accommodate that goal and for part two
    I had to walk all of it and only end after walking all paths thereby finding the longest.
    In order to do that I had to add the goal test to the surroundings function to otherwise it will never end.
    """
    q = Queue()
    q.push((initial, ""))
    visited = set()
    longest = 0
    while not q.empty:
        p, pth = q.pop()
        if p == goal:
            if part1:
                return pth
            else:
                longest = max(longest, len(pth))
        visited.add(pth)
        for loc, d in surrounding(p, passcode, pth, goal):
            new_path = pth + d
            if new_path not in visited:
                q.push((loc, new_path))
    return longest


def part_1(source):
    return solve(source)


def part_2(source):
    return solve(source, part1=False)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_data("""hijkl""")

    def test_passcode(self):
        self.assertEqual("ced9", md5_four("hijkl", ""))

    def test_example_data_part_1(self):
        self.assertEqual("DDRRRD", part_1("ihgpwlah"))

    def test_example_data_2_part_1(self):
        self.assertEqual("DDUDRLRRUDRD", part_1("kglvqrro"))

    def test_example_data_3_part_1(self):
        self.assertEqual("DRURDRUDDLLDLUURRDULRLDUUDDDRR", part_1("ulqzkmiv"))

    def test_part_1(self):
        self.assertEqual("RLDUDRDDRR", part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(370, part_2("ihgpwlah"))
        self.assertEqual(492, part_2("kglvqrro"))
        self.assertEqual(830, part_2("ulqzkmiv"))

    def test_part_2(self):
        self.assertEqual(590, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
