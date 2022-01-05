#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
             1
  0123456789012
 0#############
 1#..X.X.X.X..#  <- hallway 11 long
 2###C#B#D#D###
 3  #B#C#A#A#
 4  #########
     ^ ^ ^ ^
col: A B C D
Rules:
- # is a wall
- . is empty space
    - Eleven open spaces
- X is empty space where you can not stop
- A's need to go into the A lane
- B's / C's / D's need to go ....
- Lanes -> No Stop
    A -> 2
    B -> 4
    C -> 6
    D -> 8
- Cost 1 move:
   A -> 1
   B -> 10
   C -> 100
   D -> 1000

Grid -> Astar?
#############
#..X.X.X.X..#
###C#B#D#D###
###B#C#A#A###
#############
Going for a* function...
Astar needs:
- initial state
- callable to test if goal has been reached
- callable to get the list of successors
- callable to get the heuristic (distance to the goal)
- callable for the cost calculation
"""

import sys
import unittest
from enum import IntEnum
from pathlib import Path
from typing import NamedTuple

from ivonet.files import read_rows
from ivonet.iter import ints, words, zip_list

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Amphipod(IntEnum):
    A = 1
    B = 10
    C = 100
    D = 1000


costs = {"A": 1,
         "B": 10,
         "C": 100,
         "D": 1000
         }


class SideRoom(NamedTuple):
    top: None | Amphipod
    bottom: None | Amphipod


def parse(source):
    a1, b1, c1, d1 = words(source[2])
    a2, b2, c2, d2 = words(source[3])
    return {
        "A": SideRoom(Amphipod[a1], Amphipod[a2]),
        "B": SideRoom(Amphipod[b1], Amphipod[b2]),
        "C": SideRoom(Amphipod[c1], Amphipod[c2]),
        "D": SideRoom(Amphipod[d1], Amphipod[d2]),
    }


def parse2(source):
    longest = 0
    grid = []
    for line in source:
        longest = len(line) if len(line) > longest else longest
        line = line.replace(" ", "#")
        line = list(line)
        if len(line) < longest:
            for _ in range(len(line), longest):
                line.append("#")
        row = []
        for item in line:
            if item == "#":
                row.append("#")
            if item == "A":
                row.append(Amphipod.A)
            if item == "B":
                row.append(Amphipod.B)
            if item == "C":
                row.append(Amphipod.C)
            if item == "D":
                row.append(Amphipod.D)
            if item == ".":
                row.append(None)
        grid.append(row)

    # A very hacky way of removing the top and bottom row and left and right cols
    # as they have no added meaning in this floorplan
    floorplan = zip_list(list(zip(*(grid[1:-1])))[1:-1])
    return State(floorplan)


class State:

    def __init__(self, floorplan: dict[[str], SideRoom], hallway: list = [None] * 11) -> None:
        self.floorplan: dict[[str], SideRoom] = floorplan
        self._hash = hash(repr(self))
        self.cols = {
            Amphipod.A: 2,
            Amphipod.B: 4,
            Amphipod.C: 6,
            Amphipod.D: 8,
        }
        self.hall_doors = {
            "A": 2,
            "B": 4,
            "C": 6,
            "D": 8,
        }
        self.hallway: list = [0, 1, 3, 5, 7, 9, 10]
        self.left = {}
        self.right = {}
        for k, v in self.hall_doors.items():
            self.left[v] = self.hallway[:v]
            self.right[v] = self.hallway[v:]

    def goal_test(self) -> bool:
        """Goal has been reachted when:
        - All Amphipods in their won collective cols
        """
        for k, v in self.floorplan.items():
            if v.count(Amphipod[k]) != len(v):
                return False
        return True

    @property
    def is_legal(self) -> bool:
        for i, row in enumerate(self.floorplan):
            if i == 0:
                for pos in self.cols.values():
                    if isinstance(row[pos], Amphipod):
                        return False
            # TODO not finished
        return True

    def successors(self) -> list[State]:
        """Create all possible new states from current state
        """
        sucs: list[State] = []

    def manhatten_distance(self, ):
        ...


def part_1(source):
    """Astar needs:
    - initial state
    - callable to test if goal has been reached
    - callable to get the list of successors
    - callable to get the heuristic (distance to the goal)
    - callable for the cost calculation"""
    start = parse(source)
    _(start)
    return 0


def part_2(source):
    return 0


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}.input")))
        self.test_source = read_rows("""#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########""")

    def test_goal_1(self):
        fp = {
            "A": SideRoom(Amphipod.A, Amphipod.A),
            "B": SideRoom(Amphipod.B, Amphipod.B),
            "C": SideRoom(Amphipod.C, Amphipod.C),
            "D": SideRoom(Amphipod.D, Amphipod.D),
        }
        self.assertTrue(State(fp).goal_test())

    def test_goal_2(self):
        fp = {
            "A": SideRoom(Amphipod.B, Amphipod.A),
            "B": SideRoom(Amphipod.B, Amphipod.A),
            "C": SideRoom(Amphipod.C, Amphipod.C),
            "D": SideRoom(Amphipod.D, Amphipod.D),
        }
        self.assertFalse(State(fp).goal_test())

    def test_goal_3(self):
        fp = {
            "A": SideRoom(Amphipod.A, Amphipod.A),
            "B": SideRoom(Amphipod.B, Amphipod.B),
            "C": SideRoom(Amphipod.C, Amphipod.C),
            "D": SideRoom(None, Amphipod.D),
        }
        self.assertFalse(State(fp).goal_test())

    def test_example_data_part_1(self):
        self.assertEqual(None, part_1(self.test_source))

    @unittest.SkipTest
    def test_part_1(self):
        self.assertEqual(None, part_1(self.source))

    @unittest.SkipTest
    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    @unittest.SkipTest
    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
