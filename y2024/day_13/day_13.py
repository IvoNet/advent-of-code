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
from ivonet.iter import ints, rangei

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def parse(source):
    i = 0
    machines = []
    for line in source:
        i += 1
        if i == 1:
            a = ints(line)
        if i == 2:
            b = ints(line)
        if i == 3:
            prize = ints(line)
        if i == 4:
            machines.append((a, b, prize))
            a, b, c, = 0, 0, 0
        i %= 4
    if a and b and prize:
        machines.append((a, b, prize))

    return machines


@debug
@timer
def part_1(source) -> int | None:
    answer = 0
    machines = parse(source)
    for a, b, prize in machines:
        stop = False
        ax = a[0]
        ay = a[1]
        bx = b[0]
        by = b[1]
        px = prize[0]
        py = prize[1]
        for ai in rangei(1, 100):
            for bi in rangei(1, 100):
                axi = ax * ai
                ayi = ay * ai
                bxi = bx * bi
                byi = by * bi
                if axi + bxi == px and ayi + byi == py:
                    tokens = ai * 3 + bi * 1
                    answer += tokens
                    p("Found solution for", a, b, prize, "tokens", tokens)
                    stop = True
                if stop:
                    break
            if stop:
                break
        if not stop:
            p("No solution found for", a, b, prize)

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
        self.assertEqual(480, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(30413, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(None, part_2(self.test_source))

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
