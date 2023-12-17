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
from typing import TypeVar, Generic

from ivonet.collection import PriorityQueue
from ivonet.files import read_int_matrix
from ivonet.grid import Location
from ivonet.iter import ints

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = False
T = TypeVar('T')


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def node_to_path(node: Node) -> list[Location]:
    """
    Returns the path from the node to the start node
    :param node:
    :return:
    """
    path: list[Location] = [node.location]
    # work backwards from end to front
    while node.parent is not None:
        node = node.parent
        path.append(node.location)
    path.reverse()
    return path


def print_solution(solution_node: Node, source: list[list[int]]) -> None:
    if DEBUG:
        grid = [[str(element) for element in row] for row in source]
        for loc in node_to_path(solution_node):
            grid[loc.row][loc.col] = "#"
        for row in grid:
            print("".join(row))


class Node(Generic[T]):
    """
    Represents a node in the grid.
    it has all the information needed to calculate the cost and the path to this node and keep track of the direction
    """

    def __init__(self, row: int, col: int, direction_row: int, direction_col: int, cost: int,
                 parent: Node | None):
        self.row = row
        self.col = col
        self.direction_row = direction_row
        self.direction_col = direction_col
        self.cost = cost
        self.parent = parent

    @property
    def state(self) -> tuple[int, int, int, int, int]:
        """
        The state is the representation of the node in as a hashable tuple without the parent or the cost
        this is important for the "explored" set as the cost will change but the state will not.
        """
        return self.row, self.col, self.direction_row, self.direction_col, self.steps

    @property
    def location(self) -> Location:
        """
        The location of the node in the grid. Needed for goal comparison.
        """
        return Location(self.row, self.col)

    @property
    def steps(self) -> int:
        """
        The number of steps taken to reach this node in a straight line in any direction as long as the direction is
        the same.
        This is needed to prevent going in the same direction for more than the allowed max steps in a direction.
        We do not need to keep track of the number of steps as we can calculate it from the parent nodes.
        """
        nn = self
        steps = 0
        while nn.parent and self.direction_row == nn.direction_row and self.direction_col == nn.direction_col:
            steps += 1
            nn = nn.parent
        return steps

    def __lt__(self, other: Node) -> bool:
        """
        The priority queue needs to know which node is more important than the other.
        In this case only the cost is important for that not the distance traveled (like manhattan distance)
        """
        return self.cost < other.cost

    def __repr__(self) -> str:
        return f"({self.row}, {self.col}) - ({self.direction_row}, {self.direction_col}) - {self.cost} - {self.steps} - {self.parent}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Node):
            return False
        return self.state == other.state

    def __hash__(self) -> int:
        return hash(self.state)


def not_opposite(c_node, n_d_col, n_d_row):
    return (n_d_row, n_d_col) != (-c_node.direction_row, -c_node.direction_col)


def not_same(c_node, n_d_col, n_d_row):
    return (n_d_row, n_d_col) != (c_node.direction_row, c_node.direction_col)


def starting_point(node):
    """
    Only at the starting point is there no direction yet.
    Feels a bit like a hack :-) but it works.
    """
    return (node.direction_row, node.direction_col) == (0, 0)


def astar(grid: list[list[int]], max_steps: int = 3, min_turn: int = 0) -> Node:
    """
    Implements the A* search algorithm to find the shortest path in a grid.

    Parameters:
    grid (list[list[int]]): A 2D list representing the grid to be traversed. Each element in the grid represents the
                              cost in heat loss of visiting that cell.
    max_steps (int, optional): The maximum number of steps that can be taken in the same direction. Defaults to 3.
    min_turn (int, optional): The minimum number of steps that must be taken before a turn can be made. Defaults to 0.

    Returns:
    Node: The goal node which contains the path from the start node to the goal node and the total cost.

    The function works as follows:
    1. It starts by defining the start and goal nodes. The start node is always at the top left of the grid (0, 0),
       and the goal node is always at the bottom right of the grid.
    2. It then creates an empty set `explored` to keep track of the nodes that have already been visited, and a
       priority queue `priority_queue` to keep track of the nodes to be visited. The start node is added to the
       priority queue.
    3. The function then enters a loop that continues until the priority queue is empty. In each iteration of the loop,
       it does the following:
         - It pops a node from the priority queue. If this node is the goal node, it returns the node and ends
           the function.
         - If the node has already been explored, it skips the rest of the loop and moves on to the next iteration.
         - If the node has not been explored, it adds the node to the set of explored nodes.
         - If the current node has taken less than `max_steps` in its current direction and is not at the start, it
           generates a new node in the same direction and adds it to the priority queue.
         - If the current node has taken at least `min_turn` steps or is at the start, it generates new nodes in
           all other valid directions and adds them to the priority queue.
    4. If the function exits the loop without finding the goal node, it raises a `ValueError` indicating that no
       solution was found.
    """
    height: int = len(grid)
    width: int = len(grid[0])
    goal = Location(height - 1, width - 1)
    explored: set[tuple[int, int, int, int, int]] = set()
    start: Node = Node(0, 0, 0, 0, 0, None)
    priority_queue: PriorityQueue = PriorityQueue()
    priority_queue.push(start)

    while not priority_queue.empty:
        c_node = priority_queue.pop()
        if c_node.location == goal:
            return c_node
        if c_node.state in explored:
            continue
        explored.add(c_node.state)
        if c_node.steps < max_steps and not starting_point(c_node):
            n_row = c_node.row + c_node.direction_row
            n_col = c_node.col + c_node.direction_col
            if 0 <= n_row < height and 0 <= n_col < width:  # check if the new node is within the grid
                new_node: Node = Node(n_row, n_col, c_node.direction_row, c_node.direction_col,
                                      c_node.cost + grid[n_row][n_col], c_node)
                priority_queue.push(new_node)

        if c_node.steps >= min_turn or starting_point(c_node):
            for n_d_row, n_d_col in DIRECTIONS:
                if not_same(c_node, n_d_col, n_d_row) and not_opposite(c_node, n_d_col, n_d_row):
                    n_row = c_node.row + n_d_row
                    n_col = c_node.col + n_d_col
                    if 0 <= n_row < height and 0 <= n_col < width:
                        new_node = Node(n_row, n_col, n_d_row, n_d_col,
                                        c_node.cost + grid[n_row][n_col], c_node)
                        priority_queue.push(new_node)

    raise ValueError("This should not happen.")


def part_1(source: list[list[int]]) -> int:
    solution_node = astar(source, 3, 0)

    # Just for fun
    print_solution(solution_node, source)

    return solution_node.cost


def part_2(source: list[list[int]]) -> int | None:
    solution_node = astar(source, 10, 4)

    print_solution(solution_node, source)

    return solution_node.cost


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(102, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(686, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(94, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(801, part_2(self.source))

    def setUp(self) -> None:
        _()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_int_matrix(f"{folder}/day_{day}.input")
        self.test_source = read_int_matrix(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
