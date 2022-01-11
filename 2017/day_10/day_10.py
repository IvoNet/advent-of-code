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
from copy import deepcopy
from pathlib import Path

from ivonet.files import read_ints
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Knotter:

    def __init__(self, sequence, circle=256) -> None:
        self.sequence = sequence
        self.skip = 0
        self.head = 0
        self.circle = list(range(circle))
        self.size = len(self.circle)

    def step(self):
        for step in self.sequence:
            _("step", step, "head", self.head, "skip", self.skip)
            yield self._next(step)
            self.head = (self.head + step + self.skip) % self.size
            self.skip += 1

    def _next(self, step):
        new = deepcopy(self.circle)
        for i in range(step):
            new[(self.head + i) % self.size] = self.circle[(self.head + step - i - 1) % self.size]
        self.circle = new
        return self.circle

    def hash_1(self):
        for i, c in enumerate(self.step()):
            _(i, c)
        return self.circle[0] * self.circle[1]


def part_1(source, circle=256):
    return Knotter(source, circle=circle).hash_1()


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_ints(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input", delimiter=",")
        self.test_source = read_ints("""3,4,1,5""", delimiter=",")

    def test_example_data_part_1(self):
        self.assertEqual(12, part_1(self.test_source, circle=5))

    def test_part_1(self):
        self.assertEqual(None, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
