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

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


class Towels:

    def __init__(self, source):
        self.source = source
        self.towels = [x.strip() for x in source[0].split(", ")]
        self.designs = source[2:]
        self.valid = {}

    def valid_ways(self, design):
        """
        Recursive function to calculate the number of valid ways to create a design with the available towels
        """
        if design in self.valid:
            return self.valid[design]
        ans = 0
        if not design:  # terminator
            ans = 1
        for towel in self.towels:
            if design.startswith(towel):
                ans += self.valid_ways(design[len(towel):])  # recursive call
        self.valid[design] = ans
        return ans

    def part_1(self):
        return sum(1 for design in self.designs if self.valid_ways(design) > 0)

    def part_2(self):
        return sum(self.valid_ways(design) for design in self.designs)


@debug
@timer
def part_1(source) -> int | None:
    towel = Towels(source)
    answer = towel.part_1()
    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:
    """Purely by accident I found out that I actually first found
    the part 2 solution while solving part 1 so that helped :-)"""
    towel = Towels(source)
    answer = towel.part_2()
    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(6, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(260, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(16, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(639963796864990, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
