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
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints, words

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


costs = {"A": 1,
         "B": 10,
         "C": 100,
         "D": 1000
         }


def parse(source):
    a1, b1, c1, d1 = words(source[2])
    a2, b2, c2, d2 = words(source[3])
    return {
        'A' : (a1,a2),
        'B' : (b1,b2),
        'C' : (c1,c2),
        'D' : (d1,d2),
    }


def part_1(source):
    """Astar needs:
    - initial state
    - callable to test if goal has been reached
    - callable to get the list of successors
    - callable to get the heuristic (distance to the goal)
    - callable for the cost calculation"""
    start = parse(source)
    print(start)
    return 0


def part_2(source):
    return 0


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"day_{day.zfill(2)}.input")
        self.test_source = read_rows("""#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########""")

    def test_example_data_part_1(self):
        self.assertEqual(None, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(None, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
