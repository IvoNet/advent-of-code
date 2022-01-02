#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from collections import defaultdict
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints

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
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}.input")))
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
