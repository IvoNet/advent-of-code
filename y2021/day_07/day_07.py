#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import unittest
from pathlib import Path

import matplotlib.pyplot as plt
from numpy import mean

from ivonet.calc import step_sequence_calc
from ivonet.files import read_ints
from ivonet.iter import ints


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

    def setUp(self) -> None:
        print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_ints(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}.input")), delimiter=",")
        self.test_source = read_ints("""16,1,2,0,4,2,7,1,2,14""", delimiter=",")

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
