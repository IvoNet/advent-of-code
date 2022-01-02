#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from pathlib import Path

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

START = 20151125
DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def triangle_number(col: int) -> int:
    """https://en.wikipedia.org/wiki/Triangular_number"""
    return int((col * (col + 1)) / 2)


def lazy_caterer(row: int) -> int:
    """https://en.wikipedia.org/wiki/Lazy_caterer%27s_sequence"""
    return 1 + triangle_number(row - 1)


def code_gen():
    ret = START
    while True:
        yield ret
        ret = (ret * 252533) % 33554393


def value(row, col):
    """Get the laze"""
    it = lazy_caterer(row)
    for i in range(1, col):
        it += row + i
    for i, code in enumerate(code_gen()):
        if i == it - 1:
            return code


def part_1(source):
    row, col = ints(source)
    return value(row, col)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}.input")))

    def test_part_1(self):
        self.assertEqual(8997277, part_1(self.source))


if __name__ == '__main__':
    unittest.main()
