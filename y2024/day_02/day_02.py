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


def parse_source(source):
    return [ints(line) for line in source]


@debug
@timer
def part_1(source) -> int | None:
    answer = 0
    reports = parse_source(source)
    for levels in reports:
        answer = check_levels(answer, levels)
    answer = len(reports) - answer

    pyperclip.copy(str(answer))
    return answer


def check_levels(levels):
    answer = 0
    increase = levels[1] > levels[0]
    for idx, level in enumerate(levels[1:], 1):
        if increase:
            if level < levels[idx - 1]:
                answer += 1
                break
            if level == levels[idx - 1]:
                answer += 1
                break
            if level > levels[idx - 1]:
                if level - levels[idx - 1] > 3:
                    answer += 1
                    break
        else:
            if level > levels[idx - 1]:
                answer += 1
                break
            if level == levels[idx - 1]:
                answer += 1
                break
            if level < levels[idx - 1]:
                if levels[idx - 1] - level > 3:
                    answer += 1
                    break
    return answer == 0


@debug
@timer
def part_2(source) -> int | None:
    answer = 0
    reports = parse_source(source)
    for levels in reports:
        if check_levels(levels):
            answer += 1
        else:
            for i in range(0, len(levels)):
                new_levels = levels.copy()
                del new_levels[i]
                if check_levels(new_levels):
                    answer += 1
                    break
    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(2, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(224, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(4, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(293, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
