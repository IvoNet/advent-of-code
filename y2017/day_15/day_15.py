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

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def generator(start: int, factor: int, divider: int = 2147483647):
    seed = start
    while True:
        seed = (seed * factor) % divider
        yield bin(seed)[2:].zfill(32)[-16:]


def part_1a(source):
    """This one works just fine but is expensive and therefore slow
    ~47 seconds on my machine.
    Pobably better not to do all these conversions ...
    """
    start_a = ints(source[0])[0]
    start_b = ints(source[1])[0]
    factor_a = 16807
    factor_b = 48271
    divider = 2147483647
    a = generator(start_a, factor_a, divider=divider)
    b = generator(start_b, factor_b, divider=divider)
    total = 0
    for _ in range(40_000_000):
        total += 1 if next(a) == next(b) else 0
    return total


def part_1(source):
    """Yes is faster :-) but still not all that fast"""
    state_a = ints(source[0])[0]
    state_b = ints(source[1])[0]
    factor_a = 16807
    factor_b = 48271
    divider = 2147483647
    two_pow_16 = 2 ** 16
    total = 0
    for _ in range(40_000_000):
        state_a = state_a * factor_a % divider
        state_b = state_b * factor_b % divider
        if (state_a % two_pow_16) == (state_b % two_pow_16):
            total += 1
    return total


def part_2(source):
    state_a = ints(source[0])[0]
    state_b = ints(source[1])[0]
    factor_a = 16807
    factor_b = 48271
    divider = 2147483647
    two_pow_16 = 2 ** 16
    list_a = []
    list_b = []
    _("Phase 1")

    while True:
        state_a = state_a * factor_a % divider
        if state_a % 4 == 0:
            list_a.append(state_a)
        state_b = state_b * factor_b % divider
        if state_b % 8 == 0:
            list_b.append(state_b)
        if len(list_a) >= 5_000_000 and len(list_b) >= 5_000_000:
            break
    _("Phase 2")
    total = 0
    for i in range(5_000_000):
        if (list_a[i] % two_pow_16) == (list_b[i] % two_pow_16):
            total += 1

    return total


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""65
8921""")

    def test_example_data_part_1(self):
        self.assertEqual(588, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(638, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(309, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(343, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
