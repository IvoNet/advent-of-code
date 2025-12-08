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
from itertools import chain
from ivonet.decorators import debug
from ivonet.decorators import timer
from ivonet.files import read_rows
from ivonet.iter import ints, rangei, positive_ints

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def parse(source):
    ingredients = set()
    ranges = []
    for line in source:
        i = positive_ints(line)
        if len(i) == 0:
            continue
        if len(i) == 2:
            ranges.append(rangei(i[0], abs(i[1])))
        else:
            ingredients.add(i[0])
    return ingredients, ranges
    pass


def count_unique_numbers(ranges):
    for r in ranges:
        if r.step != 1:
            return len(set(chain.from_iterable(ranges)))

    intervals = [(r.start, r.stop) for r in ranges if r.start < r.stop]
    if not intervals:
        return 0

    intervals.sort()
    total = 0
    cur_s, cur_e = intervals[0]

    for s, e in intervals[1:]:
        if s <= cur_e:  # overlap or adjacent -> extend
            if e > cur_e:
                cur_e = e
        else:  # disjoint -> accumulate and start new
            total += cur_e - cur_s
            cur_s, cur_e = s, e

    total += cur_e - cur_s
    return total


@debug
@timer
def part_1(source) -> int | None:
    answer = 0
    ingredients, ranges = parse(source)
    for ingredient in ingredients:
        p(ingredient)
        for r in ranges:
            if ingredient in r:
                answer += 1
                break
    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:
    answer = 0
    _, ranges = parse(source)
    # unique_ids = {n for r in ranges for n in r}
    # unique_ids = set().union(*ranges)
    # unique_ids = set(chain.from_iterable(ranges))
    answer = count_unique_numbers(ranges)

    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(3, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(874, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(14, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(348548952146313, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = Path(__file__).resolve().parent
        day = f"{ints(Path(__file__).stem)[0]:02}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
