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


DIRECTIONS = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1)
}


def parse(source, part2=False):
    grid = []
    moves = ""
    pgrid = True
    start = (0, 0)
    for r, line in enumerate(source):
        if not line:
            pgrid = False
        if pgrid:
            if part2:
                new_line = []
                for l in line:
                    if l == "@":
                        start = r, len(new_line)
                        new_line.append(".")
                        new_line.append(".")
                    if l == "#":
                        new_line.append("#")
                        new_line.append("#")
                    if l == ".":
                        new_line.append(".")
                        new_line.append(".")
                    if l == "O":
                        new_line.append("[")
                        new_line.append("]")
                grid.append(new_line)
            else:
                line = list(line.strip())
                if "@" in line:
                    c = line.index("@")
                    line[c] = "."
                    start = r, c
                grid.append(line)
        else:
            moves += line.strip()
    return Robot(grid, start, moves)



class Robot:
    def __init__(self, grid, start, moves):
        self.grid = grid
        self.moves = moves
        self.row = start[0]
        self.col = start[1]

    def move(self, dr, dc):
        """
        Moves the robot in the specified direction (`dr`, `dc`).
        It handles the movement of the robot when it encounters a box (`"O"`, `"["`, or `"]"`) in the grid.

        1. Check for Box:
            - If the next cell (nr, nc) contains a box, the robot needs to move it.

        2. Initialize Queue and Seen Set:
            - A queue (deque) is initialized to keep track of cells to process.
            - The robot's current position is added to the queue.
            - A set (seen) is initialized to keep track of visited cells.
            - A flag (is_move_possible) is set to True to indicate if the move is possible.

        3. Process the Queue:
            - While there are cells in the queue, process each cell.
            - Dequeue a cell (rr, cc).
            - If the cell has already been seen, skip it.
            - Mark the cell as seen.
            - Calculate the next cell (rrr, ccc) in the direction of movement.

        4. Check for Obstacles:
            - If the next cell is a wall (#), set is_move_possible to False and break out of the loop.

        5. Add Adjacent Cells to Queue:
            - If the next cell contains a box (O, [, or ]), add it to the queue.
            - For [, also add the cell to the right.
            - For ], also add the cell to the left.

        6. Move the Box(es):
            - Sort the seen list to move the box(es) in the correct order.
            - While there are cells in the seen list, move the box(es) if the move is possible.
            - Update the grid with the new box position.
            - Update the grid with the empty space at the old box position.
            - Remove the cell from the seen list.

        That should do it :-)
        """
        nr = self.row + dr  # potential new row
        nc = self.col + dc  # potential new column
        if self.grid[nr][nc] == "#":  # wall
            return
        if self.grid[nr][nc] == ".":  # empty space
            self.row = nr
            self.col = nc
            return
        if self.grid[nr][nc] in ["O", "[", "]"]:  # box needs to be moved
            queue = deque()
            queue.append((self.row, self.col))
            seen = set()
            is_move_possible = True
            while queue:
                rr, cc = queue.popleft()
                if (rr, cc) in seen:  # no need to check again
                    continue
                seen.add((rr, cc))
                rrr = rr + dr
                ccc = cc + dc
                if self.grid[rrr][ccc] == "#":  # wall
                    is_move_possible = False
                    break
                if self.grid[rrr][ccc] == "O":  # box
                    queue.append((rrr, ccc))
                if self.grid[rrr][ccc] == "[":  # left box part
                    queue.append((rrr, ccc))
                    queue.append((rrr, ccc + 1))  # right box part
                if self.grid[rrr][ccc] == "]":  # right box part
                    queue.append((rrr, ccc))
                    queue.append((rrr, ccc - 1))  # left box part
            if not is_move_possible:  # wall encountered
                return
            seen = sorted(seen)  # sort the seen list to move the box(es) in the correct order
            while seen:  # move the box(es) in the seen list if move is possible
                for rr, cc in seen:
                    rrr, ccc = rr + dr, cc + dc
                    if (rrr, ccc) not in seen:
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
                if self.grid[r][c] in ["O", "["]:
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
    robot = parse(source)
    answer = robot.run()
    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:
    robot = parse(source, True)
    answer = robot.run()
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
        self.assertEqual(1751, part_2(self.test_source))

    def test_example_data_part_2a(self) -> None:
        self.assertEqual(9021, part_2(self.test_source_a))

    def test_example_data_part_2b(self) -> None:
        self.assertEqual(618, part_2(self.test_source_b))

    def test_part_2(self) -> None:
        self.assertEqual(1392847, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")
        self.test_source_a = read_rows(f"{folder}/test_{day}_a.input")
        self.test_source_b = read_rows(f"{folder}/test_{day}_b.input")


if __name__ == '__main__':
    unittest.main()
