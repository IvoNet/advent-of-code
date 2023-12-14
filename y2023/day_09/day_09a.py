#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2023 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
If a part of the code is not part of the post it is probably 
code I found reusable and I may have moved it to my 'ivonet' library.
you can find that here: https://github.com/IvoNet/advent-of-code/tree/master/ivonet
"""

import operator
import os
import unittest
from pathlib import Path

import sys

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def extrapolate(sequence: list[int], after: bool = True) -> int:
    """
    This function calculates the next number in a sequence based on the differences between consecutive numbers.

    Parameters:
    sequence (list): A list of integers representing the sequence.
    after (bool): A boolean value indicating whether to extrapolate after the last number in the sequence (True)
                  or before the first number in the sequence (False). Default is True.

    Returns:
    int: The extrapolated number.

    The function works as follows:
    - If all numbers in the sequence are 0, it returns 0.
    - It calculates the differences between consecutive numbers in the sequence and stores them in a list
      called 'deltas'.
    - It recursively calls itself with 'deltas' as the new sequence until all numbers in the sequence are 0.
    - It then adds or subtracts (based on the 'after' parameter) the last calculated difference from the last
      number in the original sequence and returns this as the extrapolated number.
    """
    if all(x == 0 for x in sequence):
        return 0

    deltas = [y - k for k, y in zip(sequence, sequence[1:])]  # zip the sequence of itself with itself offset by 1
    diff = extrapolate(deltas, after=after)  # recursive call
    op = operator.add if after else operator.sub
    return op(sequence[-1 if after else 0], diff)


def process_v1(source, after=True):
    total = 0
    for line in source:
        numbers = list(map(int, line.split()))
        total += extrapolate(numbers, after=after)
    return total


def process(source, after=True):
    return sum(extrapolate(list(map(int, line.split())), after=after) for line in source)


def part_1(source):
    return process(source)


def part_2(source):
    return process(source, after=False)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""")
        self.test_source2 = read_rows(
            """14 32 68 137 255 452 812 1561 3234 6964 14963 31344 63637 125819 244669 473255 919206 1802524 3570270 7116863 14193811""")

    def test_example_data_part_1(self):
        self.assertEqual(114, part_1(self.test_source))

    def test_source2(self):
        self.assertEqual(28148226, part_1(self.test_source2))

    def test_part_1(self):
        self.assertEqual(1930746032, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(2, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(1154, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
