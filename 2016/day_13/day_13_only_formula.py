#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
After solving it the first way I was thinking about it and came to the conclusion that 
creating a real maze was totally unnessesary as we already have a formula for knowing if 
we have an open space or not.
I also already had a function for finding neigbors and doing a bfs search.
So combining the successors function with the is_empty test and voila a virtual grid.

I still like my first solution a lot more as it can actually print a representation of its state
and the path, so I will keep both.

The first solution is also more generic except for the fact that I could not incorporate the second type of goal test
(testing for length) without changing the signature of the bfs function.
"""

import os
import sys
import unittest
from pathlib import Path
from queue import Queue
from typing import Optional, Set, NamedTuple, TypeVar

from ivonet.collection import Queue
from ivonet.files import read_data
from ivonet.grid import neighbors_defined_grid, Location
from ivonet.iter import ints
from ivonet.search import node_to_path, Node

sys.dont_write_bytecode = True

DEBUG = False

T = TypeVar("T")


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Point(NamedTuple):
    x: int
    y: int


def is_empty(x, y, favorite_nr) -> bool:
    """The provided empty test function"""
    return bin(x * x + 3 * x + 2 * x * y + y + y * y + favorite_nr).count("1") % 2 == 0


def successors(loc: Point, favorite_number):
    """Generates all locations that can be reached from the current location."""
    return [Point(coord.col, coord.row) for coord in
            neighbors_defined_grid(Location(loc.y, loc.x), (loc.y + 2, loc.x + 2), diagonal=False)
            if is_empty(coord.col, coord.row, favorite_number)]


def bfs(initial: T, goal: Point | int, favorite_nr: int, part_1=True) -> Optional[Node[T]] | int:
    """Standard bfs function but with a few small adjustments
    especially in the testing of the goal.
    """
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(initial, None))
    explored: Set[T] = {initial}

    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        if part_1 and goal == current_state:
            return current_node
        if not part_1 and len(node_to_path(current_node)) > goal:
            return len(explored)
        for child in successors(current_state, favorite_number=favorite_nr):
            if child in explored:
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None


def part_1(source, goal: Point = Point(31, 39)):
    return len(node_to_path(bfs(Point(1, 1), goal, int(source), part_1=True))) - 1


def part_2(source):
    return bfs(Point(1, 1), 50, int(source), part_1=False)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_data("""10""")

    def test_example_data_part_1(self):
        self.assertEqual(11, part_1(self.test_source, Point(7, 4)))

    def test_part_1(self):
        self.assertEqual(82, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(138, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
