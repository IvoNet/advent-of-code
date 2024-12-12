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
import unittest
from pathlib import Path

import pyperclip
import sys

from ivonet.direction import directions
from ivonet.files import read_rows
from ivonet.graph import WeightedGraph
from ivonet.grid import is_within_bounds
from ivonet.iter import ints

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def visualize(grid, visited):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if (r, c) in visited:
                print("O", end="")
            else:
                print(grid[r][c], end="")
        print()


def parse(source):
    grid = [list(row) for row in source]
    start = grid[0].index(".")
    goal = grid[-1].index(".")
    return grid, (0, start), (len(grid[0]) - 1, goal)


class LongWalk:
    """
    This is a class that will find the longest path through a grid.
    Optimized for performance by making a graph of the crossroads in the grid.
    """

    def __init__(self, source):
        self.grid, self.start, self.goal = parse(source)
        self.graph: WeightedGraph = WeightedGraph()
        self.seen = set()
        self.crossroads = [self.start, self.goal]
        self.__find_crossroads()
        p(f"crossroads: {self.crossroads}")
        self.__create_graph()
        p(f"graph: {self.graph}")
        self.path = []

    def __find_crossroads(self):
        """
        This method identifies the crossroads in the grid.

        A crossroad is defined as a point in the grid where you can go in 3 or more directions. The method iterates
        over all the points in the grid, and for each point, it checks the number of possible directions from that
        point. If the number of possible directions is 3 or more, the point is considered a crossroad and is added
        to the list of crossroads.

        The method uses the `directions` function to determine the possible directions from a point, and the
        `is_within_bounds` function to check if moving in a direction results in a valid point within the grid.

        This method does not return anything. It modifies the `crossroads` attribute of the `LongWalk` object, which
        is a list that stores the coordinates of all the crossroads in the grid.
        """
        for r, row in enumerate(self.grid):
            for c, col in enumerate(row):
                if col == "#":  # wall
                    continue
                neighbor_count = 0
                for nr, nc in directions(r, c):
                    if is_within_bounds(self.grid, nr, nc) and self.grid[nr][nc] != '#':
                        neighbor_count += 1
                if neighbor_count >= 3:
                    self.crossroads.append((r, c))

    def __create_graph(self):
        """
        This method creates a Graph representation of the grid.

        The method iterates over all the crossroads (points in the grid where you can go in 3 or more directions)
        and adds them as vertices to the graph. Then, for each crossroad, it performs a depth-first search (DFS)
        to find all other crossroads that can be reached from the current crossroad. For each reachable crossroad,
        it adds an edge to the graph between the current crossroad and the reachable crossroad, with the weight of
        the edge being the distance between the two crossroads.

        The method uses a stack to perform the DFS. It starts by pushing the current crossroad into the stack.
        Then, it enters a loop that continues until the stack is empty. In each iteration of the loop, it pops a
        point from the stack, and if this point is a crossroad, it adds an edge to the graph. Otherwise, it pushes
        all neighboring points that have not been visited yet into the stack.

        The method uses a set to keep track of visited points to avoid visiting the same point more than once.

        This method does not return anything. It modifies the `graph` attribute of the `LongWalk` object.
        """
        for sr, sc in self.crossroads:
            self.graph.add_vertex((sr, sc))

        for sr, sc in self.crossroads:
            stack = [(0, sr, sc)]
            seen = {(sr, sc)}

            while stack:
                n, r, c = stack.pop()

                if n != 0 and (r, c) in self.crossroads:
                    self.graph.add_edge_by_vertices((sr, sc), (r, c), n)
                    continue

                for nr, nc in directions(r, c):
                    if (is_within_bounds(self.grid, nr, nc)
                            and self.grid[nr][nc] != "#"
                            and (nr, nc) not in seen):
                        stack.append((n + 1, nr, nc))
                        seen.add((nr, nc))
        p(f"graph: {self.graph}")

    def dfs(self, pt: tuple[int, int] = None):
        if pt is None:
            pt = self.start
        self.path.append(pt)
        if pt == self.goal:
            return 0

        m = -float("inf")

        self.seen.add(pt)
        nx: tuple[int, int]
        for nx, weight in self.graph.neighbors_for_vertex_with_weights(pt):
            if nx not in self.seen:
                m = max(m, self.dfs(nx) + weight)
        self.seen.remove(pt)
        self.path.pop()
        return m


