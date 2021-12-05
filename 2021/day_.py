#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import unittest

from ivonet import get_data


def part_1(data):
    pass


def part_2(data):
    pass


class UnitTests(unittest.TestCase):
    source = get_data("day_X.txt")

    def test_example_data(self):
        source = """"""
        self.assertEqual(None, part_1(source))
        self.assertEqual(None, part_2(source))

    def test_part_1(self):
        self.assertEqual(-1, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(-1, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
