#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from pathlib import Path
from typing import Dict, Callable
from typing import TypeVar

from ivonet.files import read_int_matrix
from ivonet.grid import neighbors_defined_grid, Location
from ivonet.iter import ints
from ivonet.search import astar

sys.dont_write_bytecode = True

T = TypeVar('T')


def manhattan_distance(goal: Location) -> Callable[[Location], float]:
    def distance(ml: Location) -> float:
        xdist: int = abs(ml.col - goal.col)
        ydist: int = abs(ml.row - goal.row)
        return xdist + ydist

    return distance


def is_goal(goal: Location) -> Callable[[Location], bool]:
    def reached(current: Location) -> bool:
        return current == goal

    return reached


def adjoining(height, width) -> Callable[[Location], list[Location]]:
    def adjacent(ml: Location) -> list[Location]:
        nb = [Location(r, c) for r, c in
              neighbors_defined_grid(Location(ml.row, ml.col), grid=(width, height), diagonal=False)]
        return nb

    return adjacent


def cost_calculator(risks: Dict[Location, int]) -> Callable[[Location], int]:
    def get_cost(ml: Location) -> int:
        return risks[ml]

    return get_cost


def make_risk_map(grid: list[list[int]]) -> Dict[Location, int]:
    risks: Dict[Location, int] = {}
    for r, row in enumerate(grid):
        for c, risk in enumerate(row):
            risks[Location(r, c)] = risk
    return risks


def make_extended_risk_map(risks: Dict[Location, int], width, height) -> Dict[Location, int]:
    expanded_risks: Dict[Location, int] = {}
    for k, v in risks.items():
        for r in range(5):
            for c in range(5):
                increase = r + c
                value = 1 + (v + increase - 1) % 9
                expanded_risks[Location(k.row + r * height, k.col + c * width)] = value
    return expanded_risks


def part_1(source):
    rows = len(source)
    cols = len(source[0])
    start = Location(0, 0)
    goal = Location(rows - 1, cols - 1)
    risks = make_risk_map(source)
    solution = astar(start,  # start at the start
                     is_goal(goal),  # callback function to see if the end goal has been reached
                     adjoining(rows, cols),  # callback to get all the relevant neighbors of a Location
                     manhattan_distance(goal),  # No diagonals allowed so the Manhattan distance calculator callback
                     cost_calculator(risks))  # the cost of going a direction based on the Chiton risk per Location
    if solution:
        # print(solution)
        # print(node_to_path(solution))
        return solution.cost
    raise ValueError("Part 1: No solution found.")


def part_2(source):
    rows = len(source)
    cols = len(source[0])
    start = Location(0, 0)
    new_height = rows * 5
    new_width = cols * 5
    goal = Location(new_height - 1, new_width - 1)
    risks = make_extended_risk_map(make_risk_map(source), rows, cols)
    solution = astar(start,
                     is_goal(goal),
                     adjoining(new_height, new_width),
                     manhattan_distance(goal),
                     cost_calculator(risks))
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
        self.assertEqual(40, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(458, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(315, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(2800, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
