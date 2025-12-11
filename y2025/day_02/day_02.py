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
from ivonet.decorators import debug
from ivonet.decorators import timer
from ivonet.files import read_rows, read_data
from ivonet.iter import ints

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


@debug
@timer
def part_1(source) -> int | None:
    count_wrong_ids = 0
    ranges = source.split(",")
    for r in ranges:
        a, b = r.split("-")
        start = int(a)
        end = int(b)
        for n in range(start, end + 1):
            s = str(n)
            first_half = s[:len(s)//2]
            second_half = s[len(s)//2:]
            if first_half == second_half and first_half[0] != '0':
                p(f"Invalid ID found: {s}")
                count_wrong_ids += n
    pyperclip.copy(str(count_wrong_ids))
    return count_wrong_ids


@debug
@timer
def part_2(source) -> int | None:
    answer = 0
    ranges = source.split(",")
    for r in ranges:
        a, b = r.split("-")
        start = int(a)
        end = int(b)
        for n in range(start, end + 1):
            s = str(n)
            # Check if the string is made of a repeating pattern
            # Try all possible pattern lengths from 1 to len(s)//2
            is_invalid = False
            for pattern_len in range(1, len(s) // 2 + 1):
                if len(s) % pattern_len == 0:  # Only check if pattern can divide evenly
                    pattern = s[:pattern_len]
                    # Check if the entire string is this pattern repeated
                    if pattern * (len(s) // pattern_len) == s:
                        # Valid repeating pattern found (at least 2 repetitions)
                        is_invalid = True
                        p(f"Invalid ID found: {s:10} (pattern '{pattern:6}' repeated {len(s) // pattern_len:3} times)")
                        break
            if is_invalid:
                answer += n
    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(1227775554, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(28846518423, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(4174379265, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(31578210022, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = Path(__file__).resolve().parent
        day = f"{ints(Path(__file__).stem)[0]:02}"
        self.source = read_data(f"{folder}/day_{day}.input", )
        self.test_source = read_data(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
