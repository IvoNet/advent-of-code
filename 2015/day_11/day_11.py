#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from copy import copy
from itertools import groupby
from pathlib import Path

from ivonet.alphabet import alphabet
from ivonet.files import read_data
from ivonet.iter import ints, consecutive_element_pairing

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Password:

    def __init__(self) -> None:
        self.alphabet = list(alphabet(upper=False))
        self.letters = copy(self.alphabet)
        self.not_allowed = "iol"
        self.threes = consecutive_element_pairing(self.alphabet, elements=3,
                                                  map_to_func=lambda x: "".join(x))
        for na in self.not_allowed:
            self.letters.remove(na)
            for three in self.threes.copy():
                if na in three:
                    self.threes.remove(three)

    def consecutive_three(self, item: str) -> bool:
        for three in self.threes:
            if three in item:
                return True
        return False

    @staticmethod
    def double_double(item: str) -> bool:
        found = 0
        for label, group in groupby(item):
            g = list(group)
            if len(g) >= 2:
                found += 1
        return found >= 2

    def allowed_chars(self, item):
        for na in self.not_allowed:
            if na in item:
                return False
        return True

    def valid(self, item: str) -> bool:
        return self.consecutive_three(item) and self.double_double(item) and self.allowed_chars(item) and len(item) == 8

    def next_word(self, word: str):
        wrd = list(word)
        while True:
            for i in range(1, len(wrd)):
                pos = (i - 1) % 8 + 1
                nl = ((ord(wrd[-pos]) - ord("a") + 1) % 26)
                nl = self.alphabet[nl]
                wrd[-pos] = nl
                if nl != "a":
                    return "".join(wrd)

    def __generate_password(self, item):
        nxt = self.next_word(item)
        while not self.valid(nxt):
            nxt = self.next_word(nxt)
        return nxt

    def next(self, item):
        return self.__generate_password(item)


def part_1(source):
    return Password().next(source)


def part_2(source):
    return Password().next(part_1(source))


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}.input")))
        self.test_source = """hijklmmn"""
        self.test_source_1 = """abbceffg"""
        self.test_source_2 = """abbcegjk"""

    def test_straight_three(self):
        pwd = Password()
        self.assertTrue(pwd.consecutive_three("abcdefgh"))
        self.assertFalse(pwd.consecutive_three(self.test_source))
        self.assertFalse(pwd.consecutive_three(self.test_source_1))

    def test_double_letters(self):
        pwd = Password()
        self.assertFalse(pwd.double_double(self.test_source))
        self.assertTrue(pwd.double_double(self.test_source_1))

    def test_allowed(self):
        pwd = Password()
        self.assertFalse(pwd.allowed_chars(self.test_source))
        self.assertTrue(pwd.allowed_chars(self.test_source_1))

    def test_valid(self):
        pwd = Password()
        self.assertTrue(pwd.valid("abcdffaa"))
        self.assertFalse(pwd.allowed_chars("ghijklmn"))
        self.assertFalse(pwd.allowed_chars("ghijk"))

    def test_next_word(self):
        self.assertEqual("abcdffaa", Password().next_word("abcdfezz"))

    def test_next_password(self):
        self.assertEqual("ghjaabcc", Password().next("ghijklmn"))

    def test_part_1(self):
        self.assertEqual("vzbxxyzz", part_1(self.source))

    def test_part_2(self):
        self.assertEqual("vzcaabcc", part_2(self.source))


if __name__ == '__main__':
    unittest.main()
