#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from pathlib import Path

from ivonet.files import read_rows, read_data
from ivonet.iter import ints
from hashlib import md5
sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def part_1(key):
    idx = 0
    while True:
        answer = f"{key}{idx}".encode("ascii")
        if md5(answer).hexdigest().startswith("00000"):
            break
        idx += 1
    return idx


def part_2(key):
    idx = 0
    while True:
        answer = f"{key}{idx}".encode("ascii")
        if md5(answer).hexdigest().startswith("000000"):
            break
        idx += 1
    return idx


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"day_{day.zfill(2)}.input")
        self.test_source = read_data("""abcdef""")

    def test_example_data_part_1(self):
        self.assertEqual(609043, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(282749, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(9962624, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
