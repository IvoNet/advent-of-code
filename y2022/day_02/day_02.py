#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2022 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
If a part of the code is not part of the gist it is probably 
code I found reusable and I may have moved it to my 'ivonet' library.
you can find that here: https://github.com/IvoNet/advent-of-code/tree/master/ivonet
"""

import os
import sys
import unittest
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


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

circle = [ROCK, PAPER, SCISSORS]


def counter_move(opponent, you) -> int:
    """Calculate the counter move for the opponent"""
    return circle[(circle.index(shape[opponent]) + [-1 if you == "X" else 1 if you == "Z" else 0][0]) % 3]


def part_1(source):
    return sum([sum((state[rules_from_your_pov[(shape[a], shape[b])]], shape[b])) for a, b in source])


def part_2(source):
    score = 0
    for opponent, you in source:
        move = counter_move(opponent, you)
        score += state[rules_from_your_pov[shape[opponent], move]] + move
    return score


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = [x.split(" ") for x in read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")]
        self.test_source = [x.split(" ") for x in read_rows("""A Y
B X
C Z""")]

    def test_example_data_part_1(self):
        self.assertEqual(15, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(14069, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(12, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(12411, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
