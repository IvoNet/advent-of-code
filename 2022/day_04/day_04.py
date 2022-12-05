#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2022 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
If a part of the code is not part of the gist it is probably 
code I found reusable and I may have moved it to my 'ivonet' library.
you can find that here: https://github.com/IvoNet/advent-of-code/tree/master/ivonet
"""

import os
import sys
import unittest
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints, groupify, rangei, positive_ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def expand_group(group):
    ret = ""
    for x in rangei(group[0], group[1]):
        ret += str(x)
    return ret


def part_1(source):
    full_container = []
    for x in source:
        group1, group2 = groupify(positive_ints(x), 2)
        start1, stop1 = group1
        start2, stop2 = group2
        if start1 >= start2 and stop1 <= stop2:
            full_container.append(x)
            continue
        if start2 >= start1 and stop2 <= stop1:
            full_container.append(x)
            continue

    _(full_container)
    return len(full_container)


def part_2(source):
    overlaps = []
    for x in source:
        group1, group2 = groupify(positive_ints(x), 2)
        start1, stop1 = group1
        start2, stop2 = group2
        if start2 <= start1 <= stop2 or stop2 >= stop1 >= start2:
            overlaps.append(x)
            continue
        if start1 <= start2 <= stop1 or stop1 >= stop2 >= start1:
            overlaps.append(x)
            continue

    _(overlaps)
    return len(overlaps)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8""")

    def test_example_data_part_1(self):
        self.assertEqual(2, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(459, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(4, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(779, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
