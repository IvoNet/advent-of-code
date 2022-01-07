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
from collections import deque
from enum import Enum
from hashlib import md5
from pathlib import Path
from typing import NamedTuple, TypeVar, Optional, Generic

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True

T = TypeVar("T")


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


GRID = """#########
# | | | #
#-#-#-#-#
# | | | #
#-#-#-#-#
# | | | #
#-#-#-#-#
# | | |  
#######  """.replace("|", "~").replace("-", "~")


class Cell(str, Enum):
    EMPTY = " "
    WALL = "#"
    DOOR = "~"
    START = "S"
    GOAL = "V"
    PATH = "*"


class Location(NamedTuple):
    x: int
    y: int


class Node(Generic[T]):
    def __init__(self, state: T, parent: Optional[Node], direction: Optional[str]) -> None:
        self.state: T = state
        self.parent: Optional[Node] = parent
        self.direction: str = direction

    def __repr__(self) -> str:
        if self.parent:
            return f"state[{self.state}] - direction[{self.direction}] - parent[{self.parent.state}]"
        return f"state[{self.state}] - cost_calculator[{self.direction}] - parent[None]"


def mdfive(s):
    return md5(s.encode()).hexdigest()[:4]


def md5pth(passcode, pth):
    return mdfive(f"{passcode}{pth}")


def isopen(passcode, pth):
    digest = md5pth(passcode, pth)
    ret = {}
    ret["U"] = digest[0] in "bcdef"
    ret["D"] = digest[1] in "bcdef"
    ret["L"] = digest[2] in "bcdef"
    ret["R"] = digest[3] in "bcdef"
    return ret


def surrounding(loc: Location, passcode: str, pth: str):
    """Generates all locations that can be reached from the current location."""
    if loc == Location(3, 3):
        return
    can_go = isopen(passcode, pth)
    if loc.x + 1 <= 3 and can_go["R"]:
        yield (Location(loc.x + 1, loc.y), "R")
    if loc.x - 1 >= 0 and can_go["L"]:
        yield (Location(loc.x - 1, loc.y), "L")
    if loc.y + 1 <= 3 and can_go["D"]:
        yield (Location(loc.x, loc.y + 1), "D")
    if loc.y - 1 >= 0 and can_go["U"]:
        yield (Location(loc.x, loc.y - 1), "U")


def solve(passcode, initial=Location(0, 0), goal=Location(3, 3), part_1=True):
    q = deque()
    q.append((initial, ""))
    visited = set()
    longest = 0
    while q:
        p, pth = q.popleft()
        if p == goal:
            if part_1:
                return pth
            else:
                longest = max(longest, len(pth))
        visited.add(pth)
        for loc, d in surrounding(p, passcode, pth):
            npth = pth + d
            if npth not in visited:
                q.append((loc, npth))
    return longest


def part_1(source):
    return solve(source)


def part_2(source):
    return solve(source, part_1=False)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_data("""hijkl""")

    def test_passcode(self):
        self.assertEqual("ced9", md5pth("hijkl", ""))

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
