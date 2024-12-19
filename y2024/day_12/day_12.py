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


from collections import deque


def bfs(grid, start, target_value):
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visited = set()
    queue = deque([start])
    area_size = 0
    coordinates = []
    perimeter = 0

    while queue:
        r, c = queue.popleft()
        if (r, c) in visited:
            continue
        visited.add((r, c))
        area_size += 1
        coordinates.append((r, c))

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] != target_value:
                    perimeter += 1
                elif (nr, nc) not in visited:
                    queue.append((nr, nc))
            else:
                perimeter += 1

    return target_value, area_size, coordinates, perimeter

def find_all_areas(grid):
    areas = []
    visited = set()
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if (r, c) not in visited and grid[r][c] != ' ':
                area_type, area_size, coordinates, perimeter = bfs(grid, (r, c), grid[r][c])
                areas.append((area_type, area_size, coordinates, perimeter))
                visited.update(coordinates)
    return areas


@debug
@timer
def part_1(source) -> int | None:
    """Ooof I think this might be a modified bfs for finding the longest path
    for every patch and then doing magic with that somehow"""
    areas = find_all_areas(source)
    answer = 0
    for area_type, area_size, coordinates, perimeter in areas:
        p(f"A region of {area_type} plants with price {area_size} * {perimeter} = {area_size * perimeter}")
        answer += area_size * perimeter
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
        self.assertEqual(1930, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(None, part_1(self.source))

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
