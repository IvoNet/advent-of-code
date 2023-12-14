#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2022 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
If a part of the code is not part of the post it is probably 
code I found reusable and I may have moved it to my 'ivonet' library.
you can find that here: https://github.com/IvoNet/advent-of-code/tree/master/ivonet
"""

import os
import unittest
from pathlib import Path

import sys

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def rock_formation(t, y):
    if t == 0:
        return {(2, y), (3, y), (4, y), (5, y)}  # -
    elif t == 1:
        return {(3, y + 2), (2, y + 1), (3, y + 1), (4, y + 1), (3, y)}  # +
    elif t == 2:
        return {(2, y), (3, y), (4, y), (4, y + 1), (4, y + 2)}  # reversed L
    elif t == 3:
        return {(2, y), (2, y + 1), (2, y + 2), (2, y + 3)}  # I
    elif t == 4:
        return {(2, y + 1), (2, y), (3, y + 1), (3, y)}  # square
    else:
        assert False


def left(rock):
    if any([x == 0 for (x, y) in rock]):
        return rock
    return set([(x - 1, y) for (x, y) in rock])


def right(rock, border=7):
    if any([x == border - 1 for (x, y) in rock]):
        return rock
    return set([(x + 1, y) for (x, y) in rock])


def down(rock):
    return set([(x, y - 1) for (x, y) in rock])


def up(rock):
    return set([(x, y + 1) for (x, y) in rock])


def part_1(source, wide=7, rocks_fall=2022):
    return None


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows(""">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>""")

    def test_example_data_part_1(self):
        self.assertEqual(3068, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(3130, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(1514285714288, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(1556521739139, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
