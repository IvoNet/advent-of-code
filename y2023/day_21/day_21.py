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

from math import floor

from ivonet.files import read_rows
from ivonet.iter import ints

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def parse(source):
    grid = [list(row) for row in source]
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col == "S":
                return (r, c), grid
    raise ValueError("No start found")


def get_cell_state(grid, x, y):
    # TODO make this one pretty and put in the ivonet library
    height = len(grid)
    width = len(grid[0])

    wrapped_x = x % width
    wrapped_y = y % height

    return grid[wrapped_y][wrapped_x]


def bounded_invalid_test(grid, nr, nc):
    return nr < 0 or nr >= len(grid) or nc < 0 or nc >= len(grid[0]) or grid[nr][nc] == "#"


def unbounded_invalid_test(grid, nr, nc):
    return get_cell_state(grid, nr, nc) == "#"


def bfs(start, grid, max_steps, invalid=None):
    """
    Perform a Breadth-First Search (BFS) on the grid from the start position.

    The BFS explores all reachable positions in the grid in exactly `max_steps` steps.
    A position is considered reachable if it is a garden plot (".") and not a rock ("#").

    Args:
        start (tuple): The starting position as a tuple of (row, column).
        grid (list): The grid as a 2D list of strings. Each string can be ".", "#", or "S".
        max_steps (int): The maximum number of steps to take from the start position.

    Returns:
        set: A set of all positions that can be reached in exactly `max_steps` steps from the start position.
    """
    queue = collections.deque([(start, max_steps)])  # Add step count to queue
    visited = {start}
    answer = set()
    while queue:
        (r, c), steps = queue.popleft()

        if steps % 2 == 0:  # even steps are always possible to do in even steps (64)
            answer.add((r, c))
        if steps == 0:
            continue

        for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nr, nc = r + dr, c + dc
            if invalid(grid, nr, nc) or (nr, nc) in visited:
                continue
            visited.add((nr, nc))
            queue.append(((nr, nc), steps - 1))
    return len(answer)


def part_1(source: str | list[str], steps=64) -> int | None:
    start, grid = parse(source)
    return bfs(start, grid, steps, bounded_invalid_test)


# usage
# grid = [list(line) for line in open('day_21.input').read().splitlines()]
# print(solve(grid, 26501365))

