#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import os
import unittest
from collections import defaultdict
from pathlib import Path

import numpy as np

from ivonet.files import read_rows
from ivonet.iter import ints

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def part_1(data):
    adapters = [0] + sorted(map(int, data))  # outlet plus list
    adapters.append(adapters[-1] + 3)  # add phone as adapter
    dif = np.diff(adapters)
    unique, counts = np.unique(dif, return_counts=True)
    value = dict(zip(unique, counts))
    return value[1] * value[3]


def part_2(data):
    """Find the sum of all the possibilities per adapter in the sorted list

    in the longer example when you get to adapter '7'
    this is the state of the cache at 4:
    {0: 1, -1: 0, -2: 0, 1: 1, 2: 2, 3: 4, 4: 7})

    Adapter 7 is the first with joltage of 3 compared to former (4)
    so now if we som the cache of the adapter -1 that would be 6 and as it
    has no entry in the cache it will return 0. Same for -2 (5), but not for -3 (4)
    that will give a sum of 0 + 0 + 7 = 7 leaving state:

    {0: 1, -1: 0, -2: 0, 1: 1, 2: 2, 3: 4, 4: 7, 6: 0, 5: 0, 7: 7})

    next is adapter 8
    - adapter 8 - 1 = 7 which has value: 7
    - adapter 8 - 2 = 6 which has value: 0
    - adapter 8 - 3 = 5 which has value: 0
    {0: 1, -1: 0, -2: 0, 1: 1, 2: 2, 3: 4, 4: 7, 6: 0, 5: 0, 7: 7, 8: 7})
    next adapter 9
    - adapter 9 - 1 = 8 which has value: 7
    - adapter 9 - 2 = 7 which has value: 7
    - adapter 9 - 3 = 6 which has value: 0
    {0: 1, -1: 0, -2: 0, 1: 1, 2: 2, 3: 4, 4: 7, 6: 0, 5: 0, 7: 7, 8: 7, 9: 14})
    etc...

    In the end you get the solution of the number of possible combinations in the highest adapter
    in the cache.
    """
    adapters = sorted(map(int, data))
    _(adapters)
    highest_adapter = adapters[-1]
    cache = defaultdict(int)
    cache[0] = 1
    for adapter in adapters:
        cache[adapter] = cache[adapter - 1] + cache[adapter - 2] + cache[adapter - 3]
        _(adapter, cache)
    return cache[highest_adapter]


class UnitTests(unittest.TestCase):
    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3""")

    def test_example_data_part_1(self):
        self.assertEqual(220, part_1(self.test_source))

    def test_example_data_part_2(self):
        self.assertEqual(19208, part_2(self.test_source))

    def test_part_1(self):
        self.assertEqual(2775, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(518344341716992, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
