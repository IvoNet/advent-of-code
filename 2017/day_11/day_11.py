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

DEBUG = True
T = TypeVar('T')


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


DIR = {
    #    up,right
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
    yield Location(loc.row + DIR["n"][0], loc.col + DIR["n"][1])
    yield Location(loc.row + DIR["ne"][0], loc.col + DIR["ne"][1])
    yield Location(loc.row + DIR["se"][0], loc.col + DIR["se"][1])
    yield Location(loc.row + DIR["s"][0], loc.col + DIR["s"][1])
    yield Location(loc.row + DIR["sw"][0], loc.col + DIR["sw"][1])
    yield Location(loc.row + DIR["nw"][0], loc.col + DIR["nw"][1])


class Location(NamedTuple):
    row: float
    col: float


def bfs(initial: T, goal: T) -> Optional[Node[T]]:
    """Breath first search
    """
    # frontier is where we've yet to go
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(initial, None))
    # explored is where we've been
    explored: Set[T] = {initial}

    # keep going while there is more to explore
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # if we found the goal, we're done
        if current_state == goal:
            return current_node
        # check where we can go next and haven't explored
        for child in get_neighbors(current_state):
            if child in explored:  # skip children we already explored
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None  # went through everything and never found goal


def part_1(source):
    row = 0
    col = 0
    for d in source.strip().split(","):
        r, c = DIR[d]
        row += r
        col += c
        _(row, col)

    solution = bfs(Location(0, 0), Location(row, col))
    path = node_to_path(solution)
    _(path)
    return len(path) - 1


def part_2(source, furthest=True):
    return None


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

    def test_part_1(self):
        self.assertEqual(812, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
