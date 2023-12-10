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

import os
import unittest
from collections import deque
from pathlib import Path

import sys

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


class PipeMaze:
    NEIGHBORS = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    ALLOWED_NEIGHBORS: dict[tuple[int, int], list[str]] = {
        (0, -1): {'|', 'F', '7'},  # up
        (0, 1): {'|', 'L', 'J'},  # down
        (-1, 0): {'-', 'F', 'L'},  # left
        (1, 0): {'-', 'J', '7'}  # right
    }

    MAPPING = {
        (0, -1): {'|', 'L', 'J'},  # when going up, you can continue on these tiles
        (0, 1): {'|', 'F', '7'},  # when going down, you can continue on these tiles
        (-1, 0): {'-', 'J', '7'},  # when going left, you can continue on these tiles
        (1, 0): {'-', 'F', 'L'}  # when going right, you can continue on these tiles
    }

    def __init__(self, source):
        self.source = source
        self.visited = set()
        self.board = {}
        self.start = None
        self.__create_board(source)
        self.possible_s = {"|", "-", "J", "L", "7", "F"}
        self.bfs()
        self.start_char = list(self.possible_s)[0] if len(self.possible_s) == 1 else None
        if self.start_char is None:
            raise RuntimeError("No start character found")

    def __create_board(self, source):
        for row, line in enumerate(source):
            for col, c in enumerate(line):
                self.board[(col, row)] = c
                if c == 'S':
                    self.start = (col, row)

    def bfs(self):
        queue = deque([self.start])
        self.visited = {self.start}
        while queue:
            position = queue.popleft()
            if position == self.start:
                for n in self.NEIGHBORS:
                    neighbor_pos = (position[0] + n[0], position[1] + n[1])
                    if neighbor_pos not in self.board:
                        continue
                    if self.board[neighbor_pos] in self.ALLOWED_NEIGHBORS[n]:
                        queue.append(neighbor_pos)
                        self.possible_s &= self.MAPPING[n]  # only one possible start character should be left after bfs
            if position in self.visited:
                continue
            for n in self.NEIGHBORS:
                neighbor_pos = (position[0] + n[0], position[1] + n[1])
                if neighbor_pos not in self.board:
                    continue
                self.visited.add(position)
                if self.board[position] in self.MAPPING[n] and self.board[neighbor_pos] in self.ALLOWED_NEIGHBORS[n]:
                    queue.append(neighbor_pos)

    def bfs2(self):
        queue = deque([self.start])
        self.visited = {self.start}
        while queue:
            position = queue.popleft()
            if position == self.start:
                for n in self.NEIGHBORS:
                    neighbor_pos = (position[0] + n[0], position[1] + n[1])
                    if neighbor_pos not in self.board:
                        continue
                    if self.board[neighbor_pos] in self.ALLOWED_NEIGHBORS[n]:
                        queue.append(neighbor_pos)
                        self.possible_s &= self.MAPPING[n]  # only one possible start character should be left after bfs
            if position in self.visited:
                continue
            for n in self.NEIGHBORS:
                neighbor_pos = (position[0] + n[0], position[1] + n[1])
                if neighbor_pos not in self.board:
                    continue
                self.visited.add(position)
                if self.board[position] in self.MAPPING[n] and self.board[neighbor_pos] in self.ALLOWED_NEIGHBORS[n]:
                    queue.append(neighbor_pos)

    def furthest(self):
        """
        The Maze is a loop so the furthest point of the loop is half the length of the loop
        """
        return len(self.visited) // 2

    def enclosed(self):
        pass

    def enclosed_wrong(self):
        _("\n".join(self.source))
        grid = [row.replace("S", self.start_char) for row in self.source]
        _("\n".join(grid))
        grid = ["".join(ch if (r, c) in self.visited else "." for c, ch in enumerate(row)) for r, row in
                enumerate(grid)]
        _("\n".join(grid))

        outside = set()

        for r, row in enumerate(grid):
            within = False
            up = None
            for c, ch in enumerate(row):
                if ch == "|":
                    assert up is None
                    within = not within
                elif ch == "-":
                    assert up is not None
                elif ch in "LF":
                    assert up is None
                    up = ch == "L"
                elif ch in "7J":
                    assert up is not None
                    if ch != ("J" if up else "7"):
                        within = not within
                    up = None
                elif ch == ".":
                    pass
                else:
                    raise RuntimeError(f"unexpected character (horizontal): {ch}")
                if not within:
                    outside.add((r, c))

        return len(grid) * len(grid[0]) - len(outside | self.visited)


def part_1(source):
    return PipeMaze(source).furthest()


def part_2(source):
    return PipeMaze(source).enclosed()


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ""")
        self.test_source2 = read_rows(""".....
.S-7.
.|.|.
.L-J.
.....""")
        self.test_source3 = read_rows("""...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........""")
        self.test_source4 = read_rows("""..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........""")
        self.test_source5 = read_rows(""".F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...""")
        self.test_source6 = read_rows(""".F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...""")

    def test_example_data_part_1(self):
        self.assertEqual(8, part_1(self.test_source))

    def test_example_data_part_1_2(self):
        self.assertEqual(4, part_1(self.test_source2))

    def test_part_1(self):
        self.assertEqual(6757, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(4, part_2(self.test_source3))

    def test_example_data_part_2_4(self):
        self.assertEqual(4, part_2(self.test_source4))

    def test_example_data_part_2_5(self):
        self.assertEqual(8, part_2(self.test_source5))

    def test_example_data_part_2_6(self):
        self.assertEqual(10, part_2(self.test_source6))

    def test_part_2(self):
        self.assertEqual(523, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
