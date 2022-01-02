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
            list("00000000000000000000000000000000000000000000000000"),
            list("00000000000000000000000000000000000000000000000000"),
            list("00000000000000000000000000000000000000000000000000"),
            list("00000000000000000000000000000000000000000000000000"),
        ]

    def flip(self):
        self.display = list(map(list, zip(*self.display)))

    def rect(self, width, height):
        _(width, height)
        ww = width if width <= len(self.display[0]) else len(self.display[0])
        hh = height if height <= len(self.display) else len(self.display)
        for h in range(hh):
            for w in range(ww):
                self.display[h][w] = "1"

    def rotate_col(self, column, by):
        self.flip()
        col = self.rotate(self.display[column], by)
        self.display[column] = col
        self.flip()

    def rotate_row(self, row, by):
        # _(row, by)
        r = self.rotate(self.display[row % len(self.display)], by)
        self.display[row % len(self.display)] = r

    def rotate(self, li, x):
        return li[-x % len(li):] + li[:-x % len(li)]

    def __str__(self) -> str:
        ret = ""
        for row in self.display:
            ret += "".join(row)
            ret += "\n"
        ret += f"Lit: {self.lit()}"
        return ret

    def lit(self):
        total = 0
        for row in self.display:
            for c in row:
                total += 1 if c == "1" else 0
        return total


def part_1(source):
    d = Tcds()
    for instruction in source:
        _(d)
        left, right = ints(instruction)
        if "rect" in instruction:
            d.rect(left, right)
        elif "rotate row" in instruction:
            d.rotate_row(left, right)
        elif "rotate column" in instruction:
            d.rotate_col(left, right)
        else:
            raise ValueError("Should not be here")
    _(d)
    return d.lit()


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}.input")))

    def test_part_1(self):
        self.assertEqual(None, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
