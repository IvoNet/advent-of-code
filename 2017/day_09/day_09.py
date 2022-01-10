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
from queue import LifoQueue

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class GarbageCollector:

    def __init__(self, source) -> None:
        self.garbage_stream = source
        self.bucket = LifoQueue()
        self.ignore_next = False
        self.expected = None
        self.score = 0
        self.garbage_mode = False

    def collect(self) -> GarbageCollector:
        for ch in self.garbage_stream:
            if self.ignore_next:
                self.ignore_next = False
                continue
            if ch == "!":
                self.ignore_next = True
                continue
            if self.garbage_mode:
                if ch != ">":
                    # We could collect garbage here
                    continue
                self.garbage_mode = False
                continue
            if ch == "<":
                self.garbage_mode = True
                continue
            if ch == ",":
                continue
            if ch == "{":
                self.bucket.put("}")
                continue
            group = self.bucket.get()
            assert ch == group, "should be a group"
            if self.bucket.empty():
                self.score += 1
            else:
                self.score += self.bucket.qsize() + 1
        return self


def part_1(source):
    return GarbageCollector(source).collect().score


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_data("""""")

    def test_example_data_1_part_1(self):
        self.assertEqual(1, part_1("{}"))
        self.assertEqual(6, part_1("{{{}}}"))
        self.assertEqual(5, part_1("{{},{}}"))
        self.assertEqual(16, part_1("{{{},{},{{}}}}"))
        self.assertEqual(1, part_1("{<a>,<a>,<a>,<a>}"))
        self.assertEqual(9, part_1("{{<ab>},{<ab>},{<ab>},{<ab>}}"))
        self.assertEqual(9, part_1("{{<!!>},{<!!>},{<!!>},{<!!>}}"))
        self.assertEqual(3, part_1("{{<a!>},{<a!>},{<a!>},{<ab>}}"))

    def test_part_1(self):
        self.assertEqual(14204, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
