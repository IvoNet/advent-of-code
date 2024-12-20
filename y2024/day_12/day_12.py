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
from collections import abc, defaultdict
import os
import sys
import unittest
from pathlib import Path

import pyperclip
from ivonet.decorators import debug
from ivonet.decorators import timer
from ivonet.files import read_rows
from ivonet.iter import ints

collections.Callable = abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


from collections import deque

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def bfs(grid, start, target_value):
    rows, cols = len(grid), len(grid[0])
    visited = set()
    queue = deque([start])
    area_size = 0
    coordinates = []
    perimeter = 0
    perimeter_coords = defaultdict(set)

    while queue:
        r, c = queue.popleft()
        if (r, c) in visited:
            continue
        visited.add((r, c))
        area_size += 1
        coordinates.append((r, c))

        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == target_value:
                if (nr, nc) not in visited:
                    queue.append((nr, nc))
            else:
                perimeter += 1
                perimeter_coords[(dr, dc)].add((r, c))

    return target_value, area_size, coordinates, perimeter, perimeter_coords


def find_all_areas(grid):
    areas = []
    visited = set()
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if (r, c) not in visited and grid[r][c] != ' ':
                area_type, area_size, coordinates, perimeter, perimeter_coords = bfs(grid, (r, c), grid[r][c])
                areas.append((area_type, area_size, coordinates, perimeter, perimeter_coords))
                visited.update(coordinates)
    return areas

def calc_sides(perimeter_coords):
    """
    Calculates the number of unique sides of the perimeter of an area in a grid.

    This function counts the number of unique sides by exploring all connected perimeter
    coordinates using BFS and ensuring each side is counted only once.
    """
    sides = 0
    for direction, dir_coords in perimeter_coords.items():
        seen = set()
        for (pr, pc) in dir_coords:
            if (pr, pc) not in seen:
                sides += 1
                queue = deque([(pr, pc)])
                while queue:
                    r2, c2 = queue.popleft()
                    if (r2, c2) in seen:
                        continue
                    seen.add((r2, c2))
                    for dr, dc in DIRECTIONS:
                        rr, cc = r2 + dr, c2 + dc
                        if (rr, cc) in dir_coords:
                            queue.append((rr, cc))
    return sides

@debug
@timer
def part_1(source) -> int | None:
    """Ooof I think this might be a modified bfs for finding the longest path in stead of the shortest"""
    areas = find_all_areas(source)
    answer = 0
    for area_type, area_size, coordinates, perimeter, perimeter_coords in areas:
        p(f"A region of {area_type} plants with price {area_size} * {perimeter} = {area_size * perimeter}")
        answer += area_size * perimeter
    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:
    answer = 0
    areas = find_all_areas(source)
    p(areas)
    for area_type, area_size, coordinates, perimeter, perimeter_coords in areas:
        sides = calc_sides(perimeter_coords)
        answer += sides*area_size

    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(1930, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(1450422, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(1206, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(906606, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
