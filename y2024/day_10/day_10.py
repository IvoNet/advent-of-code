#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2023 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
If a part of the code is not part of the post it is probably 
code I found reusable and I may have moved it to my 'ivonet' library.
you can find that here: https://github.com/IvoNet/advent-of-code/tree/master/ivonet
"""

import collections
import os
import sys
import unittest
from pathlib import Path
from typing import Callable, Optional

import pyperclip

from ivonet.collection import Queue
from ivonet.decorators import debug
from ivonet.decorators import timer
from ivonet.files import read_rows
from ivonet.grid import Location
from ivonet.iter import ints
from ivonet.search import bfs, T, Node

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


class Trails:

    def __init__(self, source: list[str]):
        self.source: list[str] = source
        self.grid: list[list[int]] = []
        self.height: int = len(source)
        self.width: int = len(source[0])
        self.starts: list[Location] = []
        self.goals: list[Location] = []
        for r, line in enumerate(source):
            row = []
            for c, ch in enumerate(line):
                if ch == "0":
                    self.starts.append(Location(r, c))
                if ch == "9":
                    self.goals.append(Location(r, c))
                row.append(int(ch))
            self.grid.append(row)

    def is_goal(self, loc: Location) -> bool:
        return loc in self.goals

    def successors(self, loc: Location) -> list[Location]:
        next_value = self.grid[loc.row][loc.col] + 1
        if next_value > 9:
            return []
        ret: list[Location] = []
        left = Location(loc.row, loc.col - 1)
        if left.col >= 0 and self.grid[left.row][left.col] == next_value:
            ret.append(left)
        right = Location(loc.row, loc.col + 1)
        if right.col < self.width and self.grid[right.row][right.col] == next_value:
            ret.append(right)
        up = Location(loc.row - 1, loc.col)
        if up.row >= 0 and self.grid[up.row][up.col] == next_value:
            ret.append(up)
        down = Location(loc.row + 1, loc.col)
        if down.row < self.height and self.grid[down.row][down.col] == next_value:
            ret.append(down)
        return ret


def bfs(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], list[T]]) -> Optional[Node[T]]:
    # frontier is where we've yet to go
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(initial, None))
    # explored is where we've been
    explored: set[T] = {initial}
    answer = 0
    # keep going while there is more to explore
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # if we found the goal, we're done
        if goal_test(current_state):
            answer += 1
        # check where we can go next and haven't explored
        for child in successors(current_state):
            if child in explored:  # skip children we already explored
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return answer


@debug
@timer
def part_1(source) -> int | None:
    answer = 0
    trails = Trails(source)
    for start in trails.starts:
        solution = bfs(start, trails.is_goal, trails.successors)
        if solution:
            answer += solution

    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:
    answer = 0
    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(36, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(582, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(None, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
