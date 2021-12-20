#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import unittest
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints


def filter_binaries_on_idx_value(data, idx, value):
    ret = []
    for x in data:
        if x[idx] == value:
            ret.append(x)
    return ret


def binair_counter(data, idx):
    """creates a binary str from the idx of the data list and then counts the 1 and 0"""
    new_bin = "".join([x[idx] for x in data])
    c0 = new_bin.count("0")
    c1 = new_bin.count("1")
    return c0, c1


def oxygen(data, idx):
    """Recursive function to calculate the one binary based on the oxygen rule"""
    if len(data) == 1:
        return data

    c0, c1 = binair_counter(data, idx)
    if c0 > c1:
        new_data = filter_binaries_on_idx_value(data, idx, "0")
    else:
        new_data = filter_binaries_on_idx_value(data, idx, "1")

    return oxygen(new_data, idx + 1)


def co_two(data, idx):
    """Recursive function to calculate the one binary based on the co2 rule"""
    if len(data) == 1:
        return data

    c0, c1 = binair_counter(data, idx)
    if c0 <= c1:
        new_data = filter_binaries_on_idx_value(data, idx, "0")
    else:
        new_data = filter_binaries_on_idx_value(data, idx, "1")

    return co_two(new_data, idx + 1)


def part_1(data):
    gamma = ""
    epsilon = ""
    for idx in range(len(data[0])):
        c0, c1 = binair_counter(data, idx)
        if c0 > c1:
            gamma += "1"
            epsilon += "0"
        else:
            gamma += "0"
            epsilon += "1"
    gamma = int(gamma, 2)
    epsilon = int(epsilon, 2)
    return gamma * epsilon


def part_2(data):
    ox = int(oxygen(data, 0)[0], 2)
    co = int(co_two(data, 0)[0], 2)
    return ox * co


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"day_{day.zfill(2)}.input")
        self.test_source = read_rows("""00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010""")

    def test_example_data_part_1(self):
        self.assertEqual(198, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(4103154, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(230, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(4245351, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
