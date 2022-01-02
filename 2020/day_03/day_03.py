#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import unittest
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints


def part_1(data, right=3, down=1):
    trees = 0
    for i in range(1, len(data)):
        x = i * right
        y = i * down
        if y > len(data):
            break
        while x >= len(data[y]):
            data[y] += data[y]
        if data[y][x] == "#":
            trees += 1
    return trees


def part_2(data):
    a = part_1(data, right=1, down=1)
    b = part_1(data, right=3, down=1)
    c = part_1(data, right=5, down=1)
    d = part_1(data, right=7, down=1)
    e = part_1(data, right=1, down=2)
    # _(a, b, c, d, e)
    return a * b * c * d * e


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}.input")))

    def test_part_1(self):
        self.assertEqual(289, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(5522401584, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
