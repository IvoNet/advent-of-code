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
import unittest
from pathlib import Path

import pyperclip
import sys
from ivonet.collection import max_k_subsequence
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


@debug
@timer
def part_1(source) -> int | None:
    answer = 0
    for line in source:
        b1 = -1
        b2 = -1
        for i, char in enumerate(line):
            digit = int(char)
            if digit > b1 and i != len(line) - 1:
                b1 = digit
                b2 = -1
            elif digit > b2:
                b2 = digit
            if b2 == 9:
                break
        p(f"Line: {line} -> {b1}+{b2}={int(str(b1)+str(b2))}")
        answer += int(str(b1)+str(b2))
    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:
    # Now we need to turn on exactly 12 batteries per line to make the largest joltage
    TARGET = 12
    answer = 0
    for line in source:
        line = line.strip()
        if not line:
            continue
        best = max_k_subsequence(line, TARGET)
        p(f"Line: {line} -> best {best}")
        answer += int(best)
    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(357, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(17166, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(3121910778619, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(169077317650774, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = Path(__file__).resolve().parent
        day = f"{ints(Path(__file__).stem)[0]:02}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
