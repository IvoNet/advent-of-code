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
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Claim(NamedTuple):
    id: int
    left: int
    top: int
    wide: int
    tall: int


def parse(source):
    return [Claim(*ints(line)) for line in source]


def visualise(fabric, width=1000, height=1000):
    for h in range(height):
        for w in range(width):
            print("." if not fabric[(h, w)] else len(fabric[(h, w)]), end="")
        print()


def process(source):
    claims = parse(source)
    fabric = defaultdict(list)
    for claim in claims:
        for h in range(claim.top, claim.top + claim.tall):
            for w in range(claim.left, claim.left + claim.wide):
                fabric[(h, w)].append(claim.id)
    return fabric


def part_1(source):
    return sum(1 for k, v in process(source).items() if len(v) > 1)


def part_2(source):
    fabric = process(source)
    single_squared_ids = set(v[0] for k, v in fabric.items() if len(v) == 1)
    for i in single_squared_ids:
        if not any(x for x in fabric.values() if i in x and len(x) > 1):
            return i
    return None


def part_2_for_fun(source):
    """Just playing with list comprehension"""
    fabric = process(source)
    return [i for i in set(v[0] for k, v in fabric.items() if len(v) == 1) if
            not any(x for x in fabric.values() if i in x and len(x) > 1)][0] or None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2""")

    def test_example_data_part_1(self):
        self.assertEqual(4, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(120419, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(3, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(445, part_2(self.source))

    def test_part_2_for_fun(self):
        self.assertEqual(445, part_2_for_fun(self.source))


if __name__ == '__main__':
    unittest.main()
