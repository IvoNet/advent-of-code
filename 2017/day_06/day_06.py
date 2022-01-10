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
from itertools import count
from pathlib import Path

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def part_1(source, part2=False):
    reg = ints(source)
    seen = []
    for steps in count(1):
        dist = max(reg)
        pos = reg.index(dist)
        reg[pos] = 0
        for idx in range(pos + 1, pos + 1 + dist):
            reg[idx % len(reg)] += 1

        state = tuple(x for x in reg)
        _(state)
        if state in seen:
            if part2:
                return steps - 1 - seen.index(state)
            return steps
        seen.append(state)


def part_2(source):
    return part_1(source, part2=True)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_data("""0 2 7 0""")

    def test_example_data_part_1(self):
        self.assertEqual(5, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(4074, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(4, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(2793, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
