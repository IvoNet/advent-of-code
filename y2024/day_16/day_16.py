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
import heapq
import os
import sys
import unittest
from collections import abc, namedtuple
from collections import defaultdict
from collections import deque
from pathlib import Path

import pyperclip
from ivonet.decorators import debug
from ivonet.decorators import timer
from ivonet.files import read_rows
from ivonet.grid import Location
from ivonet.iter import ints

collections.Callable = abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


DIRECTIONS = [
    Location(-1, 0),  # north
    Location(0, 1),  # east
    Location(1, 0),  # south
    Location(0, -1)  # west
]  # north (0), east (1), south (2), west (3)

Node = namedtuple('Node', ['cost', 'location', 'direction', 'path'])


def visualize(grid, path):
    for r, c in path:
        grid[r][c] = "O"
    for row in grid:
        print("".join(row))


def parse(source):
    grid = []
    start = None
    end = None
    for r, row in enumerate(source):
        grid.append(list(row))
        if "S" in row:
            start = Location(r, row.index("S"))
        if "E" in row:
            end = Location(r, row.index("E"))
    return grid, start, end


def dijkstra_1(grid, start, goal):
    queue = []
    seen = set()
    distances = {}
    heapq.heappush(queue, Node(0, start, 1, [start]))
    while queue:
        cost, loc, direction, path = heapq.heappop(queue)
        if (loc, direction) not in distances:
            distances[(loc, direction)] = cost
        if loc == goal:
            visualize(grid, path)
            return cost, path
        if (loc, direction) in seen:
            continue
        seen.add((loc, direction))
        current_direction = DIRECTIONS[direction]
        new_loc = loc + current_direction
        if 0 <= new_loc.row < len(grid) and 0 <= new_loc.col < len(grid[0]) and grid[new_loc.row][new_loc.col] != '#':
            heapq.heappush(queue, Node(cost + 1, new_loc, direction, path + [new_loc]))
        heapq.heappush(queue, Node(cost + 1000, loc, (direction + 1) % 4, path))  # right
        heapq.heappush(queue, Node(cost + 1000, loc, (direction + 3) % 4, path))  # left


def dijkstra_with_bfs(grid, start, goal):
    """
    Implements a modified Dijkstra's algorithm combined with BFS to find all the paths with the lowest cost.

    The function uses a priority queue to explore the grid, starting from the start location and aiming to reach the goal.
    It keeps track of the lowest cost to reach each location and the direction from which it arrived.
    The algorithm also backtracks to find all possible paths to the goal.

    Args:
        grid (list[list[str]]): The grid representing the map, where each cell can be a path or a wall.
        start (Location): The starting location in the grid.
        goal (Location): The goal location in the grid.

    Returns:
        tuple: A tuple containing the best cost to reach the goal and the number of unique locations visited.

    The algorithm works as follows:
    1. Initialize a priority queue with the starting node.
    2. Use a defaultdict to keep track of the lowest cost to reach each location and direction.
    3. Use a set to keep track of the end states (goal locations reached).
    4. While the queue is not empty:
        a. Pop the node with the lowest cost.
        b. If the current cost is higher than the recorded lowest cost for this location and direction, skip it.
        c. If the current location is the goal and the cost is higher than the best cost, break the loop.
        d. Update the best cost and add the current location and direction to the end states.
        e. For each possible move (forward, right, left):
            i. Calculate the new cost, location, and direction.
            ii. If the new location is within the grid bounds and not a wall:
                - If the new cost is higher than the recorded lowest cost, skip it.
                - If the new cost is lower, update the backtrack dictionary and the lowest cost.
                - Add the new state to the priority queue.
    5. Use a deque to backtrack from the end states to find all unique locations visited.
    6. Return the best cost and the number of unique locations visited.
    """
    queue = []
    lowest_cost = defaultdict(lambda: float("inf"))
    best_cost = float("inf")
    backtrack = {}
    end_states = set()
    heapq.heappush(queue, Node(0, start, 1, [start]))
    while queue:
        cost, loc, direction, path = heapq.heappop(queue)
        if cost > lowest_cost[(loc, direction)]:  # if we have a better path to this location
            continue
        if loc == goal:
            if cost > best_cost:
                break
            best_cost = cost
            end_states.add((loc, direction))

        for new_cost, new_loc, new_direction in [(cost + 1, loc + DIRECTIONS[direction], direction),  # forward
                                                 (cost + 1000, loc, (direction + 1) % 4),  # right
                                                 (cost + 1000, loc, (direction + 3) % 4)  # left
                                                 ]:
            if (0 <= new_loc.row < len(grid)
                    and 0 <= new_loc.col < len(grid[0])
                    and grid[new_loc.row][new_loc.col] != '#'):
                lowest = lowest_cost.get((new_loc, new_direction), float("inf"))
                if new_cost > lowest:
                    continue
                if new_cost < lowest:
                    backtrack[(new_loc, new_direction)] = set()
                    lowest_cost[(new_loc, new_direction)] = new_cost
                backtrack[(new_loc, new_direction)].add((loc, direction))
                heapq.heappush(queue, Node(new_cost, new_loc, new_direction, path + [new_loc]))

    states = deque(end_states)
    seen = set(end_states)

    while states:
        key = states.popleft()
        for last in backtrack.get(key, []):
            if last in seen:
                continue
            seen.add(last)
            states.append(last)

    return best_cost, len({loc for loc, _ in seen})


@debug
@timer
def part_1(source) -> int | None:
    grid, start, end = parse(source)
    p(grid, start, end)
    answer, _ = dijkstra_with_bfs(grid, start, end)
    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:
    answer = 0
    grid, start, end = parse(source)
    p(grid, start, end)
    cost, places = dijkstra_with_bfs(grid, start, end)
    answer = places

    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(7036, part_1(self.test_source))

    def test_example_data_part_1a(self) -> None:
        self.assertEqual(11048, part_1(self.test_source_1))

    def test_part_1(self) -> None:
        self.assertEqual(92432, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(45, part_2(self.test_source))

    def test_example_data_part_2a(self) -> None:
        self.assertEqual(64, part_2(self.test_source_1))

    def test_part_2(self) -> None:
        self.assertEqual(458, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")
        self.test_source_1 = read_rows(f"{folder}/test_{day}_1.input")


if __name__ == '__main__':
    unittest.main()
