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
import sys
import unittest
from pathlib import Path

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def part_1(source, unique_size=4):
    for i in range(0, len(source) - unique_size):
        if len(set(source[i:i + unique_size])) < unique_size:
            continue
        return i + unique_size
    raise ValueError("No solution found")


def part_2(source):
    return part_1(source, 14)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_data("""mjqjpqmgbljsphdztnvjfqwrcgsmlb""")  # 7
        self.test_source2 = read_data("""bvwbjplbgvbhsrlpgdmjqwftvncz""")  # 5
        self.test_source3 = read_data("""nppdvjthqldpwncqszvftbrmjlhg""")  # 6
        self.test_source4 = read_data("""nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg""")  # 10
        self.test_source5 = read_data("""zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw""")  # 11
        self.test_source6 = read_data("""mjqjpqmgbljsphdztnvjfqwrcgsmlb""")  # 19
        self.test_source7 = read_data("""bvwbjplbgvbhsrlpgdmjqwftvncz""")  # 23
        self.test_source8 = read_data("""nppdvjthqldpwncqszvftbrmjlhg""")  # 23
        self.test_source9 = read_data("""nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg""")  # 29
        self.test_source10 = read_data("""zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw""")  # 26

    def test_example_data_part_1(self):
        self.assertEqual(7, part_1(self.test_source))
        self.assertEqual(5, part_1(self.test_source2))
        self.assertEqual(6, part_1(self.test_source3))
        self.assertEqual(10, part_1(self.test_source4))
        self.assertEqual(11, part_1(self.test_source5))

    def test_part_1(self):
        self.assertEqual(1848, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(19, part_2(self.test_source6))
        self.assertEqual(23, part_2(self.test_source7))
        self.assertEqual(23, part_2(self.test_source8))
        self.assertEqual(29, part_2(self.test_source9))
        self.assertEqual(26, part_2(self.test_source10))

    def test_part_2(self):
        self.assertEqual(2308, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
