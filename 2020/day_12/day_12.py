#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
--- Day 12: Rain Risk ---
Your ferry made decent progress toward the island, but the storm came in faster 
than anyone expected. The ferry needs to take evasive actions!

Unfortunately, the ship's navigation computer seems to be malfunctioning; rather 
than giving a route directly to safety, it produced extremely circuitous instructions. 
When the captain uses the PA system to ask if anyone can help, you quickly volunteer.

The navigation instructions (your puzzle input) consists of a sequence of 
single-character actions paired with integer input values. After staring at 
them for a few minutes, you work out what they probably mean:

- Action N means to move north by the given value.
- Action S means to move south by the given value.
- Action E means to move east by the given value.
- Action W means to move west by the given value.
- Action L means to turn left the given number of degrees.
- Action R means to turn right the given number of degrees.
- Action F means to move forward by the given value in the direction the ship is 
  currently facing.

The ship starts by facing east. Only the L and R actions change the direction the ship is 
facing. (That is, if the ship is facing east and the next instruction is N10, the 
ship would move north 10 units, but would still move east if the following action were F.)

For example:

F10
N3
F7
R90
F11

These instructions would be handled as follows:

- F10 would move the ship 10 units east (because the ship starts by facing east) 
  to east 10, north 0.
- N3 would move the ship 3 units north to east 10, north 3.
- F7 would move the ship another 7 units east (because the ship is still facing east) 
  to east 17, north 3.
- R90 would cause the ship to turn right by 90 degrees and face south; it remains at 
  east 17, north 3.
- F11 would move the ship 11 units south to east 17, south 8.

At the end of these instructions, the ship's Manhattan distance (sum of the absolute 
values of its east/west position and its north/south position) from its starting
position is 17 + 8 = 25.

Figure out where the navigation instructions lead. What is the Manhattan distance 
between that location and the ship's starting position?

--- Part Two ---

Before you can give the destination to the captain, you realize that the actual 
action meanings were printed on the back of the instructions the whole time.

Almost all of the actions indicate how to move a waypoint which is relative 
to the ship's position:

- Action N means to move the waypoint north by the given value.
- Action S means to move the waypoint south by the given value.
- Action E means to move the waypoint east by the given value.
- Action W means to move the waypoint west by the given value.
- Action L means to rotate the waypoint around the ship left (counter-clockwise) 
  the given number of degrees.
- Action R means to rotate the waypoint around the ship right (clockwise) the 
  given number of degrees.
- Action F means to move forward to the waypoint a number of times equal to the 
  given value.

The waypoint starts 10 units east and 1 unit north relative to the ship. 
The waypoint is relative to the ship; that is, if the ship moves, the 
waypoint moves with it.

For example, using the same instructions as above:

- F10 moves the ship to the waypoint 10 times (a total of 100 units east and 10 
  units north), leaving the ship at east 100, north 10. The waypoint stays 10 units 
  east and 1 unit north of the ship.
- N3 moves the waypoint 3 units north to 10 units east and 4 units north of the 
  ship. The ship remains at east 100, north 10.
- F7 moves the ship to the waypoint 7 times (a total of 70 units east and 28 
  units north), leaving the ship at east 170, north 38. The waypoint stays 10 units 
  east and 4 units north of the ship.
- R90 rotates the waypoint around the ship clockwise 90 degrees, moving it to 
  4 units east and 10 units south of the ship. 
  The ship remains at east 170, north 38.
- F11 moves the ship to the waypoint 11 times (a total of 44 units east and 110 
  units south), leaving the ship at east 214, south 72. The waypoint stays 4 units 
  east and 10 units south of the ship.

After these operations, the ship's Manhattan distance from its 
starting position is 214 + 72 = 286.

Figure out where the navigation instructions actually lead. 
What is the Manhattan distance between that location and the ship's starting position?
"""

import sys
import unittest
from collections import defaultdict

from ivonet.files import read_rows

sys.dont_write_bytecode = True

DIR = {
    "N": {
        "R": {
            90: "E",
            180: "S",
            270: "W"
        },
        "L": {
            90: "W",
            180: "S",
            270: "E"
        },
    },
    "E": {
        "R": {
            90: "S",
            180: "W",
            270: "N"
        },
        "L": {
            90: "N",
            180: "W",
            270: "S"
        },
    },
    "S": {
        "R": {
            90: "W",
            180: "N",
            270: "E"
        },
        "L": {
            90: "E",
            180: "N",
            270: "W"
        },
    },
    "W": {
        "R": {
            90: "N",
            180: "E",
            270: "S"
        },
        "L": {
            90: "S",
            180: "E",
            270: "N"
        },
    },
}


def part_1(source):
    total = defaultdict(int)
    d = "E"
    for cmd in source:
        c = cmd[0]
        value = int(cmd[1:])
        if c in "NESW":
            total[c] += value
        elif c == "F":
            total[d] += value
        elif c in "RL":
            d = DIR[d][c][value]
        else:
            raise ValueError(f"Wrong command: {c}")
    return abs(total["N"] - total["S"]) + abs(total["E"] - total["W"])


def part_2(source):
    d = "E"
    ship = defaultdict(int)
    waypoint = defaultdict(int)
    waypoint["E"] = 10
    waypoint["N"] = 1
    d = "E"
    for cmd in source:
        c = cmd[0]
        value = int(cmd[1:])
        if c in "NESW":
            waypoint[c] += value
        elif c == "F":
            ns = abs(waypoint[d] - waypoint[DIR[d][c][180]])
            ship[d] += value * ns
        elif c in "RL":
            d = DIR[d][c][value]
        else:
            raise ValueError(f"Wrong command: {c}")
    return abs(ship["N"] - ship["S"]) + abs(ship["E"] - ship["W"])


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        self.source = read_rows("day_12.input")
        self.test_source = read_rows("""F10
N3
F7
R90
F11""")

    def test_example_data_part_1(self):
        self.assertEqual(25, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(1533, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(286, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
