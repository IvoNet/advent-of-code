#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """"""

import os
import sys
import unittest
from pathlib import Path

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class ChocolateChart:

    def __init__(self) -> None:
        self.recipes_scores = [3, 7]
        self.cook_1 = 0
        self.cook_2 = 1
        self.round = 0

    def walk(self):
        """Repositions the cooks to their new 'current' recepies
        - 1 plus the score of their current recipe relative to their current pos
        """
        self.cook_1 = (self.cook_1 + 1 + self.recipes_scores[self.cook_1]) % len(self.recipes_scores)
        self.cook_2 = (self.cook_2 + 1 + self.recipes_scores[self.cook_2]) % len(self.recipes_scores)

    def cook(self):
        """Cook a recipe per cook"""
        self.round += 1
        base = self.recipes_scores[self.cook_1] + self.recipes_scores[self.cook_2]
        if base >= 10:
            self.recipes_scores.append(base // 10)
        self.recipes_scores.append(base % 10)
        self.walk()

    def scores(self, nr):
        """Get the 10 scores after the nr of recipes given."""
        while len(self.recipes_scores) < nr + 10:
            self.cook()
        return "".join(map(str, self.recipes_scores[nr:nr + 10]))

    def scores_left(self, digits: str):
        """The length of the number or recipes before the one where our digits can be found
        - get the 6 digits before our current pos
        - the last two recipes are new so don't count
        """
        position_space = 2
        while True:
            s = "".join(map(str, self.recipes_scores[-len(digits) - position_space:]))
            index = s.find(digits)
            if index >= 0:
                return index + len(self.recipes_scores) - len(digits) - position_space
            self.cook()

    def __repr__(self) -> str:
        return f"ChocolateChart<recipes={self.recipes_scores}, elf_1={self.cook_1}, elf_2={self.cook_2}, round={self.round}>"


def part_1(source):
    return ChocolateChart().scores(int(source))


def part_2(source):
    return ChocolateChart().scores_left(source)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")

    def test_part_1(self):
        self.assertEqual("2107929416", part_1(self.source))

    def test_part_2(self):
        self.assertEqual(20307394, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
