#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import unittest
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints


def part_1(rows):
    x = 0
    y = 0
    for course in rows:
        direction, steps = course.strip().split(" ")
        steps = int(steps)
        if direction == "forward":
            y += steps
        elif direction == "up":
            x -= steps
        elif direction == "down":
            x += steps
    return x * y


def part_2(rows):
    x = 0
    y = 0
    aim = 0
    for course in rows:
        direction, steps = course.strip().split(" ")
        steps = int(steps)
        if direction == "forward":
            y += steps
            x += steps * aim
        elif direction == "up":
            aim -= steps
        elif direction == "down":
            aim += steps
    return x * y


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}.input")))
        self.test_source = read_rows("""forward 5
down 5
forward 8
up 3
down 8
forward 2""")

    def test_example_data_part_1(self):
        self.assertEqual(150, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(2019945, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(900, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(1599311480, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
