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


def part_1(source):
    steps = source[0].strip().split(",")
    answer=0
    for step in steps:
        current = 0
        for s in step:
            ascii = ord(s)
            current += ascii
            current *= 17
            current %= 256
        answer += current
    return answer





def part_2(source):
    return None


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
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
