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
from heapq import heappush, heappop
from pathlib import Path
from typing import Generic, TypeVar, Callable, List, Optional, NamedTuple, Dict

from ivonet.files import read_int_matrix
from ivonet.grid import neighbors
from ivonet.iter import ints

sys.dont_write_bytecode = True

T = TypeVar('T')


class MazeLocation(NamedTuple):
    row: int
    col: int


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


def node_to_path(node: Node[T]) -> List[T]:
    path: List[T] = [node.state]
    # work backwards from end to front
    while node.parent is not None:
        node = node.parent
        path.append(node.state)
    path.reverse()
    return path


def astar(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]],
          cost_calc: Callable[[T], float], heuristic: Callable[[T], float]) -> Optional[Node[T]]:
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
        for child in successors(current_state):
            new_cost: float = current_node.cost + cost_calc(current_node.state)

            if child not in explored or explored[child] > new_cost:
                explored[child] = new_cost
                frontier.push(Node(child, current_node, new_cost, heuristic(child)))
    return Node(MazeLocation(-1, -1), None, -1)  # went through everything and never found goal


class Cavern(Generic[T]):

    def __init__(self, grid) -> None:
        self.grid = grid
        self.rows = len(grid)
        self.columns = len(grid[0])
        self.goal = MazeLocation(self.rows - 1, self.columns - 1)
        self.start = MazeLocation(0, 0)
        self.risks: dict[MazeLocation] = {}
        self.make_risk_map()

    def successors(self, current: MazeLocation) -> list[MazeLocation]:
        nb = [MazeLocation(r, c) for r, c in neighbors(self.grid, (current.row, current.col), diagonal=False)]
        return nb

    def cost(self, location: MazeLocation) -> float:
        if location.row == 0 and location.col == 0:
            return 0
        return self.grid[location.row][location.col]

    def goal_test(self, location: MazeLocation) -> bool:
        return location == self.goal

    def make_risk_map(self):
        for r, row in enumerate(self.grid):
            for c, col in enumerate(row):
                self.risks[MazeLocation(r, c)] = col


def manhattan_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation) -> float:
        xdist: int = abs(ml.col - goal.col)
        ydist: int = abs(ml.row - goal.row)
        return xdist + ydist

    return distance


def part_1(grid):
    cavern = Cavern(grid)
    distance = manhattan_distance(MazeLocation(cavern.rows, cavern.columns))
    solution = astar(MazeLocation(0, 0), cavern.goal_test, cavern.successors, cavern.cost, distance)
    print(solution)
    return solution.cost


def part_2(source):
    return 0


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = ints(Path(__file__).name)[0]
        self.source = read_int_matrix(f"day_{day}.txt")
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
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(2800, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
