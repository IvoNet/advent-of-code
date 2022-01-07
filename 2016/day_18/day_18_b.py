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
def p(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def trap(left, center, right):
    return left and center and not right or \
           not left and center and right or \
           not left and not center and right or \
           left and not center and not right


def generate_new_row(last_row):
    new = []
    for i in range(len(last_row)):
        left = last_row[i - 1] if i != 0 else False
        center = last_row[i]
        right = last_row[i + 1] if i != len(last_row) - 1 else False
        new.append(trap(left, center, right))
    return new


def part_1_2(source, row_count=40, to_count="."):
    rows = [[x == "^" for x in source]]  # convert to bool
    while len(rows) != row_count:
        rows.append(generate_new_row(rows[-1]))
    return sum(1 for x in rows for i in x if not i)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_data("""..^^.""")

    def test_example_data_part_1(self):
        self.assertEqual(6, part_1_2(self.test_source, row_count=3))

    def test_part_1(self):
        self.assertEqual(1961, part_1_2(self.source, row_count=40))

    def test_part_2(self):
        self.assertEqual(20000795, part_1_2(self.source, row_count=400000))


if __name__ == '__main__':
    unittest.main()
