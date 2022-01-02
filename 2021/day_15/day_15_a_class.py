#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import sys
import unittest
from collections import Callable
from pathlib import Path
from typing import Dict, NamedTuple
from typing import TypeVar

from ivonet.files import read_int_matrix
from ivonet.grid import neighbors_defined_grid
from ivonet.iter import ints
from ivonet.search import astar

sys.dont_write_bytecode = True

T = TypeVar('T')


class MazeLocation(NamedTuple):
    row: int
    col: int


def manhattan_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation) -> float:
        xdist: int = abs(ml.col - goal.col)
        ydist: int = abs(ml.row - goal.row)
        return xdist + ydist

    return distance


def is_goal(goal: MazeLocation) -> Callable[[MazeLocation], bool]:
    def reached(current: MazeLocation) -> bool:
        return current == goal

    return reached


def adjoining(height, width) -> Callable[[MazeLocation], list[MazeLocation]]:
    def adjacent(ml: MazeLocation) -> list[MazeLocation]:
        nb = [MazeLocation(r, c) for r, c in
              neighbors_defined_grid((ml.row, ml.col), grid=(width, height), diagonal=False)]
        return nb

    return adjacent


def cost(risks: Dict[MazeLocation, int]) -> Callable[[MazeLocation], int]:
    def get_cost(ml: MazeLocation) -> int:
        return risks[ml]

    return get_cost


class Cavern(object):

    def __init__(self, source) -> None:
        self.source = source
        self.height = len(source)
        self.width = len(source[0])
        self.start = MazeLocation(0, 0)
        self.first_goal = MazeLocation(self.height - 1, self.width - 1)
        self.chiton_risks = self._make_risk_map()
        self.full_height = self.height * 5
        self.full_width = self.width * 5
        self.final_goal = MazeLocation(self.full_height - 1, self.full_width - 1)
        self.full_chiton_risks = self._make_extended_risk_map()

    def _make_risk_map(self) -> Dict[MazeLocation, int]:
        risks: Dict[MazeLocation, int] = {}
        for r, row in enumerate(self.source):
            for c, risk in enumerate(row):
                risks[MazeLocation(r, c)] = risk
        return risks

    def _make_extended_risk_map(self) -> Dict[MazeLocation, int]:
        expanded_risks: Dict[MazeLocation, int] = {}
        for k, v in self.chiton_risks.items():
            for r in range(5):
                for c in range(5):
                    increase = r + c
                    value = 1 + (v + increase - 1) % 9
                    expanded_risks[MazeLocation(k.row + r * self.height, k.col + c * self.width)] = value
        return expanded_risks

    def part_1(self):
        solution = astar(self.start,
                         is_goal(self.first_goal),
                         adjoining(self.height, self.width),
                         manhattan_distance(self.final_goal),
                         cost(self.chiton_risks))
        if solution:
            # print(solution)
            # print(node_to_path(solution))
            return solution.cost
        raise ValueError("Part 1: No solution found.")

    def part_2(self):
        solution = astar(self.start,
                         is_goal(self.final_goal),
                         adjoining(self.full_height, self.full_width),
                         manhattan_distance(self.final_goal),
                         cost(self.full_chiton_risks))
        if solution:
            # print(solution)
            # print(node_to_path(solution))
            return solution.cost
        raise ValueError("Part 2: No solution found.")


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_int_matrix(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}.input")))
        self.test_source = read_int_matrix("""1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581""")

    def test_example_data_part_1(self):
        self.assertEqual(40, Cavern(self.test_source).part_1())

    def test_part_1(self):
        self.assertEqual(458, Cavern(self.source).part_1())

    def test_example_data_part_2(self):
        self.assertEqual(315, Cavern(self.test_source).part_2())

    def test_part_2(self):
        self.assertEqual(2800, Cavern(self.source).part_2())


if __name__ == '__main__':
    unittest.main()
