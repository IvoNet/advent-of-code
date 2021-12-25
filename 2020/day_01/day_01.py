#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import unittest
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints


def part_1(data):
    data = list(map(int, data))
    for x in data:
        for y in data[1:]:
            if x + y == 2020:
                return x, y, x * y


def part_2(data):
    data = list(map(int, data))
    for x in data:
        for y in data[1:]:
            for z in data[2:]:
                if x + y + z == 2020:
                    return x, y, z, x * y * z


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"day_{day.zfill(2)}.input")
        self.test_source = read_rows("""""")

    def test_part_1(self):
        self.assertEqual(889779, part_1(self.source)[2])

    def test_part_2(self):
        self.assertEqual(76110336, part_2(self.source)[3])


if __name__ == '__main__':
    unittest.main()
