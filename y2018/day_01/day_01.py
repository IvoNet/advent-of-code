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
from itertools import count
from pathlib import Path

from ivonet.files import read_ints
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def part_1(source):
    return sum(source)


def part_2(source):
    frequencies = set()
    freq = 0
    for i in count():
        for hz in source:
            freq += hz
            if freq in frequencies:
                return freq
            frequencies.add(freq)
        _(i, end=" ")


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_ints(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")

    def test_part_1(self):
        self.assertEqual(513, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(287, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
