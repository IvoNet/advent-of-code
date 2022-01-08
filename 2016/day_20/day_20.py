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
    """Create a sorted list of the input of ranges(low, high) so that we can start from zero"""
    return sorted([ints(line.replace("-", " ")) for line in source])


def valid_ip(data, ip):
    """Test if an ip is valid
    Valid when:
    - not in one of the ranges in the data
    - not higher than highest IP allowed
    """
    for start, end in data:
        if start <= ip <= end:
            break
    else:
        if ip <= 4294967295:  # or n < 2 ** 32
            return True
    return False


def process(source):
    """
    A candidate is:
    - always 1 higher than a highest in a range
    - must not fall in a range of another
    - must not be higher than the allowed highest value
    """
    data = parse(source)
    candidates = [x[1] + 1 for x in data]
    valids = [ip for ip in candidates if valid_ip(data, ip)]
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
