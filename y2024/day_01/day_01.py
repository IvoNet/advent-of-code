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
import unittest
from pathlib import Path

import pyperclip
import sys

from ivonet.decorators import debug, timer
from ivonet.files import read_rows
from ivonet.iter import ints

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def parse_source(source):
    left, right = zip(*[ints(line) for line in source])
    return left, right


@debug
@timer
def part_1(source) -> int | None:
    answer = 0
    left, right = parse_source(source)
    for i, j in zip(sorted(left), sorted(right)):
        answer += abs(i - j)
    print(source)
    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:
    answer = 0
    left, right = parse_source(source)
    for i in left:
        #     count the number of times i in left occurs in right
        answer += i * right.count(i)

    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(11, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(1889772, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(31, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(23228917, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
