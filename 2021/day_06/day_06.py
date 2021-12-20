#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import unittest
from collections import defaultdict

from ivonet.files import read_data


def growth_calculator(fishes: list[int], days: int = 80):
    bucket = defaultdict(int)
    bucket[1] = fishes.count(1)
    bucket[2] = fishes.count(2)
    bucket[3] = fishes.count(3)
    bucket[4] = fishes.count(4)
    bucket[5] = fishes.count(5)
    bucket[6] = fishes.count(6)
    for _ in range(1, days + 1):
        temp = defaultdict(int)
        temp[0] = bucket[1]
        temp[1] = bucket[2]
        temp[2] = bucket[3]
        temp[3] = bucket[4]
        temp[4] = bucket[5]
        temp[5] = bucket[6]
        temp[6] = bucket[7] + bucket[0]
        temp[7] = bucket[8]
        temp[8] = bucket[0]
        bucket = temp
    return sum(bucket.values())


def part_1(data, days=80):
    return growth_calculator(data, days)


def part_2(data, days=256):
    return growth_calculator(data, days)


class UnitTests(unittest.TestCase):
    source = list(map(int, read_data("day_06.input").split(",")))
    test_source = [3, 4, 3, 1, 2]

    def test_example_data_part_1(self):
        self.assertEqual(5934, part_1(self.test_source, 80))

    def test_example_data_part_2(self):
        self.assertEqual(26984457539, part_2(self.test_source))

    def test_part_1(self):
        self.assertEqual(356190, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(1617359101538, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
