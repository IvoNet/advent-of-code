#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from pathlib import Path

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def part_1(source):
    print(source)
    return sum(1 if x == "(" else -1 for x in source)


def part_2(source):
    level = 0
    for i, c in enumerate(source):
        if c == "(":
            level += 1
        else:
            level -= 1
        if level < 0:
            return i + 1
    raise ValueError("Not ever in basement")


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = ints(Path(__file__).name)[0]
        self.source = read_data(f"day_{day:02}.input")

    def test_example_data_part_1(self):
        self.assertEqual(0, part_1("(())"))
        self.assertEqual(0, part_1("()()"))
        self.assertEqual(3, part_1("((("))
        self.assertEqual(3, part_1("(()(()("))
        self.assertEqual(-1, part_1("())"))
        self.assertEqual(-1, part_1("))("))

    def test_part_1(self):
        self.assertEqual(232, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(1, part_2(")"))
        self.assertEqual(5, part_2("()())"))

    def test_part_2(self):
        self.assertEqual(1783, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