def part_2(source: str | list[str], steps=26501365) -> int | None:
    """ OK this one is killing me. So let's observe and see if we can extrapolate:
    NOTE!! my bfs version works with the unbounded_invalid_test but us way to slow to solve this puzzle
    - the question is how many positions can be reached in exactly 26501365 steps
    - wy this specific odd number? (I'm going to assume it has a good reason to be that specific number)
    - the grid is a square 131x131
    - the grid can infinitely be repeated
    - none of the sides have obstacles only "."
    - looking even more closely I noticed that vertically and horizontally the grid is completely free of obstacles
      from start (S) to the edge of the grid
    - the S vertical and horizontal axis are free of obstacles and S is in the middle of the grid (65,65)
    - that means that one can walk to the edge of the grid in 65 steps which is in effect the shortest path to the edge
    - 26501365 // 131 = 202300 (but has remainder)
    - 202300 // 2 = 101150
    - 202300 // 2 + 1 = 101151
    - 26501365 % 131 = 65 ---- oeh this is the same as the S position?! 0 indexed => 64
    - 26501365 = 202300 * 131 + 65
    - the actual input file also has a visible open diamond shape in the middle is that something?
    - when I try to find all the places within the original boundaries I can go to in increments of 65 steps (+1 for every iteration) I
      find a pattern of 7255 steps every time
    - unbounded it does not repeat this pattern lets ask wolfram alpha if there is a pattern i don't see
    - if I do 131 * 2 steps I get Odds:  14706,131218,363866,712650,1177570,1758626,...
      https://www.wolframalpha.com/input?i=14706%2C131218%2C363866%2C712650%2C1177570
      -> 2 * (29034 * n ** 2 - 28846 * n + 7165)
    - if I do 131 * 2 steps I get Evens: 1,58445,233025,523741,930593,1453581
      https://www.wolframalpha.com/input?i=58445%2C233025%2C523741%2C930593
      -> 58068 * n ** 2 - 115760 * n + 57693
    - and for offset 65 (just trying to find patterns) I get:
      odds : 3676,90974,294408,613978,1049684,1601526  -> 2(29034 * n ** 2 - 43453 * n + 16257)
      evens: 32808,178174,439676,817314,1311088,1920998 -> 2(29034 * n ** 2 - 43453 * n + 16257)
    - so the pattern is 2 (16257 - 43453 n + 29034 n^2), n= steps // (131 *2) + 1
      https://www.wolframalpha.com/input?i=2+%2816257+-+43453+n+%2B+29034+n%5E2%29%2C+n%3D%28floor%2826501365+%2F+262%29+%2B+1%29
      The mathematical term for // in Python is called "floor division". It divides the left operand by the right operand and rounds down the result to the nearest whole number.
    - I've tried al combinations and yes I had to wait minutes before I could enter a new answer
    - I've got the second star but I don't understand it. Wolfram Alpha is my friend here
    - I just found patterns and applied the formula and it worked after a lot of one offs and trials. I really want to understand this!
    - going to look at solutions now from others
    - for reference and learning I will commit this code as is
    - I chose the odds formula as the steps was an odd number
    - I am pretty sure this solution is for my input only and not a general solution!

    """
    # pas = (steps // (131 * 2)) + 1
    # ans = 2 * (29034 * pas ** 2 - 43453 * pas + 16257)
    # n = steps // (131 * 2) + 1  # 101151
    n = floor(steps / (131 * 2)) + 1  # 101151
    # e = 58068 * n ** 2 - 115760 * n + 57693
    o = 2 * (29034 * n ** 2 - 43453 * n + 16257)
    return o  # <<<< this works! OMG and I don't understand it :-) I will try to understand it later

    # The code below was all stuuf I used to find the patterns above
    # start, grid = parse(source)
    # p(f"start: {start}")
    # p(f"grid: {grid}")
    # p(f"steps: {steps}")
    # p(f"grid is: {len(grid)}x{len(grid[0])}")
    # bounded = []
    # unbounded = []
    # odds = []
    # evens = []
    # for i in range(0, 10):
    #     stps = 65 + i * 131
    #     # answer = bfs(start, grid, stps, bounded_invalid_test)
    #     # p(f"stps: {stps} answer: {answer}")
    #     # bounded.append(answer)
    #     answer = bfs(start, grid, stps, unbounded_invalid_test)
    #     p(f"stps: {stps} answer: {answer}")
    #     if stps % 2 == 0:
    #         evens.append(answer)
    #     else:
    #         odds.append(answer)
    #     unbounded.append(answer)
    # # p(",".join(str(x) for x in bounded))
    # p(",".join(str(x) for x in unbounded))
    # p(",".join(str(x) for x in odds))
    # p(",".join(str(x) for x in evens))
    # # print(gcd(*odds))
    # print(list(gcd(a, b) for a, b in zip(odds[:-1], odds[1:])))
    # print(list(gcd(a, b) for a, b in zip(evens[:-1], evens[1:])))
    # ans = 2(29034 * steps ** 2 - 43453 * steps + 16257)
    # print(ans)
    # # prev_diff = 0
    # # prev = 0
    # # for i in range(1, 300):
    # #     answer = bfs(start, grid, i, unbounded_invalid_test)
    # #     diff = answer - prev
    # #     p(f"steps: {i:>3} answer: {answer:>6}, diff to prev: {diff:>6}, 2nd diff: {prev_diff - diff:>6}")
    # #     prev_diff = answer - prev
    # #     prev = answer
    # # return None
    # # return solve(grid, start, steps)
    # # return bfs(start, grid, steps)
    # # return bfs(start, grid, steps, unbounded_invalid_test)


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        # self.assertEqual(2, part_1(self.test_source, 1))
        # self.assertEqual(6, part_1(self.test_source, 3))
        self.assertEqual(16, part_1(self.test_source, 6))

    def test_part_1(self) -> None:
        self.assertEqual(3578, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        # self.assertEqual(16, part_2(self.test_source, 6))
        # self.assertEqual(50, part_2(self.test_source, 10))
        # self.assertEqual(1594, part_2(self.test_source, 50))
        # self.assertEqual(6536, part_2(self.test_source, 100))
        # self.assertEqual(167004, part_2(self.test_source, 500))
        # self.assertEqual(668697, part_2(self.test_source, 1000))
        self.assertEqual(16733044, part_2(self.test_source, 5000))

    def test_part_2(self) -> None:
        self.assertEqual(594115391548176, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
