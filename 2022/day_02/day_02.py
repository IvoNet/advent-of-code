#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """"""

import os
import unittest
from pathlib import Path

import sys

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


ROCK = 1
PAPER = 2
SCISSORS = 3

shape = {
    "A": ROCK,
    "B": PAPER,
    "C": SCISSORS,
    "X": ROCK,
    "Y": PAPER,
    "Z": SCISSORS,
}

rules_from_your_pov = {
    (ROCK, ROCK): "draw",
    (ROCK, PAPER): "win",
    (ROCK, SCISSORS): "loss",
    (PAPER, PAPER): "draw",
    (PAPER, ROCK): "loss",
    (PAPER, SCISSORS): "win",
    (SCISSORS, SCISSORS): "draw",
    (SCISSORS, ROCK): "win",
    (SCISSORS, PAPER): "loss",
}

state = {
    "win": 6,
    "draw": 3,
    "loss": 0,
}


def rock_paper_scissors(source):
    return sum(
        [sum((state[rules_from_your_pov[(shape[a], shape[b])]], shape[b])) for a, b in [x.split(" ") for x in source]])


def part_1(source):
    return rock_paper_scissors(source)


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""A Y
B X
C Z""")

    def test_example_data_part_1(self):
        self.assertEqual(15, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(8933, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
