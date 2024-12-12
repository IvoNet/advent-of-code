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
from ivonet.files import read_data
from ivonet.iter import ints

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


PATTERN = r"mul\(\d{1,3},\d{1,3}\)"
PATTERN_DONT = r"don't\(\)"
PATTERN_DO = r"do\(\)"

@debug
@timer
def part_1(source) -> int | None:
    answer = 0
    matches = re.findall(PATTERN, source)
    for match in matches:
        left, right = ints(match)
        answer += left * right
    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:
    answer = 0
    donts = [m.start() for m in re.finditer(PATTERN_DONT, source)]
    dos = [m.start() for m in re.finditer(PATTERN_DO, source)]
    muls = [(m.start(), ints(m.group())) for m in re.finditer(PATTERN, source)]
    donts_and_dos = sorted(donts + dos)
    enabled = True
    for position, (left, right) in muls:
        for idx in donts_and_dos:
            if position > idx:
                enabled = idx in dos
        if enabled:
            answer += left * right

    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(161, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(183788984, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(48, part_2(self.test_source_p2))

    def test_part_2(self) -> None:
        self.assertEqual(62098619, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_data(f"{folder}/day_{day}.input")
        self.test_source = read_data(f"{folder}/test_{day}.input")
        self.test_source_p2 = read_data(f"{folder}/test_{day}_p2.input")


if __name__ == '__main__':
    unittest.main()
