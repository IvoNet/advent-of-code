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
from pathlib import Path

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def part_1(source):
    """sum occurences as long as the next is the same
    the modulo function is a nice way to wrap the last around to the first
    """
    return sum(int(source[i]) for i in range(len(source)) if source[i] == source[(i + 1) % len(source)])


def part_2(source):
    return sum(int(source[i]) for i in range(len(source)) if source[i] == source[(i + len(source) // 2) % len(source)])


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")

    def test_part_testdata_1(self):
        self.assertEqual(3, part_1("1122"))
        self.assertEqual(4, part_1("1111"))
        self.assertEqual(0, part_1("1234"))
        self.assertEqual(9, part_1("91212129"))

    def test_part_1(self):
        self.assertEqual(1069, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
