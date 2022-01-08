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

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def parse(source):
    ret = []
    for line in source:
        l, h = ints(line.replace("-", " "))
        ret.append((l, h))
    return sorted(ret)


def valid_ip(data, n):
    for start, end in data:
        if start <= n <= end:
            break
    else:
        if n <= 4294967295:  # or n < 2 ** 32
            return True
    return False


def process(source):
    data = parse(source)
    upper_ranges = [x[1] + 1 for x in data]
    valids = [x for x in upper_ranges if valid_ip(data, x)]
    return min(valids), len(valids)


def part_1(source):
    return process(source)[0]


def part_2(source):
    return process(source)[1]


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""5-8
0-2
4-7""")

    def test_example_data_part_1(self):
        self.assertEqual(3, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(31053880, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(117, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
