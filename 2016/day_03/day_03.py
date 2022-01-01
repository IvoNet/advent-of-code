#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from itertools import permutations
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints, chunkify

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def prepare(source):
    return [ints(x) for x in source]


def valid(potential):
    """Tests all permutations of the three element tuple
    which is easy and fast enough but also in percentages 50% less efficient then the is_valid() method
    e.g.
    [(4, 21, 894),  # same as idx 2
     (4, 894, 21),  # same as idx 4
     (21, 4, 894),  # same as idx 0
     (21, 894, 4),  # etc...
     (894, 4, 21),
     (894, 21, 4)]
    """
    for combi in permutations(potential):
        if combi[0] + combi[1] <= combi[2]:
            return False
    return True


def is_valid(potential):
    """More verbose but also more precise then the valid method as it tests 50% less than the permutations
    """
    return (potential[0] + potential[1] > potential[2]) \
           and (potential[1] + potential[2] > potential[0]) \
           and (potential[2] + potential[0] > potential[1])


def part_1(source, valid_check=is_valid):
    total = 0
    data = prepare(source)
    for option in data:
        if valid_check(option):
            total += 1
    return total


def part_2(source, valid_check=is_valid):
    data = prepare(source)
    total = 0
    for col in zip(*data):  # transpose cols to rows
        for option in chunkify(col, 3):  # Re-chunkify the new rows into groups of three
            if valid_check(option):
                total += 1
    return total


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"day_{day.zfill(2)}.input")

    def test_part_1(self):
        self.assertEqual(983, part_1(self.source, valid_check=valid))

    def test_part_2(self):
        self.assertEqual(1836, part_2(self.source, valid_check=valid))

    def test_part_1_v2(self):
        self.assertEqual(983, part_1(self.source, valid_check=is_valid))

    def test_part_2_v2(self):
        self.assertEqual(1836, part_2(self.source, valid_check=is_valid))


if __name__ == '__main__':
    unittest.main()
