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
from typing import NamedTuple

from ivonet.files import read_ints
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Tree(NamedTuple):
    kids: int
    metadata: list


def parse(source):
    kids, num_metas, rest = source[0], source[1], source[2:]
    total = 0
    for _ in range(kids):
        sub_total, rest = parse(rest)
        total += sub_total
    metas, rest = rest[:num_metas], rest[num_metas:]
    total += sum(metas)
    return total, rest


def part_1(source):
    return parse(source)[0]


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_ints(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input", delimiter=" ")
        self.test_source = read_ints("""2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2""", delimiter=" ")

    def test_example_data_part_1(self):
        self.assertEqual(138, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(41028, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
