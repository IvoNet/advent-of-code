#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """"""

import sys
import unittest
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Tcds:
    """tiny-code-displaying-screen"""

    def __init__(self) -> None:
        self.display = [
            list("00000000000000000000000000000000000000000000000000"),
            list("00000000000000000000000000000000000000000000000000"),
            list("00000000000000000000000000000000000000000000000000")
        ]

    def flip(self):
        self.display = list(zip(*self.display))

    def rect(self, width, height):
        for h in range(height):
            for w in range(width):
                self.display[h][w] = "1"

    def rotate_col(self, column, by):
        self.flip()
        col = self.rotate(self.display[column], by)
        del self.display[column]
        self.display.insert(column, col)
        self.flip()

    def rotate_row(self, row, by):
        r = self.rotate(self.display[row], by)
        del self.display[row]
        self.display.insert(row, r)

    def rotate(self, li, x):
        return li[-x % len(li):] + li[:-x % len(li)]

    def __str__(self) -> str:
        ret = ""
        for row in self.display:
            ret += "".join(row)
            ret += "\n"
        return ret


def part_1(source):
    d = Tcds()
    d.rect(3, 2)
    # d.rotate_row(0, 6)
    d.rotate_col(1, 1)
    print(d)
    return None


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}.input")))
        self.test_source = read_rows("""""")

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
