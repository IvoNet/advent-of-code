#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import unittest
from itertools import permutations

from ivonet import get_data


def part_1(data, preamble=25):
    end_idx = len(data) - preamble
    for idx in range(end_idx):
        under_test = int(data[idx + preamble])
        pre_lst = list(map(int, data[idx:idx + preamble]))
        perms = list(permutations(pre_lst, 2))
        allowed_nums = [int(x + y) for x, y in perms]
        #
        # print(under_test)
        # print(pre_lst)
        # print(perms)
        # print(allowed_nums)

        if under_test not in allowed_nums:
            return under_test
    return -1


def part_2(data, preamble=25):
    pass


class UnitTests(unittest.TestCase):
    source = get_data("day-9.txt")

    def test_example_data(self):
        source = """35
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
        self.assertEqual(127, part_1(source, 5))
        self.assertEqual(None, part_2(source))

    def test_part_1(self):
        self.assertEqual(31161678, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(-1, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
