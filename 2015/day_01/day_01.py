#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """ Day 1: Not Quite Lisp ---
Santa was hoping for a white Christmas, but his weather machine's "snow" function is powered by stars, and he's fresh out! To save Christmas, he needs you to collect fifty stars by December 25th.

Collect stars by helping Santa solve puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

Here's an easy puzzle to warm you up.

Santa is trying to deliver presents in a large apartment building, but he can't find the right floor - the directions he got are a little confusing. He starts on the ground floor (floor 0) and then follows the instructions one character at a time.

An opening parenthesis, (, means he should go up one floor, and a closing parenthesis, ), means he should go down one floor.

The apartment building is very tall, and the basement is very deep; he will never find the top or bottom floors.

For example:

(()) and ()() both result in floor 0.
((( and (()(()( both result in floor 3.
))((((( also results in floor 3.
()) and ))( both result in floor -1 (the first basement level).
))) and )())()) both result in floor -3.
To what floor do the instructions take Santa?

Your puzzle answer was 232.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
Now, given the same instructions, find the position of the first 
character that causes him to enter the basement (floor -1). The first 
character in the instructions has position 1, the second character has position 2, and so on.

For example:

) causes him to enter the basement at character position 1.
()()) causes him to enter the basement at character position 5.
What is the position of the character that causes Santa to first enter the basement?
"""

import sys
import unittest
from pathlib import Path

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def part_1(source):
    print(source)
    return sum(1 if x == "(" else -1 for x in source)


def part_2(source):
    level = 0
    for i, c in enumerate(source):
        if c == "(":
            level += 1
        else:
            level -= 1
        if level < 0:
            return i + 1
    raise ValueError("Not ever in basement")


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = ints(Path(__file__).name)[0]
        self.source = read_data(f"day_{day:02}.input")

    def test_example_data_part_1(self):
        self.assertEqual(0, part_1("(())"))
        self.assertEqual(0, part_1("()()"))
        self.assertEqual(3, part_1("((("))
        self.assertEqual(3, part_1("(()(()("))
        self.assertEqual(-1, part_1("())"))
        self.assertEqual(-1, part_1("))("))

    def test_part_1(self):
        self.assertEqual(232, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(1, part_2(")"))
        self.assertEqual(5, part_2("()())"))

    def test_part_2(self):
        self.assertEqual(1783, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
