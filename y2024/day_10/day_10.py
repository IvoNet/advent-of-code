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
from collections import abc, defaultdict
from pathlib import Path

import pyperclip

from ivonet.collection import Queue
from ivonet.decorators import debug
from ivonet.decorators import timer
from ivonet.files import read_rows
from ivonet.grid import Location
from ivonet.iter import ints
from ivonet.search import T, Node

collections.Callable = abc.Callable  # type: ignore
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
        self.distinct_paths = defaultdict(int)
        for r, line in enumerate(source):
            row = []
            for c, ch in enumerate(line):
                if ch == "0":  # Starting locations
                    self.starts.append(Location(r, c))
                if ch == "9":  # Goal locations
                    self.goals.append(Location(r, c))
                row.append(int(ch))
            self.grid.append(row)

    def is_goal(self, loc: Location) -> bool:
        """Check if the location is a goal"""
        return loc in self.goals

    def successors(self, loc: Location) -> list[Location]:
        """Return a list of locations that can be reached from the current location
        Note that only directions left, right, up and down are allowed and only if
        the next value is the current value + 1 and no more.
        """
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

    def bfs_part1(self, initial: T, ) -> int:
        """Breadth First Search for part 1

        Kinda standard BFS but with a twist.
        We need to count the number of possible paths to the goal
        """
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
            if self.is_goal(current_state):
                answer += 1
            # check where we can go next and haven't explored
            for child in self.successors(current_state):
                if child in explored:  # skip children we already explored
                    continue
                explored.add(child)
                frontier.push(Node(child, current_node))
        return answer

    def bfs_part2(self, initial: T) -> int:
        """Breadth First Search for part 2
        This adjusted version of a BFS is used to count the number of distinct paths to the goal
        """
        if self.grid[initial.row][initial.col] == 9:
            return 1
        if initial in self.distinct_paths:
            return self.distinct_paths[initial]
        answer = 0
        for child in self.successors(initial):
            answer += self.bfs_part2(child)
        self.distinct_paths[initial] = answer
        return answer

    def part_1(self):
        answer = 0
        for start in self.starts:
            solution = self.bfs_part1(start)
            if solution:
                answer += solution
        return answer

    def part_2(self):
        answer = 0
        for start in self.starts:
            solution = self.bfs_part2(start)
            if solution:
                answer += solution
        return answer


@debug
@timer
def part_1(source) -> int | None:
    trails = Trails(source)
    answer = trails.part_1()
    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:
    trails = Trails(source)
    answer = trails.part_2()
    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(36, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(582, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(81, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(1302, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
