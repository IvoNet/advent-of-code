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
from collections import Counter
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints
from ivonet.str import cat

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def diff(left, right):
    return sum(a != b for a, b in zip(left, right))


def common(left, right):
    return cat(a for a, b in zip(left, right) if a == b)


def part_1(source):
    two = 0
    three = 0
    for line in source:
        count = Counter(line)
        two += 1 if 2 in count.values() else 0
        three += 1 if 3 in count.values() else 0
    return two * three


def part_2(source):
    return common(*[i for i in source if any(diff(i, x) == 1 for x in source)])


def part_2_verbose_version(source):
    for i in source:
        for x in source:
            if diff(i, x) == 1:
                return common(i, x)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz""")

    def test_part_1(self):
        self.assertEqual(5434, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual("fgij", part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual("agimdjvlhedpsyoqfzuknpjwt", part_2(self.source))

    def test_part_2_verbose(self):
        self.assertEqual("agimdjvlhedpsyoqfzuknpjwt", part_2_verbose_version(self.source))


if __name__ == '__main__':
    unittest.main()
