#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2022 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
If a part of the code is not part of the post it is probably 
code I found reusable and I may have moved it to my 'ivonet' library.
you can find that here: https://github.com/IvoNet/advent-of-code/tree/master/ivonet
"""

import os
import re
import unittest
from pathlib import Path
from string import digits

import sys

from ivonet.files import read_rows
from ivonet.iter import ints

NOT_FOUND = -1

sys.dont_write_bytecode = True

DEBUG = True

WRITTEN_DIGITS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

WRITTEN = {written: digit for digit, written in enumerate(WRITTEN_DIGITS, 1)}


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def combine_first_last_digits(line):
    digits = re.findall(r'\d', line)
    return int(digits[0] + digits[-1])


def part_1(source):
    total = 0
    for line in source:
        total += combine_first_last_digits(line)
    return total


def part_2(source):
    total = 0
    for line in source:
        numbers = set()
        for digit in digits:
            idx = line.find(digit)
            if idx > NOT_FOUND:
                numbers.add((idx, digit))
            idx = line.rfind(digit)
            if idx > NOT_FOUND:
                numbers.add((idx, digit))
        for digit, value in WRITTEN.items():
            idx = line.find(digit)
            if idx > NOT_FOUND:
                numbers.add((idx, value))
            idx = line.rfind(digit)
            if idx > NOT_FOUND:
                numbers.add((idx, value))
        numbers = list(numbers)
        _(numbers)
        numbers.sort(key=lambda x: x[0])
        _(numbers)
        total += int(f"{numbers[0][1]}{numbers[-1][1]}")
    return total


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""")
        self.test_source2 = read_rows("""two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen""")
        self.test_source3 = read_rows("""31onem18pcqkzsrnhqone1""")

    def test_example_data_part_1(self):
        self.assertEqual(142, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(55712, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(281, part_2(self.test_source2))

    def test_part_2(self):
        self.assertEqual(55413, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
