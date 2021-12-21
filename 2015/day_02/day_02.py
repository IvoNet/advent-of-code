#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from pathlib import Path
from typing import NamedTuple

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Box(NamedTuple):
    l: int
    w: int
    h: int


def parse(source):
    boxes: list[Box] = []
    for box in source:
        boxes.append(Box(*ints(box)))
    return boxes


def wrapping(box: Box) -> int:
    total = 2 * box.l * box.w + 2 * box.w * box.h + 2 * box.h * box.l
    b = list(box)
    b.remove(max(b))
    total += b[0] * b[1]
    return total


def ribbon(box: Box) -> int:
    total = box.l * box.h * box.w
    b = list(box)
    b.remove(max(b))
    total += 2 * b[0] + 2 * b[1]
    return total


def part_1(source):
    boxes = parse(source)
    total = sum(wrapping(box) for box in boxes)
    _(total)
    return total


def part_2(source):
    boxes = parse(source)
    total = sum(ribbon(box) for box in boxes)
    _(total)
    return total


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"day_{day.zfill(2)}.input")
        self.test_source = read_rows("""2x3x4""")

    def test_example_data_part_1(self):
        self.assertEqual(58, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(1598415, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(34, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(3812909, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
