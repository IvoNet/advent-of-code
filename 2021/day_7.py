#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import unittest

import matplotlib.pyplot as plt
from numpy import mean

from ivonet import read_data
from ivonet import step_sequence_calc


def part_1(data):
    """
    >>> part_1([16,1,2,0,4,2,7,1,2,14])
    37
    """
    minimal_fuel = 0
    for align in data:
        fuel = sum(abs(x - align) for x in data)
        if not minimal_fuel or minimal_fuel > fuel:
            minimal_fuel = fuel
    return minimal_fuel


def part_2(data):
    """
    >>> part_2([16,1,2,0,4,2,7,1,2,14])
    168
    """
    minimal_fuel = 0
    avg = int(mean(data))
    for align in range(avg - 2, avg + 2):  # faster but not by much anymore
        # for align in range(len(data)):
        fuel = sum(step_sequence_calc(abs(x - align)) for x in data)
        if not minimal_fuel or minimal_fuel > fuel:
            minimal_fuel = fuel
    return int(minimal_fuel)


def plot(data):
    plt.plot(data)
    plt.ylabel("crabs")
    plt.show()


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
    # plot(list(map(int, read_data("day_7.txt").split(","))))
    unittest.main()
