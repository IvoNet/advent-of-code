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


def parse_input(source):
    return [list(map(int, line.strip().split())) for line in source]


def generate_differences(sequence):
    sequences = [sequence]
    while any(sequences[-1]):
        sequences.append([j - i for i, j in zip(sequences[-1][:-1], sequences[-1][1:])])
    ret = list(reversed(sequences))
    # _(ret)
    return ret


def sum_differences_after(lst):
    result = 0
    for num in lst:
        result += num
    return result


def sum_differences_before(seqs):
    """
    formula for single step: result = seqs[i + 1] - before
    :param seqs:
    :return:
    """
    before = 0
    for i in range(len(seqs) - 1):
        before = seqs[i + 1] - before
    return before


def extrapolate_next(sequence):
    """
    formula for single step: result = seqs[i] + before
    :param sequence:
    :return:
    """
    seqs = [x[-1] for x in generate_differences(sequence)]
    return sum_differences_after(seqs)


def extrapolate_before(sequence):
    seqs = [x[0] for x in generate_differences(sequence)]
    _(seqs)
    return sum_differences_before(seqs)


def sum_extrapolated_next(sequences):
    return sum(list(extrapolate_next(sequence) for sequence in sequences))


def sum_extrapolated_before(sequences):
    return sum(list(extrapolate_before(sequence) for sequence in sequences))


def part_1(source):
    sequences = parse_input(source)
    return sum_extrapolated_next(sequences)


def part_2(source):
    sequences = parse_input(source)
    return sum_extrapolated_before(sequences)


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
