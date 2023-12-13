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
from functools import cache
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def parse(source):
    """
    parse the source:
    - every line contains pattern and a groups list of numbers
    - the two are separated by a space
    """
    for line in source:
        springs, parity = line.split(" ")
        yield springs, tuple(ints(parity))


class HotSprings(object):
    def __init__(self, source, fold=1):
        self.source = source
        self.cache = {}
        self.fold = fold

    @cache
    def count_valid_combinations(self, pattern, groups, damage_count=0):
        """
        Recursively counts the number of valid arrangements of operational and broken springs
        that meet the given criteria in each row.

        Parameters:
        pattern (str): A string representing the current state of the springs in a row.
        groups (tuple): A tuple of integers representing the size of each contiguous group of damaged springs.
        damage_count (int, optional): An integer representing the current damage_count of contiguous damaged springs. Defaults to 0.

        Returns:
        int: The number of valid arrangements of springs.

        :param pattern: is a string representing the current state of the springs in a
                        row, where each spring can be operational ('.'), damaged ('#'),
                        or unknown ('?').
        :param groups: is a tuple of integers representing the size of each contiguous group of damaged springs
                       in the order they appear in the row.
        :param damage_count: is an integer representing the current damage_count of contiguous damaged springs.
                      It is optional and defaults to 0.
        :return:
        """
        # All pattern accounted for
        if not pattern and damage_count > 0:  # Last spring was damaged
            if len(groups) == 1 and damage_count == groups[0]:
                return 1
            else:
                return 0
        if not pattern and not damage_count:  # Last spring was operational
            if not len(groups):
                return 1
            else:
                return 0

        # We saw more damaged pattern in a row than there
        # should be according to the groups, so it is not valid
        if damage_count > 0 and (not groups or damage_count > groups[0]):
            return 0

        # So far everything's good, but we have more pattern to see
        first, rest = pattern[0], pattern[1:]
        match first:
            case '.':
                if damage_count > 0:  # We finished a run of damaged pattern
                    if damage_count != groups[0]:
                        return 0
                    else:  # Last spring was also operational
                        groups = groups[1:]
                return self.count_valid_combinations(rest, groups, 0)
            case '#':
                # Increase damage damage_count
                return self.count_valid_combinations(rest, groups, damage_count + 1)
            case '?':
                if not groups or damage_count == groups[0]:  # We finished a run of damaged pattern
                    return self.count_valid_combinations(rest, groups[1:], 0)

                if damage_count > 0:
                    # We are in the middle of a run of damaged pattern
                    return self.count_valid_combinations(rest, groups, damage_count + 1)
                else:
                    # This unknown could be a . or # so let's damage_count both options
                    return (self.count_valid_combinations(rest, groups, damage_count + 1) +
                            self.count_valid_combinations(rest, groups, damage_count))

    def run(self):
        answer = 0
        for patterns, groups in parse(self.source):
            s = "?".join([patterns] * self.fold)
            g = groups * self.fold
            answer += self.count_valid_combinations(s, g)
        return answer


def part_1(source):
    return HotSprings(source).run()


def part_2(source, times=5):
    return HotSprings(source, times).run()


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""")
        self.test_source2 = read_rows("""#.#.### 1,1,3
.#...#....###. 1,1,3
.#.###.#.###### 1,3,1,6
####.#...#... 4,1,1
#....######..#####. 1,6,5
.###.##....# 3,2,1""")

    def test_example_data_part_1(self):
        self.assertEqual(21, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(7173, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(525152, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(29826669191291, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
