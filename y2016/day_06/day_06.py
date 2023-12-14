#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """"""

import sys
import unittest
from collections import Counter
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def part_1(source):
    data = [list(x) for x in source]
    by_col = list(zip(*data))
    _(by_col)
    msg = "".join([Counter(x).most_common(1)[0][0] for x in by_col])
    _(msg)
    return msg


def part_2(source):
    data = [list(x) for x in source]
    by_col = list(zip(*data))
    msg = "".join([Counter(x).most_common()[-1][0] for x in by_col])
    _(msg)
    return msg


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}.input")))
        self.test_source = read_rows("""eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar""")

    def test_example_data_part_1(self):
        self.assertEqual("easter", part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual("ygjzvzib", part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual("advent", part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual("pdesmnoz", part_2(self.source))


if __name__ == '__main__':
    unittest.main()
