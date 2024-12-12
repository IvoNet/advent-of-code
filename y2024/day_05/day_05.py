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


def parse(source):
    rules = []
    updates = []
    for line in source:
        if "|" in line:
            rules.append(ints(line))
        elif line == "":
            pass
        else:
            updates.append(ints(line))
    return rules, updates


def valid(rules, update) -> (bool, tuple[int, int, int] | None):
    for idx, nr in enumerate(update):
        for left in update[:idx]:
            if [left, nr] not in rules:
                return False, (idx, left, nr)
        for right in update[idx + 1:]:
            if [nr, right] not in rules:
                return False, (idx, nr, right)
    return True, None


@debug
@timer
def part_1(source) -> int | None:
    answer = 0
    rules, updates = parse(source)
    p(rules)
    p(updates)
    for update in updates:
        if valid(rules, update)[0]:
            p("valid {}".format(update))
            middle = len(update) // 2
            answer += update[middle]
    pyperclip.copy(str(answer))
    return answer


def fix(rules, update, wrong):
    """fix the row so that it adheres to the rules"""
    upd = update.copy()
    idx, left, right = wrong
    if [right, left] in rules:
        upd[idx] = right
        upd[update.index(right)] = left
    return upd


@debug
@timer
def part_2(source) -> int | None:
    answer = 0
    rules, updates = parse(source)
    for update in updates:
        ok, wrong = valid(rules, update)
        upd = update.copy()
        if not ok:
            while not ok:
                p("invalid {}".format(upd))
                upd = fix(rules, upd, wrong)
                ok, wrong = valid(rules, upd)
            p("valid {}".format(upd))
            middle = len(upd) // 2
            answer += upd[middle]

    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(143, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(4872, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(123, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(5564, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
