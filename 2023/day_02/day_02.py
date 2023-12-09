#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2022 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
If a part of the code is not part of the post it is probably 
code I found reusable and I may have moved it to my 'ivonet' library.
you can find that here: https://github.com/IvoNet/advent-of-code/tree/master/ivonet
"""

import os
import unittest
from collections import defaultdict
from pathlib import Path

import sys

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


# 12 red cubes, 13 green cubes, and 14 blue
GAME = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def parse_input_v1(source):
    games = {}
    for line in source:
        l = line.split(":")
        game_id = l[0].strip().split(" ")[1]
        sets = l[1].strip().split(";")
        sets = [x.strip().split(",") for x in sets]
        sets = [[x.strip().split(" ") for x in s] for s in sets]
        games[int(game_id)] = sets
    return games


def parse_input(source):
    """ see the parse_input_v1 function for the original code

    this dict comprehension does the same thing, but I doubt it is more readable
    """
    return {
        int(game_id): [[cube.strip().split(" ") for cube in s.strip().split(",")] for s in sets]
        for line in source
        for gid, rest in [line.split(":")]
        for _, game_id in [gid.strip().split(" ")]
        for sets in [rest.strip().split(";")]
    }


def part_1(source):
    answer = 0
    bad_ones = set()
    games = parse_input(source)
    for game_id, game in games.items():
        answer += game_id
        for round in game:
            for amount, color in round:
                if int(amount) > GAME[color]:
                    bad_ones.add(game_id)
                    break
    return answer - sum(bad_ones)


def part_2(source):
    ans = 0
    games = parse_input(source)
    for game_id, game in games.items():
        d = defaultdict(int)
        for round in game:
            for amount, color in round:
                d[color] = max(d[color], int(amount))
        ans += d['red'] * d['green'] * d['blue']
    return ans


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
""")
        self.test_source2 = read_rows("""""")

    def test_example_data_part_1(self):
        self.assertEqual(8, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(2239, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(2286, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(83435, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
