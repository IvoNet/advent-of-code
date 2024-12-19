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
import sys
import unittest
from pathlib import Path

import pyperclip
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


class Blinker:

    def __init__(self, source, times):
        self.stones = ints(source[0])
        self.times = times
        self.memoization = {} # This is the memoization cache and makes all the difference in speed

    def blink(self, number, steps):
        """Recursively blink one number for the amount of steps needed"""
        if (number, steps) in self.memoization:
            return self.memoization[(number, steps)]
        if steps == 0:
            ret = 1
        elif number == 0:
            ret = self.blink(1, steps - 1)
        elif len(str(number)) % 2 == 0:
            str_number = str(number)
            left = int(str_number[:len(str_number) // 2])
            right = int(str_number[len(str_number) // 2:])
            ret = self.blink(left, steps - 1) + self.blink(right, steps - 1)
        else:
            ret = self.blink(number * 2024, steps - 1)
        self.memoization[(number, steps)] = ret
        return ret

    def do_blinks(self):
        return sum(self.blink(stone, self.times) for stone in self.stones)


@debug
@timer
def part_1(source) -> int | None:
    blinker = Blinker(source, 25)
    answer = blinker.do_blinks()
    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:
    b = Blinker(source, 75)
    answer = b.do_blinks()
    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(55312, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(183248, part_1(self.source))

    def test_part_2(self) -> None:
        self.assertEqual(218811774248729, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
