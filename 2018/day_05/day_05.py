#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """"""

import os
import re
import sys
import unittest
from pathlib import Path

from ivonet.alphabet import alphabet
from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def reacting(source, remove=None):
    l = alphabet(upper=False)
    lu = "|".join(["".join(x) for x in list(zip(l, l.upper()))])
    ul = "|".join(["".join(x) for x in list(zip(l.upper(), l))])
    regex = f"{lu}|{ul}"
    pat = re.compile(regex)
    ret = source
    if remove:
        ret = re.sub(remove, "", ret)
    while True:
        exploded = pat.sub("", ret)
        if len(exploded) == len(ret):
            break
        ret = exploded
    return len(ret)


def part_1(source):
    return reacting(source)


def part_2(source):
    units = ["|".join(x) for x in list(zip(alphabet(), alphabet(True)))]
    return min(reacting(source, unit) for unit in units)


def part_2_orig(source):
    units = ["|".join(x) for x in list(zip(alphabet(), alphabet(True)))]
    shortest_polymer = None
    shortest = float("inf")
    for unit in units:
        ret = source
        length, polymer = reacting(ret, unit)
        if length < shortest:
            shortest_polymer = polymer
            shortest = length
    return len(shortest_polymer)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_data("""dabAcCaCBAcCcaDA""")

    def test_example_data_part_1(self):
        self.assertEqual(10, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(10972, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(4, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(5278, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
