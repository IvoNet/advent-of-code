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

DEBUG = False


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)

class Stone:

    def __init__(self, number: int):
        self.number: int = number
        self.blinks = 0

    def blink(self):
        self.blinks += 1
        if self.number == 0:
            self.number = 1
            return
        length = len(str(self.number))
        if length > 0 and length % 2 == 0:
            left = int(str(self.number)[:length // 2])
            right = int(str(self.number)[length // 2:])
            self.number = left
            return Stone(right) # right
        self.number = self.number * 2024

    def __repr__(self):
        return f"Stone({self.number})"


def blinks(source, times):
    answer = 0
    stones = [Stone(x) for x in ints(source[0])]
    stone_state = []
    for i in range(times):
        for stone in stones:
            split = stone.blink()
            stone_state.append(stone)
            if split:
                stone_state.append(split)
        answer = len(stone_state)
        p(stone_state)
        stones = stone_state.copy()
        stone_state = []
    return answer


@debug
@timer
def part_1(source) -> int | None:
    answer = blinks(source, 25)
    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:
    answer = blinks(source, 75)
    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(55312, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(183248, part_1(self.source))

    def test_part_2(self) -> None:
        self.assertEqual(None, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