def get_sloped_neighbors(grid, row, col):
    """
    This function determines the neighboring points in a grid that can be visited from a given point,
    considering the direction of movement.

    Parameters:
    - grid (list): A 2D list representing the grid. Each cell in the grid is a character representing a path ('.')
      or a wall ('#'), or a direction ('v', '^', '>', '<').
    - row (int): The row index of the given point in the grid.
    - col (int): The column index of the given point in the grid.

    Returns:
    list: A list of tuples, where each tuple represents the coordinates of a neighboring point that can
          be visited from the given point.

    The function checks the value of the given point in the grid. If it's a directional character ('v', '^', '>', '<'),
    it determines the next point in that direction and checks if it's a valid point within the grid that is not a wall.
     If so, it returns a list containing the coordinates of that point.

    If the value of the given point is not a directional character, it iterates over the four possible directions
    (up, down, left, and right) from the given point. For each direction, it checks if moving in that direction would
    result in a valid point within the grid that is not a wall. If so, it adds the coordinates of that point to the
    list of neighbors.

    This function takes into account the direction of movement, so it can be used in scenarios where the path is sloped
    or the movement is restricted to certain directions.
    """
    if grid[row][col] == "v":  # down
        return [(row + 1, col)]
    if grid[row][col] == "^":  # up
        return [(row - 1, col)]
    if grid[row][col] == ">":  # right
        return [(row, col + 1)]
    if grid[row][col] == "<":  # left
        return [(row, col - 1)]
    neighbours = []
    for nr, nc in directions(row, col):
        if is_within_bounds(grid, nr, nc) and grid[nr][nc] != '#':
            neighbours.append((nr, nc))
    return neighbours


def get_non_sloped_neighbors(grid, row, col):
    """
    This function determines the neighboring points in a grid that can be visited from a given point.

    Parameters:
    grid (list): A 2D list representing the grid. Each cell in the grid is a character representing a path ('.') or a wall ('#').
    row (int): The row index of the given point in the grid.
    col (int): The column index of the given point in the grid.

    Returns:
    list: A list of tuples, where each tuple represents the coordinates of a neighboring point that can be visited from the given point.

    The function iterates over the four possible directions (up, down, left, and right) from the given point. For each direction, it checks if moving in that direction would result in a valid point within the grid that is not a wall. If so, it adds the coordinates of that point to the list of neighbors.

    This function does not consider the direction of movement (i.e., it does not take into account whether the path is sloped or not). Therefore, it can be used in scenarios where movement is allowed in any direction, regardless of the orientation of the path.
    """
    neighbours = []
    for nr, nc in directions(row, col):
        if is_within_bounds(grid, nr, nc) and grid[nr][nc] != '#':
            neighbours.append((nr, nc))
    return neighbours


def dfs_longest_path(grid, start, end, neighbors_func=get_sloped_neighbors, debug=False) -> int:
    """
    This function performs a depth-first search (DFS) to find the longest path in a grid from a start point to an end point.

    Parameters:
    - grid (list): A 2D list representing the grid. Each cell in the grid is a character representing a path ('.')
      or a wall ('#').
    - start (tuple): A tuple representing the coordinates of the start point in the grid.
    - end (tuple): A tuple representing the coordinates of the end point in the grid.
    - neighbors_func (function, optional): A function that takes the grid and a point's coordinates and returns a
      list of neighboring points that can be visited from the given point.
    - debug (bool, optional): A boolean flag used for debugging. If True, the function will print additional
      debug information. By default, it is False.

    The function uses a stack to perform the DFS. It starts by pushing the start point into the stack.
    Then, it enters a loop that continues until the stack is empty. In each iteration of the loop, it pops
    a point from the stack, and if this point is the end point, it updates the longest path length if the
    current path length is longer. Otherwise, it pushes all neighboring points that have not been visited
    yet into the stack.

    The function uses a set to keep track of visited points to avoid visiting the same point more than once.
    It also uses a variable to keep track of the length of the longest path found so far.

    The `neighbors_func` parameter allows customizing the way neighboring points are determined. This can be
    used to change the behavior of the function to handle different types of grids or different rules for moving
    from one point to another.
    """
    visited = set()
    visualisation = []
    stack = [(start, 0, visited)]
    longest = 0
    while stack:
        (r, c), length, visited = stack.pop()
        if (r, c) == end:
            if length > longest:
                visualisation = visited | {start, end}
                p("Possible longest:", length)
                longest = length
            continue
        for loc in neighbors_func(grid, r, c):
            if loc not in visited:
                stack.append((loc, length + 1, visited | {loc}))
    if debug:
        visualize(grid, visualisation)
    return longest


