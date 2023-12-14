#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
https://www.eiu.edu/math/pdf/Gregory_Galperin_February_24_2017.pdf
https://www.youtube.com/watch?v=ea7lJkEhytA
"""

import sys
import unittest
from copy import copy
from itertools import groupby
from pathlib import Path

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False
print()


# noinspection DuplicatedCode
def p(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def part_1(source, times=40):
    """Nice use of the groupby function it made doing this very easy
    maybe not the most performant but fast enough
    """
    number = copy(source)
    for _ in range(times):
        p(number)
        ret = ""
        for label, group in groupby(number):
            g = list(group)
            ret += str(len(g))
            ret += g[0]
        number = ret

    return len(number)


def part_2(source):
    return part_1(source, 50)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}.input")))

    def test_part_1(self):
        self.assertEqual(492982, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(6989950, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
