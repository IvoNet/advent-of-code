#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2023 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
If a part of the code is not part of the post it is probably 
code I found reusable and I may have moved it to my 'ivonet' library.
you can find that here: https://github.com/IvoNet/advent-of-code/tree/master/ivonet
"""

import collections
import os
import unittest
from collections import defaultdict
from pathlib import Path

collections.Callable = collections.abc.Callable

import sys

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def hash(step):
    current = 0
    for s in step:
        current += ord(s)
        current *= 17
        current %= 256
    return current


def part_1(source):
    steps = source[0].strip().split(",")
    return sum(hash(step) for step in steps)


def part_2(source):
    steps = source[0].strip().split(',')
    boxes = defaultdict(dict)
    for step in steps:
        if '=' in step:
            lens, num = step.split('=')
            boxes[hash(lens)][lens] = int(num)
        else:
            lens = step[:-1]
            boxes[hash(lens)].pop(lens, None)
    total = 0
    for box, lenses in boxes.items():
        for index, value in enumerate(lenses.values(), start=1):
            total += (box + 1) * index * value
    return total


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows(f"{os.path.dirname(__file__)}/test_{day.zfill(2)}.input")
        self.test_source2 = read_rows("""""")

    def test_example_data_part_1(self):
        self.assertEqual(52, part_1(["HASH"]))
        self.assertEqual(1320, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(497373, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(145, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(259356, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
