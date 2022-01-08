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

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def part_1a(source):
    nr_of_elves = int(source)
    elves = {k: True for k in range(int(nr_of_elves))}
    for i in count():
        elf = i % nr_of_elves
        if elves[elf]:
            for l in count(i + 1):
                lelf = l % nr_of_elves
                if lelf != i and elves[lelf]:
                    elves[lelf] = False
                    break
        left = [k for k, v in elves.items() if v]
        if len(left) == 1:
            return left[0] + 1


def part_1(source):
    nr_of_elves = int(source)
    elves = list(range(1, int(nr_of_elves) + 1))
    elf = 0
    while len(elves) > 1:
        elf = (elf + 1) % len(elves)
        elves.pop(elf)
    return elves[0]


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")

    def test_example_data_part_1(self):
        self.assertEqual(3, part_1("5"))

    def test_part_1(self):
        self.assertEqual(None, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
