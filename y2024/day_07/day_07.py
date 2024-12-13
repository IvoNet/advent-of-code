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
import itertools
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


class Test:
    def __init__(self, lst):
        self.test = lst[0]
        self.values = lst[1:]


def evaluate_expression(values, operators):
    result = values[0]
    for i in range(1, len(values)):
        if operators[i - 1] == '+':
            result += values[i]
        elif operators[i - 1] == '*':
            result *= values[i]
        elif operators[i - 1] == '||':  # added for part 2
            result = int(str(result) + str(values[i]))
    return result


def can_make_amount(t: Test, operators=('+', '*')):
    operator_permutations = list(itertools.product(operators, repeat=len(t.values) - 1))

    for perm in operator_permutations:
        if evaluate_expression(t.values, perm) == t.test:
            return True
    return False


def parse(source):
    bridge = []
    for line in source:
        bridge.append(Test(ints(line)))
    return bridge


@debug
@timer
def part_1(source, operators=('+', '*')) -> int | None:
    answer = 0
    bridge = parse(source)
    for t in bridge:
        if can_make_amount(t, operators=operators):
            answer += t.test

    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:
    answer = part_1(source, operators=('+', '*', '||'))
    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(3749, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(1430271835320, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(11387, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(456565678667482, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
