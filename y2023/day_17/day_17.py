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
from typing import Callable, TypeVar, Optional

from ivonet.collection import PriorityQueue
from ivonet.files import read_int_matrix
from ivonet.grid import Location, DIRECTIONS
from ivonet.iter import ints
from ivonet.search import Node

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True
T = TypeVar('T')


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def manhattan_distance(goal: Location) -> Callable[[Location], float]:
    def distance(ml: Location) -> float:
        xdist: int = abs(ml.col - goal.col)
        ydist: int = abs(ml.row - goal.row)
        return xdist + ydist

    return distance


def make_heat_loss_map(grid: list[list[int]]) -> dict[Location, int]:
    risks: dict[Location, int] = {}
    for r, row in enumerate(grid):
        for c, risk in enumerate(row):
            risks[Location(r, c)] = risk
    return risks


def is_goal(goal: Location) -> Callable[[Location], bool]:
    def reached(current: Location) -> bool:
        return current == goal

    return reached


def neighbors_defined_grid(coord: Location, grid=(100, 100), allowed_directions="NESW") -> list[
    Location]:
    height = grid[0] - 1
    width = grid[1] - 1
    current = coord
    adjacent = []
    nb: list[Location] = [v for k, v in DIRECTIONS.items() if k in list(allowed_directions)]
    for loc in nb:
        pos = current + loc
        if pos.col < 0 or pos.col > width or pos.row < 0 or pos.row > height:
            continue
        adjacent.append(pos)
    return adjacent


def adjoining(height, width) -> Callable[[Node[T]], list[Location]]:
    def adjacent(node: Node[T]) -> list[Location]:
        """
        - test if direction is allowed (not more than 3 steps in the same direction)
        - test if direction is allowed (not reverse direction in a block)
        """
        # determine direction
        if node.parent is None:  # start (moving right)
            return [Location(r, c) for r, c in
                    neighbors_defined_grid(Location(node.state.row, node.state.col), grid=(width, height),
                                           allowed_directions="NES")]
        if node.parent.parent is None:  # second step
            # determine direction and eliminate reverse direction
            if node.state.row == node.parent.state.row:  # moving left or right
                return [Location(r, c) for r, c in
                        neighbors_defined_grid(Location(node.state.row, node.state.col), grid=(width, height),
                                               allowed_directions="NES" if node.state.col > node.parent.state.col else "NWS")]
            return [Location(r, c) for r, c in
                    neighbors_defined_grid(Location(node.state.row, node.state.col), grid=(width, height),
                                           allowed_directions="ESW" if node.state.row > node.parent.state.row else "NEW")]
        if node.parent.parent.parent is None:  # third step
            # determine direction and eliminate reverse direction and more than 3 steps in the same direction
            # Hmm it seems that the direction check here is not important as reverse is not allowed, and we are testing for same direction
            if node.state.row == node.parent.state.row:  # moving left or right
                if node.state.row == node.parent.parent.state.row:  # moving left or right and previous move was left or right
                    return [Location(r, c) for r, c in
                            neighbors_defined_grid(Location(node.state.row, node.state.col), grid=(width, height),
                                                   allowed_directions="NS")]
                else:  # moving up or down and previous move was left or right
                    return [Location(r, c) for r, c in
                            neighbors_defined_grid(Location(node.state.row, node.state.col), grid=(width, height),
                                                   allowed_directions="ESW" if node.state.col > node.parent.state.col else "NWE")]
            # optimization later? seems the same the two below
            if node.state.col == node.parent.state.col:  # moving up or down
                if node.parent.state.col == node.parent.parent.state.col:  # moving up or down and previous move was up or down
                    return [Location(r, c) for r, c in
                            neighbors_defined_grid(Location(node.state.row, node.state.col), grid=(width, height),
                                                   allowed_directions="EW")]
                else:  # moving left or right and previous move was up or down
                    return [Location(r, c) for r, c in
                            neighbors_defined_grid(Location(node.state.row, node.state.col), grid=(width, height),
                                                   allowed_directions="NES" if node.state.col > node.parent.state.row else "NEW")]


        raise ValueError("This should not happen")

    return adjacent


def cost_calculator(risks: dict[Location, int]) -> Callable[[Location], int]:
    def get_cost(ml: Location) -> int:
        return risks[ml]

    return get_cost


def astar(initial: T,
          goal_test: Callable[[T], bool],
          successors: Callable[[Node[T]], list[T]],
          heuristic: Callable[[T], float],
          cost: Callable[[T], int]) -> Optional[Node[T]]:
    """The A* (astar)

    is a dfs but you can provide a cost callback function that can direct your search
    (see 2021/Day15 of the Advent of Code for an implementation example)
    """
    # frontier is where we've yet to go
    frontier: PriorityQueue[Node[T]] = PriorityQueue()
    frontier.push(Node(initial, None, 0.0, heuristic(initial)))
    # explored is where we've been
    explored: dict[T, float] = {initial: 0.0}

    # keep going while there is more to explore
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # if we found the goal, we're done
        if goal_test(current_state):
            return current_node
        # check where we can go next and haven't explored
        for nb in successors(current_node):
            new_cost: float = current_node.cost + cost(nb)

            if nb not in explored or explored[nb] > new_cost:
                explored[nb] = new_cost
                frontier.push(Node(nb, current_node, new_cost, heuristic(nb)))
    return None  # went through everything and never found goal


def part_1(source: list[list[int]]) -> int | None:
    """
     Depth First Search
     - grid of single digits. the digit indicates the cost of moving to that square
     - you can not move diagonally
     - you can not reverse direction in a block. in a block you can only go in the same direction, move left or right
     - you can not go more than 3 steps in the same direction
     - find the path from top left to bottom right with the lowest cost

     """
    rows = len(source)
    cols = len(source[0])
    start = Location(0, 0)
    goal = Location(rows - 1, cols - 1)
    risks = make_heat_loss_map(source)
    solution = astar(start,  # start at the start
                     is_goal(goal),  # callback function to see if the end goal has been reached
                     adjoining(rows, cols),  # callback to get all the relevant neighbors of a Location
                     manhattan_distance(goal),  # No diagonals allowed so the Manhattan distance calculator callback
                     cost_calculator(risks))  # the cost of going a direction based on the Chiton risk per Location
    if solution:
        # print(solution)
        # print(node_to_path(solution))
        return int(solution.cost)
    raise ValueError("Part 1: No solution found.")


def part_2(source: list[list[int]]) -> int | None:
    return None


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(102, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(None, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(None, part_2(self.source))

    def setUp(self) -> None:
        _()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_int_matrix(f"{folder}/day_{day}.input")
        self.test_source = read_int_matrix(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
