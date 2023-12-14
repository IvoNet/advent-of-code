#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2022 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
If a part of the code is not part of the gist it is probably 
code I found reusable and I may have moved it to my 'ivonet' library.
you can find that here: https://github.com/IvoNet/advent-of-code/tree/master/ivonet
"""

import os
import sys
import unittest
from pathlib import Path

from ivonet.alphabet import alphabet
from ivonet.files import read_rows
from ivonet.iter import ints, groupify
from ivonet.str import common_elements

sys.dont_write_bytecode = True

DEBUG = False

letters = alphabet() + alphabet(True)


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def part_1(source):
    priority = 0
    for line in source:
        for char in common_elements(groupify(line, len(line) // 2)):
            priority += letters.index(char) + 1
    return priority


def part_2(source):
    groups = groupify(source, 3)
    priority = 0
    for group in groups:
        for char in common_elements(group):
            priority += letters.index(char) + 1
    return priority


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw""")

    def test_example_data_part_1(self):
        self.assertEqual(157, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(8233, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(70, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(2821, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
