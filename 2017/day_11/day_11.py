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
from typing import TypeVar, Set, Optional, NamedTuple

from ivonet.collection import Queue
from ivonet.files import read_data
from ivonet.iter import ints
from ivonet.search import Node, node_to_path

sys.dont_write_bytecode = True

DEBUG = False
T = TypeVar('T')


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


DIRECTION = {
    "n": (1, 0),
    "ne": (0.5, 1),
    "se": (-0.5, 1),
    "s": (-1, 0),
    "sw": (-0.5, -1),
    "nw": (0.5, -1),
}


def get_neighbors(loc: Location, with_self=False):
    if with_self:
        yield loc
    yield Location(loc.row + DIRECTION["n"][0], loc.col + DIRECTION["n"][1])
    yield Location(loc.row + DIRECTION["ne"][0], loc.col + DIRECTION["ne"][1])
    yield Location(loc.row + DIRECTION["se"][0], loc.col + DIRECTION["se"][1])
    yield Location(loc.row + DIRECTION["s"][0], loc.col + DIRECTION["s"][1])
    yield Location(loc.row + DIRECTION["sw"][0], loc.col + DIRECTION["sw"][1])
    yield Location(loc.row + DIRECTION["nw"][0], loc.col + DIRECTION["nw"][1])


class Location(NamedTuple):
    row: float
    col: float


def bfs(initial: T, goal: T) -> Optional[Node[T]]:
    """Breath first search
    """
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(initial, None))
    explored: Set[T] = {initial}

    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        if current_state == goal:
            return current_node
        for child in get_neighbors(current_state):
            if child in explored:  # skip children we already explored
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None


def hexagon_distance(row, col):
    """Hexagon distance.
    - if the col is larger than the row and we always walk diagonally
      we do not need to take the row into account the distance is the col
    - if the col is smaller than the row the formulae is a bit more convoluted
      it is the col distance plus the number of steps up or down we need to do and
      those are measured in halves and we need to subtract the col times halve from
      that because we walk diagonally.
    """
    if abs(col) >= abs(row):
        return abs(col)
    else:
        return abs(col) + (abs(row) - abs(col) * 0.5)


def part_1(source):
    """bfs approach
    Works beautifully but is slow.
    """
    row = 0
    col = 0
    for d in source.strip().split(","):
        r, c = DIRECTION[d]
        row += r
        col += c
        _(row, col)

    solution = bfs(Location(0, 0), Location(row, col))
    path = node_to_path(solution)
    _(path)
    return len(path) - 1


def part_1_v2(source):
    row = 0
    col = 0
    for d in source.strip().split(","):
        r, c = DIRECTION[d]
        row += r
        col += c
        _(row, col, hexagon_distance(row, col))
    return hexagon_distance(row, col)


def part_2(source):
    row = 0
    col = 0
    ret = 0
    for d in source.strip().split(","):
        r, c = DIRECTION[d]
        row += r
        col += c
        _(row, col, hexagon_distance(row, col))
        ret = max(hexagon_distance(row, col), ret)
    return ret


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_data("""se,sw,se,sw,sw""")

    def test_example_data_part_1(self):
        self.assertEqual(3, part_1("se,sw,se,sw,sw"))
        self.assertEqual(2, part_1("ne,ne,s,s"))
        self.assertEqual(0, part_1("ne,ne,sw,sw"))
        self.assertEqual(3, part_1("ne,ne,ne"))

    def test_example_data_part_1_a(self):
        self.assertEqual(3, part_1_v2("se,sw,se,sw,sw"))
        self.assertEqual(2, part_1_v2("ne,ne,s,s"))
        self.assertEqual(0, part_1_v2("ne,ne,sw,sw"))
        self.assertEqual(3, part_1_v2("ne,ne,ne"))

    # @unittest.SkipTest
    def test_part_1(self):
        """This test proves the bfs approach and yes it works but it takes about 10 seconds
        just uncomment the skiptest to speed things up.
        """
        self.assertEqual(812, part_1(self.source))

    def test_part_1_v2(self):
        self.assertEqual(812, part_1_v2(self.source))

    def test_part_2(self):
        self.assertEqual(1603, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
