#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import unittest

from ivonet import read_data


def fuel_calc(steps):
    fuel = 0
    for i in range(1, steps + 1):
        fuel += i
    return fuel


def part_1(data):
    minimal_fuel = 100000000000000000000000000
    for allign in data:
        fuel = 0
        for x in data:
            fuel += abs(x - allign)
        if minimal_fuel > fuel:
            minimal_fuel = fuel
    return minimal_fuel


def part_2(data):
    minimal_fuel = 100000000000000000000000000000000000000
    for allign in range(len(data)):
        fuel = 0
        for x in data:
            fuel += fuel_calc(abs(x - allign))
        if minimal_fuel > fuel:
            minimal_fuel = fuel
    return minimal_fuel


class UnitTests(unittest.TestCase):
    source = list(map(int, read_data("day_7.txt").split(",")))
    test_source = list(map(int, "16,1,2,0,4,2,7,1,2,14".split(",")))

    def test_example_data_part_1(self):
        self.assertEqual(37, part_1(self.test_source))

    def test_example_data_part_2(self):
        self.assertEqual(168, part_2(self.test_source))

    def test_part_1(self):
        self.assertEqual(343441, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(98925151, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