def part_1(source: str | list[str]) -> int | None:
    grid, start, goal = parse(source)
    answer = dfs_longest_path(grid, start, goal, neighbors_func=get_sloped_neighbors, debug=False)
    pyperclip.copy(str(answer))
    return answer


def part_2_to_slow(source: str | list[str]) -> int | None:
    """Left it here for reference as the thought was good but the implementation was too slow."""
    grid, start, goal = parse(source)
    answer = dfs_longest_path(grid, start, goal, neighbors_func=get_non_sloped_neighbors)
    pyperclip.copy(str(answer))
    return answer


def part_2(source: str | list[str]) -> int | None:
    """Ahh again with the brute force problem
    My first solution wil work but in days rather than seconds :-)
    so what can I optimize. Memoization is the first thing that comes to mind.
    - did that still not fast enough
    - I think I need to use a* here (with Manhattan distance as heuristic)
    - dit that and still not fast enough
    - hmm what can I do to speed this up?
    - looking at the grid I see many single direction paths. I think I can use that to speed things up.
    - how to distinguish between single direction paths and multi direction paths?
    - I think I need to use the neighbors function to determine that.
    - as long as we have only 1 direction choice it is a single path
    - as long as we can move in 2 directions it is still single path but one with a corner
    - as long as we have 3 or 4 directions it is a multi path. This seems significant.
    - can I pre process the grid with this in mind?
    - what if I preprocess and find all the places in the grid where I can go in 3 or more directions?
    - then process the link these points in a graph and then use that graph to find the longest path?
      - between these points it should be a single path with a length right?
      - if I take the seen into account and we can not go back...
    - but How do I do that.
    - first find these three plus points... see if that work :-) this is fun
    - ok i have that so now I need to find the longest path between these points ?! graph?
    - yes I think it should be that. the observation that we mostly don;t have a choice in where to go
      unless it is a crossroads of 3 or more paths demands it. we can reduce the number of paths to consider by quite a
      bit this way.
    - no I have to relearn how to do the graph thing again...
    - I have a graph implementation in ivonet package so I guess I will use that.
    - yeah! it works just fine but still takes about 60 seconds to complete! which is a major
      improvement over the hours it took the first time :-)

    NOTE: it takes about 60 seconds!
    """
    long_walk = LongWalk(source)
    answer = long_walk.dfs()
    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(94, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(2178, part_1(self.source))

    def test_example_data_part_2_slow(self) -> None:
        self.assertEqual(154, part_2_to_slow(self.test_source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(154, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(6486, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
#
# crossroads: [(0, 1), (22, 21), (3, 11), (5, 3), (11, 21), (13, 5), (13, 13), (19, 13), (19, 19)]
# graph: {(0, 1): {(5, 3): 15}, (22, 21): {(19, 19): 5}, (3, 11): {(11, 21): 30, (5, 3): 22, (13, 13): 24}, (5, 3): {(3, 11): 22, (13, 5): 22, (0, 1): 15}, (11, 21): {(13, 13): 18, (19, 19): 10, (3, 11): 30}, (13, 5): {(13, 13): 12, (19, 13): 38, (5, 3): 22}, (13, 13): {(11, 21): 18, (13, 5): 12, (19, 13): 10, (3, 11): 24}, (19, 13): {(19, 19): 10, (13, 5): 38, (13, 13): 10}, (19, 19): {(19, 13): 10, (22, 21): 5, (11, 21): 10}}
# path: [(0, 1), (5, 3), (3, 11), (11, 21), (13, 13), (13, 5), (19, 13), (19, 19), (22, 21)]
# start: (0, 1) -> np: (5, 3) = 15 -> answer: 15
# start: (5, 3) -> np: (3, 11) = 22 -> answer: 37
# start: (3, 11) -> np: (11, 21) = 30 -> answer: 67
# start: (11, 21) -> np: (13, 13) = 18 -> answer: 85
# start: (13, 13) -> np: (13, 5) = 12 -> answer: 97
# start: (13, 5) -> np: (19, 13) = 38 -> answer: 135
# start: (19, 13) -> np: (19, 19) = 10 -> answer: 145
# start: (19, 19) -> np: (22, 21) = 5 -> answer: 150
# answer: 150
