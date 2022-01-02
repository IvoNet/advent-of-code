#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import unittest
from pathlib import Path
from typing import List

from ivonet.files import read_ints, read_data
from ivonet.iter import consecutive_element_pairing, ints


def sum_tripplewise(data: List[int]) -> List[int]:
    """group by next three per item in list"""
    if len(data) < 3:
        return []
    return [sum(data[i:i + 3]) for i in range(len(data) - 2)]


# Second successfully attempt
def sum_consecutive_triple_element_pairing(data: List[int]) -> List[int]:
    if len(data) < 3:
        return []
    return list(map(sum, zip(data, data[1:], data[2:])))


def increase_counter(values: list[int]) -> int:
    """Counts how many measurements are larger than the previous measurement"""
    if not values:
        return 0
    level = values[0]
    count = 0
    for item in values[1:]:
        if item > level:
            count += 1
        level = item
    return count


def part_1(source):
    return increase_counter(source)


def part_2(source):
    return increase_counter(consecutive_element_pairing(source, 3, sum))


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}.input")))
        self.test_source = read_ints("""199
200
208
210
200
207
240
269
260
263""", delimiter="\n")

    def test_example_data_part_1(self):
        self.assertEqual(7, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(1226, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(5, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(1252, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
