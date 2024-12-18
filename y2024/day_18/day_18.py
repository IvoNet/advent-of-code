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

import pyperclip

from ivonet.collection import Queue
from ivonet.decorators import debug
from ivonet.decorators import timer
from ivonet.files import read_rows
from ivonet.iter import ints

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def parse(source):
    """parsing coordinates from source and making sure the x,y is translated to row, column"""
    return [(r, c) for c, r in [ints(line) for line in source]]


class MemorySpace:
    def __init__(self, coordinates: list[tuple[int, int]], width=70, height=70, bytes=1024):
        self.side = width + 1
        self.coordinates = coordinates
        self.memory = [["." for _ in range(width + 1)] for _ in range(height + 1)]
        self.start: tuple[int, int] = (0, 0)
        self.end: tuple[int, int] = (height, width)
        self.bytes = bytes - 1

    def successors(self, loc: tuple[int, int]) -> list[tuple[int, int]]:
        ret = []
        r, c = loc
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            rr, cc = r + dr, c + dc
            if 0 <= rr < self.side and 0 <= cc < self.side and self.memory[rr][cc] != "#":
                ret.append((rr, cc))
        return ret

    def goal_test(self, loc) -> bool:
        return loc == self.end

    def bfs(self, bytes):
        """Breath first search
        """
        togo = bytes - 1
        for i, (r, c) in enumerate(self.coordinates):
            if 0 <= r < self.side and 0 <= c < self.side:
                self.memory[r][c] = "#"

            frontier = Queue()
            frontier.push((0, self.start))
            # explored is where we've been
            explored = {(0, self.start)}
            # keep going while there is more to explore
            ok = False
            while not frontier.empty:
                distance, current_state = frontier.pop()
                # if we found the goal, we're done
                if self.goal_test(current_state):
                    if i == togo:
                        return distance
                    ok = True
                    break
                # check where we can go next and haven't explored
                for child in self.successors(current_state):
                    if child in explored:  # skip children we already explored
                        continue
                    explored.add(child)
                    frontier.push((distance + 1, child))
            if not ok:
                return f'{r},{c}'


@debug
@timer
def part_1(source, w=70, h=70, bytes=1024) -> int | None:
    answer = 0
    coordinates = parse(source)
    ms = MemorySpace(coordinates, w, h, bytes)
    answer = ms.bfs(bytes)
    p(answer)
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
        self.assertEqual(22, part_1(self.test_source, 6, 6, 12))

    def test_part_1(self) -> None:
        self.assertEqual(292, part_1(self.source))

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
