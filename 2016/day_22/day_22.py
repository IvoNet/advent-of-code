#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """"""

import os
import sys
import unittest
from itertools import permutations
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


class Node(NamedTuple):
    x: int
    y: int
    size: int
    used: int
    avail: int
    use: int


def parse(source) -> list[Node]:
    return [Node(*ints(line)) for line in source[2:]]


def part_1(source):
    nodes = parse(source)
    # _(nodes)
    candidates = [n for n in nodes if n.used != 0]
    # _(sorted(nodes, key=lambda x: x.avail, reverse=True))
    # _(sorted(nodes, key=lambda x: x.used))
    # _(candidates)
    ret = []
    for a, b in permutations(nodes, 2):
        # _(a.used, b.avail, a.avail, b.used)
        if b.avail >= a.used > 0:
            ret.append((a, b))
    _(ret)
    ret = [x for x in ret if x[0].used != 0]
    return len(ret)


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""""")


    def test_part_1(self):
        self.assertEqual(967, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
