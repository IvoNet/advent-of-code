#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import re
import sys
import unittest
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def parse(source):
    molecule = source[-1]
    replacements = [(x[0], x[2]) for x in [y.strip().split() for y in source[:-2]]]
    return molecule, replacements


def calibrate(replacements, molecule):
    """Yields all combinations without making it unique"""
    for key, value in replacements:
        for m in re.finditer(key, molecule):
            yield molecule[:m.start()] + value + molecule[m.end():]


def reverse_engineer(replacements, molecule):
    """Note that the key, value has been reversed in this loop!
    Reverse enginering you know :-)"""
    for value, key in replacements:
        for m in re.finditer(key, molecule):
            yield molecule[:m.start()] + value + molecule[m.end():]


def part_1(source):
    molecule, replacements = parse(source)
    return len(set(list(calibrate(replacements, molecule))))


def part_2(source):
    """To build a molecule we need to start with 'e', so in order to get to build the molecule we already have
    as a starting point we need to reverse engineer back to e.
    Replacements in reverse and than look at the shortest path to e
    """
    molecule, replacements = parse(source)

    idx = 0
    while molecule != "e":
        shortest_len = float("inf")
        shortest = None
        for candidate in reverse_engineer(replacements, molecule):
            s = len(candidate)
            if s < shortest_len:
                shortest_len = s
                shortest = candidate
        assert molecule is not None
        molecule = shortest
        idx += 1

    return idx


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"day_{day.zfill(2)}.input")
        self.test_source = read_rows("""H => HO
H => OH
O => HH

HOHOHO""")
        self.test_source = read_rows("""e => H
e => O
H => HO
H => OH
O => HH

HOHOHO""")

    def test_example_data_part_1(self):
        self.assertEqual(7, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(535, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(6, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(212, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
