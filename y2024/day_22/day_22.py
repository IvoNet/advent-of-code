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
from collections import abc, defaultdict
from pathlib import Path

import pyperclip
import sys
from ivonet.decorators import debug
from ivonet.decorators import timer
from ivonet.files import read_rows
from ivonet.iter import ints

collections.Callable = abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def mix(left, right):
    """bitwise XOR operation on two integers."""
    return left ^ right


def prune(value):
    """Take the modulo 16777216 of the given value."""
    return value % 16777216


def secrets(value):
    """Generate a list of 2000 values based on the given value and provided formulae.
    - every rule must be mixed and pruned
    """
    ans = [value]
    for _ in range(2000):
        value = prune(mix(value, 64 * value))
        value = prune(mix(value, value // 32))
        value = prune(mix(value, value * 2048))
        ans.append(value)
    return ans


def prices(secrets):
    return [x % 10 for x in secrets]


def banana_score(prices):
    """
    - modulo 10
    - compare given with former and calc the difference. negative is minus prices, positive is plus prices
    - only the start is just a given as a reference point
    """
    answers = []
    for i in range(1, len(prices)):
        answers.append(prices[i] - prices[i - 1])
    return answers


def ranges(prices, bananas):
    """ get all ranges of 4 bananas and the price after that
    """
    ret = {}
    for i in range(len(bananas) - 3):
        pattern = (bananas[i], bananas[i + 1], bananas[i + 2], bananas[i + 3])
        if pattern not in ret:
            ret[pattern] = prices[i + 4]
    return ret


@debug
@timer
def part_1(source) -> int | None:
    """
    This is a simple sum of the last value of the secrets list.
    """
    answer = 0
    for line in source:
        pr = secrets(int(line))
        answer += pr[-1]
    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:
    """
    This is a bit more complex as we need to keep track of the ranges of 4 bananas and the price after that.
    We need to keep track of the total score for each range and return the highest score.
    """
    memory = defaultdict(int)  # init at 0
    for line in source:
        s = secrets(int(line))
        p = prices(s)
        b = banana_score(p)
        r = ranges(p, b)
        for k, v in r.items():
            memory[k] += v
    answer = max(memory.values())
    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_calculus(self):
        self.assertEqual(37, 42 ^ 15)  # bitwise xor
        self.assertEqual(16113920, 100000000 % 16777216)  # Prune
        self.assertEqual(3, 11 // 3)  # round down to nearest integer
        self.assertEqual(8685429, secrets(1)[-1])
        self.assertEqual(4700978, secrets(10)[-1])
        self.assertEqual(15273692, secrets(100)[-1])
        self.assertEqual(8667524, secrets(2024)[-1])
        self.assertEqual([-3, 6, -1, -1, 0, 2, -2, 0, -2], banana_score(prices(secrets(123))[:10]))

    def test_example_data_part_1(self) -> None:
        self.assertEqual(37327623, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(14623556510, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(23, part_2(self.test_source_1))

    def test_part_2(self) -> None:
        self.assertEqual(1701, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = Path(__file__).resolve().parent
        day = f"{ints(Path(__file__).stem)[0]:02}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")
        self.test_source_1 = read_rows(f"{folder}/test_{day}_1.input")


if __name__ == '__main__':
    unittest.main()
