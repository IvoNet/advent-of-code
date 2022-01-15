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
from pathlib import Path
from typing import TypeVar, Callable

from ivonet.collection import Queue
from ivonet.files import read_rows
from ivonet.iter import ints
from ivonet.search import Node, node_to_path

sys.dont_write_bytecode = True
T = TypeVar('T')

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def parse(source):
    return [(a, b) if a < b else (b, a) for a, b in [ints(line) for line in source]]


def strength(bridge):
    return sum(x + y for x, y in bridge)


def bfs(magnets, successors):
    """Adjusted BFS
    - more than one init as there are more then one magnets with a 0 as start
    - the 'explored' had to be adjusted as we can reuse magnets as long as they
      are not part of the bridge
    - The goal test removed
    - testing for longest and strongest bridge added
    """
    strongest = float("-inf")
    longest = float("-inf")
    longest_bridge = []
    for initial in [magnet for magnet in magnets if 0 in magnet]:
        frontier: Queue[Node[T]] = Queue()
        frontier.push(Node(initial, None))

        while not frontier.empty:
            current_node: Node[T] = frontier.pop()
            current_state: T = current_node.state
            bridge = node_to_path(current_node)
            strongest = max(strength(bridge), strongest)
            length = len(bridge)
            if length > longest:
                longest_bridge = bridge
                longest = length
            for child in successors(current_state):
                if child in bridge or child[::-1] in bridge:
                    continue
                frontier.push(Node(child, current_node))
    return strongest, strength(longest_bridge)


def can_connect(magnets) -> Callable[[list[tuple[int, int]]], list[T]]:
    def connectors(a: T) -> list[T]:
        ret = set()
        ret = ret.union((x, y) for x, y in magnets if x == a[1])
        ret = ret.union((y, x) for x, y in magnets if y == a[1])
        return list(ret)

    return connectors


def part_1_2(source):
    magnets = parse(source)
    neigbors = can_connect(magnets)
    strongest, longest = bfs(magnets, neigbors)
    return strongest, longest


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10""")

    def test_example_data_part_1(self):
        self.assertEqual(31, part_1_2(self.test_source)[0])

    def test_part_1_2(self):
        strongest, longest = part_1_2(self.source)
        self.assertEqual(1868, strongest)
        self.assertEqual(1841, longest)


if __name__ == '__main__':
    unittest.main()
