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
from ivonet.files import read_data
from ivonet.iter import ints

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def parse(source):
    grids = source.split('\n\n')
    keys = []
    locks = []
    for grid in grids:
        grid = grid.split('\n')
        grid = [list(line) for line in grid]
        if "." in grid[0]:  # key
            keys.append(grid)
        else:
            locks.append(grid)
    return keys, locks


def fits(key, lock):
    for r in range(len(key)):
        for c in range(len(key[0])):
            if key[r][c] == '#' and lock[r][c] == '#':
                return False
    return True


@debug
@timer
def part_1(source) -> int | None:
    answer = 0
    keys, locks = parse(source)
    for key in keys:
        for lock in locks:
            if fits(key, lock):
                answer += 1
    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:
    answer = 0
    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(3, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(3264, part_1(self.source))

    def setUp(self) -> None:
        print()
        folder = Path(__file__).resolve().parent
        day = f"{ints(Path(__file__).stem)[0]:02}"
        self.source = read_data(f"{folder}/day_{day}.input")
        self.test_source = read_data(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
