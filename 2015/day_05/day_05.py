#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import re
import sys
import unittest
from itertools import groupby
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints, consecutive_element_pairing

sys.dont_write_bytecode = True

DEBUG = False

WRONG = [
    "ab",
    "cd",
    "pq",
    "xy",
]


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def nice(word):
    for w in WRONG:
        if w in word:
            return False
    if len(re.findall("[aeiou]", word)) < 3:
        return False
    if max([(label, sum(1 for _ in group)) for label, group in groupby(word)], key=lambda x: x[1])[1] < 2:
        return False
    return True


def rule_two_letters_repeated(word: str) -> bool:
    for pair in consecutive_element_pairing(list(word), 2, lambda z: "".join([str(x) for x in z])):
        if len(re.findall(pair, word)) >= 2:
            return True
    return False


def rule_three_letters_beginning_and_end_same(word: str) -> bool:
    for part in consecutive_element_pairing(list(word), 3, lambda z: "".join([str(x) for x in z])):
        if part.endswith(part[0]):
            return True
    return False


def nice_v2(word):
    if not rule_two_letters_repeated(word):
        return False
    if not rule_three_letters_beginning_and_end_same(word):
        return False
    return True


def part_1(source):
    return sum(1 for word in source if nice(word))


def part_2(source):
    return sum(1 for word in source if nice_v2(word))


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}.input")))
        self.test_source = read_rows("""ugknbfddgicrmopn
aaa
jchzalrnumimnmhp
haegwjzuvuyypxyu
dvszwmarrgswjxmb""")

    def test_example_data_part_1(self):
        self.assertEqual(2, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(258, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(53, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
