#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)



@dataclass
class Location:
    keypad = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    row: int
    col: int

    def up(self):
        self.row -= 1 if self.row > 0 else 0

    def down(self):
        self.row += 1 if self.row < 2 else 0

    def left(self):
        self.col -= 1 if self.col > 0 else 0

    def right(self):
        self.col += 1 if self.col < 2 else 0

    def key(self):
        return self.keypad[self.row][self.col]

    def move(self, m):
        if m == "L":
            self.left()
        elif m == "R":
            self.right()
        elif m == "U":
            self.up()
        elif m == "D":
            self.down()
        else:
            raise ValueError("Should not be here")



def part_1(source):
    loc = Location(1,1)
    nr = ""
    for line in source:
        for c in line:
            loc.move(c)
        nr += str(loc.key())
    return int(nr)


def part_2(source):
    return 0


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"day_{day.zfill(2)}.input")
        self.test_source = read_rows("""ULL
RRDDD
LURDL
UUUUD""")

    def test_example_data_part_1(self):
        self.assertEqual(1985, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(38961, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
