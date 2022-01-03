#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """"""

import os
import re
import sys
import unittest
from pathlib import Path

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def decompress_v1(source):
    result = ""
    while True:
        match = re.search("\(([0-9]+)x([0-9]+)\)", source)
        if not match:
            result += source
            return result
        begin, end = match.span()
        length, times = [int(x) for x in match.groups()]
        result += source[:begin]
        result += source[end:end + length] * times
        source = source[end + length:]


def decompress_v2(source):
    """part 2"""
    result = 0
    while True:
        match = re.search("\(([0-9]+)x([0-9]+)\)", source)
        if not match:
            return result + len(source)
        begin, end = match.span()
        length, times = [int(x) for x in match.groups()]
        result += len(source[:begin])
        result += decompress(source[end:end + length]) * times
        source = source[end + length:]


def decompress(source, version=2):
    """part 2"""
    result = 0
    while True:
        match = re.search("\(([0-9]+)x([0-9]+)\)", source)
        if not match:
            return result + len(source)
        begin, end = match.span()
        length, times = [int(x) for x in match.groups()]
        result += len(source[:begin])
        if version == 1:
            result += len(source[end:end + length]) * times
        else:
            result += decompress(source[end:end + length]) * times
        source = source[end + length:]


def part_1(source):
    return decompress(source, 1)


def part_2(source):
    return decompress(source)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")

    def test_example_1_part_1(self):
        self.assertEqual("ABBBBBC", decompress_v1("A(1x5)BC"))

    def test_example_2_part_1(self):
        self.assertEqual("XYZXYZXYZ", decompress_v1("(3x3)XYZ"))

    def test_example_3_part_1(self):
        self.assertEqual("ABCBCDEFEFG", decompress_v1("A(2x2)BCD(2x2)EFG"))

    def test_part_1(self):
        self.assertEqual(102239, part_1(self.source))

    def test_example_1_part_2(self):
        self.assertEqual(20, decompress("X(8x2)(3x3)ABCY"))

    def test_example_2_part_2(self):
        self.assertEqual(241920, part_2("(27x12)(20x12)(13x14)(7x10)(1x12)A"))

    def test_example_3_part_2(self):
        self.assertEqual(445, part_2("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN"))

    def test_part_2(self):
        self.assertEqual(10780403063, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
