#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
##############################################################################
# Part 1
##############################################################################

##############################################################################
# Part 2
##############################################################################

"""

import unittest

from ivonet import get_data


def part_1(data):
    pass


def part_2(data):
    pass


class UnitTests(unittest.TestCase):
    source = get_data("day-4.txt")

    def test_example_data(self):
        source = """"""
        self.assertEqual(part_1(source), None)
        self.assertEqual(part_2(source), None)

    def test_part_1(self):
        self.assertEqual(part_1(self.source), 0)

    def test_part_2(self):
        self.assertEqual(part_2(self.source), 0)


if __name__ == '__main__':
    unittest.main()
