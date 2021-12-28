#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import re
import sys
import unittest
from itertools import permutations
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
    molecule = source[-1]
    replacements = [(x[0], x[2]) for x in [y.strip().split() for y in source[:-2]]]
    return molecule, replacements


def count(replacements: dict, molecule: str):
    total = 0
    for k, v in replacements.items():
        nr = molecule.count(k)
        combi = list(permutations(v, min(len(v), nr)))
        total += len(combi) * nr
    return total


def calibrate(replacements, molecule):
    for k, v in replacements:
        for m in re.finditer(k, molecule):
            yield molecule[:m.start()] + v + molecule[m.end():]

def part_1(source):
    molecule, replacements = parse(source)
    return len(set(list(calibrate(replacements, molecule))))


def part_2(source):
    return 0


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"day_{day.zfill(2)}.input")
        self.test_source = read_rows("""H => HO
H => OH
O => HH

HOHOHO""")

    def test_example_data_part_1(self):
        self.assertEqual(7, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(535, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
