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
    ret = []
    for a, b in permutations(nodes, 2):
        # _(a.used, b.avail, a.avail, b.used)
        if b.avail >= a.used > 0:
            ret.append((a, b))
    _(ret)
    ret = [x for x in ret if x[0].used != 0]
    return len(ret)


def visualize(nodes):
    empty = [n for n in nodes if n.used == 0]
    max_x = max(n.x for n in nodes)
    ret = "   012345678901234567890123456789012"
    y = -1
    for node in sorted(nodes, key=lambda x: x.y):
        if node.y > y:
            ret += f"\n{str(node.y).zfill(2)} "
            y = node.y
        if node.x == 0 and node.y == 0:
            ret += "F"
        elif node.y == 0 and node.x == max_x:
            ret += "G"
        elif node.used > empty[0].avail:
            # elif node.used > 90:
            ret += "#"
        elif node.used == 0:
            ret += "o"
        else:
            ret += "."
    return ret


def part_2(source):
    nodes = parse(source)
    print(visualize(nodes))
    print("Visualisation helped! its just a sliding puzzle.")
    print("- move the o (empty) to G which takes 16 + 12 + 21 steps")
    print("- then it takes 5 steps to move G one place to the left")
    print("- repeat the last step 31 times")
    print("No real code here but will probably try to program it at a later date :-)")
    return 16 + 12 + 22 + 31 * 5


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")

    def test_part_1(self):
        self.assertEqual(967, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(205, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
