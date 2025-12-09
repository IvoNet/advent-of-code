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
from itertools import zip_longest
from ivonet.calc import prod
from ivonet.collection import Stack
from ivonet.decorators import debug
from ivonet.decorators import timer
from ivonet.files import read_rows
from ivonet.iter import ints
from more_itertools.recipes import transpose

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)

def transpose_strict(lists):
    """Transpose when all inner lists have the same length."""
    return [list(col) for col in zip(*lists)]

def transpose_fill(lists, fill=" "):
    """Transpose even if inner lists differ in length; missing values are `fill`."""
    return [list(col) for col in zip_longest(*lists, fillvalue=fill)]


def parse(source):
    data = list(transpose([ints(line) for line in source[:-1]]))
    operators = [x for x in source[-1].split() if x in ('+', '*',)]
    length = len(operators)
    p(operators, length, data)
    if len(data) != length:
        p(len(data), length)
        raise ValueError("Inconsistent number of operators and data columns")
    return operators, data


@debug
@timer
def part_1(source) -> int | None:
    answer = 0
    operators, data = parse(source)
    p(operators)
    p(data)
    for i, op in enumerate(operators):
        if op == '+':
            answer += sum(data[i])
        elif op == '*':
            answer += prod(data[i])
    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:
    answer = 0
    operators = [x for x in source[-1].split() if x in ('+', '*',)]
    length = len(operators)
    data = transpose_fill([list(line) for line in source[:-1]])
    ll = []
    group = []
    for n in data:
        nr_str = "".join(str(x) for x in n if x != ' ')
        if not nr_str:
            ll.append(group)
            group = []
            continue
        nr = int(nr_str)
        group.append(nr)
    ll.append(group)
    for i, op in enumerate(operators):
        if op == '+':
            answer += sum(ll[i])
        elif op == '*':
            answer += prod(ll[i])


    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(4277556, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(5595593539811, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(3263827, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(None, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = Path(__file__).resolve().parent
        day = f"{ints(Path(__file__).stem)[0]:02}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
