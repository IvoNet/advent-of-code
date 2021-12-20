#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import unittest
from itertools import permutations

from ivonet.files import read_rows
from ivonet.iter import consecutive_element_pairing

MINIMAL_PAIRING_LEN: int = 2


def part_1(data, preamble=25):
    data = list(map(int, data))
    end_idx = len(data) - preamble
    for idx in range(end_idx):
        under_test = data[idx + preamble]
        pre_lst = data[idx:idx + preamble]
        perms = list(permutations(pre_lst, 2))
        allowed_nums = [x + y for x, y in perms]
        if under_test not in allowed_nums:
            # print(f"Answer part 1 is [{under_test}] which was at index [{idx}]")
            return under_test
    return -1


def part_2(data, preamble=25):
    to_find = part_1(data, preamble)
    data_ints = list(map(int, data))
    for i in range(MINIMAL_PAIRING_LEN, len(data_ints)):
        sums = list(consecutive_element_pairing(data_ints, i, sum))
        if to_find in sums:
            find_idx = sums.index(to_find)
            lst = data_ints[find_idx: find_idx + i]
            print(i)
            print(lst)
            print(min(lst))
            print(max(lst))
            return min(lst) + max(lst)
    return -1


class UnitTests(unittest.TestCase):
    source = read_rows("day_9.input")
    test_source = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576""".split("\n")

    def test_example_data_part_1(self):
        self.assertEqual(127, part_1(self.test_source, 5))

    def test_sample_data_part_2(self):
        self.assertEqual(62, part_2(self.test_source, 5))

    def test_part_1(self):
        self.assertEqual(31161678, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(5453868, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
