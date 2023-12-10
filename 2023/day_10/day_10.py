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

collections.Callable = collections.abc.Callable
from collections import deque
from pathlib import Path

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

    POSSIBLE_START_CHARS = {"|", "-", "J", "L", "7", "F"}

    ALLOWED_NEIGHBORS = {
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

    PIPE_TYPES = {
        "|": ["n", "s"],
        "-": ["w", "e"],
        "L": ["n", "e"],
        "J": ["n", "w"],
        "7": ["s", "w"],
        "F": ["s", "e"],
        'S': ["n", "s", "w", "e"],
    }

    def __init__(self, source):
        self.source = source
        self.board, self.start = self.__create_board(source)
        self.visited = {}
        self.__bfs()

    @staticmethod
    def __create_board(source):
        board = {}
        start = None
        for row, line in enumerate(source):
            for col, c in enumerate(line):
                board[(col, row)] = c
                if c == 'S':
                    start = (col, row)
        return board, start

    @property
    def start_char(self):
        possible_s = self.POSSIBLE_START_CHARS.copy()
        position = self.start
        for n in self.NEIGHBORS:
            neighbor_pos = (position[0] + n[0], position[1] + n[1])
            if neighbor_pos not in self.board:
                continue
            if self.board[neighbor_pos] in self.ALLOWED_NEIGHBORS[n]:
                possible_s &= self.MAPPING[n]
        start_ch = list(possible_s)[0] if len(possible_s) == 1 else None
        if start_ch is None:
            raise RuntimeError("No start character found")
        return start_ch

    @property
    def start_neighbors(self):
        start_neighbors = []
        position = self.start
        for n in self.NEIGHBORS:
            neighbor_pos = (position[0] + n[0], position[1] + n[1])
            if neighbor_pos not in self.board:
                continue
            if self.board[neighbor_pos] in self.ALLOWED_NEIGHBORS[n]:
                start_neighbors.append((neighbor_pos, 1))
        return start_neighbors

    def __bfs(self):
        """Breath first search (bfs) to find the furthest point in a loop"""
        queue = deque([(self.start, 0)])
        self.visited[self.start] = 0
        while queue:
            position, distance = queue.popleft()
            [queue.append(p) for p in self.start_neighbors if position == self.start]
            if position in self.visited:
                continue
            self.visited[position] = distance
            for n in self.NEIGHBORS:
                neighbor_pos = (position[0] + n[0], position[1] + n[1])
                if neighbor_pos not in self.board:
                    continue
                if self.board[position] in self.MAPPING[n] and self.board[neighbor_pos] in self.ALLOWED_NEIGHBORS[n]:
                    queue.append((neighbor_pos, distance + 1))

    def furthest(self):
        return max(self.visited.values())

    def enclosed(self):
        board = [[c for c in line.strip()] for line in self.source]
        board[self.start[1]][self.start[0]] = self.start_char

        if DEBUG:
            for line in board:
                print("".join(line))

        for i, row in enumerate(board):
            norths = 0
            for j, place in enumerate(row):
                if (j, i) in self.visited:
                    pipe_directions = self.PIPE_TYPES[place]
                    if "n" in pipe_directions:
                        norths += 1
                    continue
                if norths % 2 == 0:
                    board[i][j] = "O"
                else:
                    board[i][j] = "I"

        if DEBUG:
            for line in board:
                print("".join(line))

        inside_count = "\n".join(["".join(line) for line in board]).count("I")
        return inside_count


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
        self.test_source6 = read_rows("""FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L""")

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
