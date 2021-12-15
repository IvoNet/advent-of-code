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
from heapq import heappush, heappop
from pathlib import Path
from typing import Generic, List, Dict, Optional, NamedTuple
from typing import TypeVar

from ivonet.files import read_int_matrix
from ivonet.grid import neighbors_defined_grid
from ivonet.iter import ints

sys.dont_write_bytecode = True

T = TypeVar('T')


class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self._container  # not is true for empty container

    def push(self, item: T) -> None:
        heappush(self._container, item)  # in by priority

    def pop(self) -> T:
        return heappop(self._container)  # out by priority

    def __repr__(self) -> str:
        return repr(self._container)


class MazeLocation(NamedTuple):
    row: int
    col: int


def node_to_path(node: Node[T]) -> List[T]:
    path: List[T] = [node.state]
    # work backwards from end to front
    while node.parent is not None:
        node = node.parent
        path.append(node.state)
    path.reverse()
    return path


class Node(Generic[T]):
    def __init__(self, state: T, parent: Optional[Node], cost: float = 0.0, heuristic: float = 0.0) -> None:
        self.state: T = state
        self.parent: Optional[Node] = parent
        self.cost: float = cost
        self.heuristic: float = heuristic

    def __lt__(self, other: Node) -> bool:
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

    def __repr__(self) -> str:
        if self.parent:
            return f"state[{self.state}] - cost[{self.cost}] - parent[{self.parent.state}]"
        return f"state[{self.state}] - cost[{self.cost}] - parent[None]"


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


def make_risk_map(grid: list[list[int]]) -> Dict[MazeLocation, int]:
    risks: Dict[MazeLocation, int] = {}
    for r, row in enumerate(grid):
        for c, risk in enumerate(row):
            risks[MazeLocation(r, c)] = risk
    return risks


def astar(initial: T, goal_test: Callable[[T], bool],
          successors: Callable[[T], List[T]],
          heuristic: Callable[[T], float],
          cost: Callable[[T], int]) -> Optional[Node[T]]:
    # frontier is where we've yet to go
    frontier: PriorityQueue[Node[T]] = PriorityQueue()
    frontier.push(Node(initial, None, 0.0, heuristic(initial)))
    # explored is where we've been
    explored: Dict[T, float] = {initial: 0.0}

    # keep going while there is more to explore
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # if we found the goal, we're done
        if goal_test(current_state):
            return current_node
        # check where we can go next and haven't explored
        for nb in successors(current_state):
            new_cost: float = current_node.cost + cost(nb)

            if nb not in explored or explored[nb] > new_cost:
                explored[nb] = new_cost
                frontier.push(Node(nb, current_node, new_cost, heuristic(nb)))
    return None  # went through everything and never found goal


def part_1(source):
    rows = len(source)
    cols = len(source[0])
    start = MazeLocation(0, 0)
    goal = MazeLocation(rows - 1, cols - 1)
    risks = make_risk_map(source)
    solution = astar(start, is_goal(goal), adjoining(rows, cols), manhattan_distance(goal), cost(risks))
    if solution:
        print(solution)
        print(node_to_path(solution))
        return solution.cost
    raise ValueError("Part 1: No solution found.")


def make_extended_risk_map(risks: Dict[MazeLocation, int], width, height) -> Dict[MazeLocation, int]:
    expanded_risks: Dict[MazeLocation, int] = {}
    for k, v in risks.items():
        for r in range(5):
            for c in range(5):
                increase = r + c
                value = 1 + (v + increase - 1) % 9
                expanded_risks[MazeLocation(k.row + r * height, k.col + c * width)] = value
    return expanded_risks


def part_2(source):
    rows = len(source)
    cols = len(source[0])
    start = MazeLocation(0, 0)
    new_height = rows * 5
    new_width = cols * 5
    goal = MazeLocation(new_height - 1, new_width - 1)
    risks = make_extended_risk_map(make_risk_map(source), rows, cols)
    solution = astar(start, is_goal(goal), adjoining(new_height, new_width), manhattan_distance(goal), cost(risks))
    if solution:
        print(solution)
        print(node_to_path(solution))
        return solution.cost
    raise ValueError("Part 1: No solution found.")


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = ints(Path(__file__).name)[0]
        self.source = read_int_matrix(f"day_{day}.txt")
        self.test_source_small = read_int_matrix("""196
138
431""")
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

    def test_example_data_part_1_small(self):
        self.assertEqual(8, part_1(self.test_source_small))

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
