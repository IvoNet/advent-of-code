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
from pathlib import Path

import sys

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


class Factory:
    def __init__(self, source):
        self.source = source
        self.blueprints: list[list[int]] = [ints(line) for line in source]
        self.max = 0
        self.max_ore = 0
        self.clay_cost = 0
        self.max_obsidian = 0
        pass

    def dfs(self, time_left, goal,
            ore_robot, clay_robot, obsidian_robot, geode_robot,
            ore_available, clay_available, obsidian_available, geode_available):
        if (goal == 0 and ore_robot >= mi or
                goal == 1 and clay_robot >= mj or
                goal == 2 and (obsidian_robot >= mk or clay_robot == 0) or
                goal == 3 and obsidian_robot == 0 or
                geode_available + geode_robot * time_left + o[time_left] <= m):
            return
        while time_left:
            if goal == 0 and ore_available >= a:
                self.dfs(time_left - 1, goal, ore_robot + 1, clay_robot, obsidian_robot, geode_robot,
                         ore_available - a + ore_robot, clay_available + clay_robot,
                         obsidian_available + obsidian_robot, geode_available + geode_robot)
                return
            elif goal == 1 and ore_available >= b:
                self.dfs(time_left - 1, goal, ore_robot, clay_robot + 1, obsidian_robot, geode_robot,
                         ore_available - b + ore_robot, clay_available + clay_robot,
                         obsidian_available + obsidian_robot, geode_available + geode_robot)
                return
            elif goal == 2 and ore_available >= c and clay_available >= d:
                self.dfs(time_left - 1, goal, ore_robot, clay_robot, obsidian_robot + 1, geode_robot,
                         ore_available - c + ore_robot, clay_available - d + clay_robot,
                         obsidian_available + obsidian_robot, geode_available + geode_robot)
                return
            elif goal == 3 and ore_available >= e and obsidian_available >= f:
                self.dfs(time_left - 1, goal, ore_robot, clay_robot, obsidian_robot, geode_robot + 1,
                         ore_available - e + ore_robot, clay_available + clay_robot,
                         obsidian_available - f + obsidian_robot, geode_available + geode_robot)
                return
            time_left, ore_available, clay_available, obsidian_available, geode_available = time_left - 1, ore_available + ore_robot, clay_available + clay_robot, obsidian_available + obsidian_robot, geode_available + geode_robot
        self.max = max(self.max, geode_available)

    def run(self):
        for


def part_1(source):
    factory = Factory(source)
    return None


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""""")

    def test_example_data_part_1(self):
        self.assertEqual(33, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(1834, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(56 * 62, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(2240, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
