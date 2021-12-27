#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import json
import sys
import unittest
from pathlib import Path

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def remove_red(source):
    """First try of part 2.... went wrong!"""
    try:
        idx = source.index("red")
    except ValueError:
        return source
    start = -1
    pos = -1
    for i in range(idx, -1, -1):
        if source[i] == "[":
            break
        if source[i] == "{":
            start = 1
            pos = i
            break
    if start >= 0:
        if pos >= 0:
            for i in range(idx, len(source)):
                if source[i] == "{":
                    start += 1
                elif source[i] == "}":
                    start -= 1
                if start == 0:
                    new = source[:pos] + source[i + 1:]
                    return remove_red(new)
    elif idx >= 0:
        return remove_red(source.replace("red", "!!!", 1))
    _(source)
    return source


def exclude_red_sum(source):
    if isinstance(source, int):
        return source
    elif isinstance(source, str):
        return 0
    elif isinstance(source, list):
        return sum(exclude_red_sum(x) for x in source)
    else:  # dict
        if any(x == "red" for x in source.values()):
            return 0
        else:
            return sum(exclude_red_sum(x) for x in source.values())


def part_1(source):
    """Don't treat it as a Python or JSON object but just do regex on all integers and sum them"""
    return sum(ints(source))


def part_2(source):
    data = json.loads(source)
    return exclude_red_sum(data)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"day_{day.zfill(2)}.input")
        self.test_source = read_data("""[1,2,3]""")

    def test_example_data_part_1(self):
        self.assertEqual(6, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(111754, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(4, part_2('[1,{"c":"red","b":2},3]'))
        self.assertEqual(0, part_2('{"d":"red","e":[1,2,3,4],"f":5}'))
        self.assertEqual(6, part_2('[1,"red",5]'))

    def test_part_2(self):
        self.assertEqual(65402, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
