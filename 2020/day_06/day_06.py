#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import unittest
from pathlib import Path

from ivonet.files import read_data
from ivonet.iter import ints


class Group(object):

    def __init__(self, data: str) -> None:
        self.data = data
        self.group_answers = data.strip().split("\n")
        self.member_count = len(self.group_answers)
        self.combined_answers = set(list("".join(self.group_answers)))
        self.count = len(self.combined_answers)
        self.intersection = set(self.group_answers[0]).intersection(*self.group_answers)
        self.intersection_count = len(self.intersection)


def part_1_2(data):
    groups = data.split("\n\n")
    converted_groups = list(map(Group, groups))
    count = sum(i.count for i in converted_groups)
    intersection_count = sum(i.intersection_count for i in converted_groups)
    return count, intersection_count


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"day_{day.zfill(2)}.input")

    def test_part_1(self):
        self.assertEqual(6585, part_1_2(self.source)[0])

    def test_part_2(self):
        self.assertEqual(3276, part_1_2(self.source)[1])


if __name__ == '__main__':
    unittest.main()
