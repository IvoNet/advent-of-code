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
from collections import deque, abc
from pathlib import Path

import pyperclip

from ivonet.decorators import debug
from ivonet.decorators import timer
from ivonet.files import read_rows
from ivonet.iter import ints

collections.Callable = abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def parse(source):
    grid = []
    moves = ""
    pgrid = True
    start = (0, 0)
    for r, line in enumerate(source):
        if not line:
            pgrid = False
        if pgrid:
            line = list(line.strip())
            if "@" in line:
                c = line.index("@")
                line[c] = "."
                start = r, c
            grid.append(line)
        else:
            moves += line.strip()
    return Robot(grid, start, moves)


DIRECTIONS = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1)
}


class Robot:
    def __init__(self, grid, start, moves):
        self.grid = grid
        self.moves = moves
        self.row = start[0]
        self.col = start[1]

    def move(self, dr, dc):
        nr, nc = self.row + dr, self.col + dc
        if self.grid[nr][nc] == "#":
            return
        if self.grid[nr][nc] in ".":
            self.row, self.col = nr, nc
            return
        if self.grid[nr][nc] in ["O"]:
            queue = deque([(nr, nc)])
            seen = set()
            ok = True
            while queue:
                rr, cc = queue.popleft()
                if (rr, cc) in seen:
                    continue
                seen.add((rr, cc))
                rrr, ccc = rr + dr, cc + dc
                if self.grid[rrr][ccc] == "#":
                    ok = False
                    break
                if self.grid[rrr][ccc] == "O":
                    queue.append((rrr, ccc))
            if not ok:
                return
            while len(seen) > 0:
                for rr, cc in sorted(seen):
                    rrr, ccc = rr + dr, cc + dc
                    if (rrr, ccc) not in seen:
                        assert self.grid[rrr][ccc] == "."
                        self.grid[rrr][ccc] = self.grid[rr][cc]
                        self.grid[rr][cc] = "."
                        seen.remove((rr, cc))
            self.row += dr
            self.col += dc

    def run(self):
        for move in self.moves:
            dr, dc = DIRECTIONS[move]
            self.move(dr, dc)
            p(self)
        gps_coordinates = 0
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                if self.grid[r][c] in ["O"]:
                    gps_coordinates += r * 100 + c
        print(self)
        return gps_coordinates

    def __str__(self):
        self.grid[self.row][self.col] = "@"
        ret = "\n".join("".join(line) for line in self.grid)
        self.grid[self.row][self.col] = "."
        return ret

    def __repr__(self):
        return self.__str__(self)


@debug
@timer
def part_1(source) -> int | None:
    answer = 0
    robot = parse(source)
    answer = robot.run()

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
        self.assertEqual(2028, part_1(self.test_source))

    def test_example_data_part_1a(self) -> None:
        self.assertEqual(10092, part_1(self.test_source_a))

    def test_part_1(self) -> None:
        self.assertEqual(1371036, part_1(self.source))

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
        self.test_source_a = read_rows(f"{folder}/test_{day}_a.input")


if __name__ == '__main__':
    unittest.main()
