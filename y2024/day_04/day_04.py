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

import collections
import os
import re
import unittest
from pathlib import Path

import pyperclip
import sys

from ivonet.decorators import debug
from ivonet.decorators import timer
from ivonet.files import read_rows
from ivonet.iter import ints

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


PATTERNS = ["XMAS", "SAMX"]
X_MAS = ["MAS", "SAM"]


def count_horizontal(source):
    return sum(sum(1 for _ in re.findall(pat, row)) for row in source for pat in PATTERNS)


def check_vertical_up(matrix, row, col, r, c):
    if r < len("XMAS") - 1:
        return False
    return "".join(matrix[r - i][c] for i in range(0, len("XMAS") + 1)) in PATTERNS


def check_vertical_down(matrix, row, col, r, c):
    if r + len("XMAS") > len(matrix):
        return False
    return "".join(matrix[r + i][c] for i in range(0, len("XMAS"))) in PATTERNS


def check_diagonally_down_left(matrix, row, col, r, c):
    if r + len("XMAS") > len(matrix) or c < len("XMAS") - 1:
        return False
    return "".join(matrix[r + i][c - i] for i in range(0, len("XMAS"))) in PATTERNS


def check_diagonally_down_right(matrix, row, col, r, c):
    if r + len("XMAS") > len(matrix) or c + len("XMAS") > len(row):
        return False
    return "".join(matrix[r + i][c + i] for i in range(0, len("XMAS"))) in PATTERNS


@debug
@timer
def part_1(source) -> int | None:
    answer = 0
    matrix = [list(row) for row in source]
    answer += count_horizontal(source)
    for r, row in enumerate(matrix):
        for c, col in enumerate(row):
            if col not in "XS":
                continue
            if check_vertical_up(matrix, row, col, r, c):
                p(f"VU Found at {r},{c}")
                answer += 1
            if check_vertical_down(matrix, row, col, r, c):
                p(f"VD Found at {r},{c}")
                answer += 1
            if check_diagonally_down_left(matrix, row, col, r, c):
                p(f"DL Found at {r},{c}")
                answer += 1
            if check_diagonally_down_right(matrix, row, col, r, c):
                p(f"DR Found at {r},{c}")
                answer += 1
    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:
    answer = 0
    matrix = [list(row) for row in source]
    rows = len(matrix)
    p(rows)
    p(list(range(1, rows - 1)))
    cols = len(matrix[0])
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if matrix[r][c] == "A":
                xl = matrix[r - 1][c - 1] + "A" + matrix[r + 1][c + 1]
                xr = matrix[r - 1][c + 1] + "A" + matrix[r + 1][c - 1]
                if xl in X_MAS and xr in X_MAS:
                    answer += 1

    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(18, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(2521, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(9, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(1912, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
