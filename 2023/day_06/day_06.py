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

import os
import sys
import unittest
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints, rangei

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def parse_data(source):
    """Two lines of input:
    Time with game durations
    and Distance with the longest distances recorded for each game.
    """
    times = ints(source[0])
    distances = ints(source[1])
    return times, distances


def calculate_ways_to_win(times, distances):
    """
    takes a list of race durations and a list of record distances as input.
    For each race, it calculates the maximum distance the boat can travel for
    each possible button hold duration and counts the number of ways we can
     beat the record.
     It then multiplies these counts together to get the final answer.
     """
    ways_to_win = 1
    for time, distance in zip(times, distances):
        max_distances = [(time - i) * i for i in rangei(time)]
        ways = sum(d > distance for d in max_distances)
        ways_to_win *= ways
    return ways_to_win


def calculate_ways_to_win_single_race(time, distance):
    """
    takes a single race duration and a single record distance as input.
    It calculates the maximum distance the boat can travel for each possible
    button hold duration and counts the number of ways you can beat the record.
    """
    max_distances = [(time - i) * i for i in rangei(time)]
    ways = sum(d > distance for d in max_distances)
    return ways


def part_1(source):
    times, distances = parse_data(source)
    return calculate_ways_to_win(times, distances)


def part_2(source):
    """"""
    times, distances = parse_data(source)
    time = int("".join(str(t) for t in times))
    distance = int("".join(str(d) for d in distances))
    return calculate_ways_to_win_single_race(time, distance)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""Time:      7  15   30
Distance:  9  40  200
""")
        self.test_source2 = read_rows("""""")

    def test_example_data_part_1(self):
        self.assertEqual(288, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(227850, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(71503, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(42948149, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
