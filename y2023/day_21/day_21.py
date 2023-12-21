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
from typing import Callable, Sequence

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


def quadratic_sequence(seq: Sequence[int]) -> Callable:
    """
    Returns a function that calculates the value of the quadratic sequence for the given list of integers
    :param seq:
    :return:
    """
    diff1 = [b - a for a, b in zip(seq, seq[1:])]  # first differences
    diff2 = [b - a for a, b in zip(diff1, diff1[1:])]  # second differences
    # test if it is a quadratic sequence
    if len(set(diff2)) == 1:  # all second differences should be the same in a quadratic sequence
        a = diff2[0] // 2  # 2a = 2nd diff
        b = diff1[0] - 3 * a  # 3a + b = u2 - u1 = 1st diff
        c = seq[0] - a - b  # a + b + c = u1
        return lambda n: quadratic_formula(a, b, c, n)
    else:
        raise ValueError("Not a quadratic sequence")


def quadratic_formula(a, b, c, n):
    """
    Returns the value of the quadratic formula for the given parameters.

    Un = an^2 + bn + c
    """
    return a * n ** 2 + b * n + c


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


def bfs(start, grid, max_steps, invalid=None) -> int:
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


def try_sequence(grid, start, samples=6, odd=True):
    """
    Try to find the quadratic sequence for the given grid and start position.
    This is done by performing a BFS for the given number of samples and then
    calculating the quadratic sequence for the odd or even samples.
    """
    answers_odd = []
    answers_even = []
    offset = len(grid) // 2
    width = len(grid)
    for i in range(0, samples):
        s = offset + width * i
        answer = bfs(start, grid, s, unbounded_invalid_test)
        if s % 2 == 1:
            answers_odd.append(answer)
        else:
            answers_even.append(answer)
    return quadratic_sequence(answers_odd) if odd else quadratic_sequence(answers_even)


def part_1(source: str | list[str], steps=64, invalid=bounded_invalid_test) -> int | None:
    start, grid = parse(source)
    return bfs(start, grid, steps, invalid)


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
    - 26501365 % 262 = 65
    - 26501365 = 202300 * 131 + 65 => 101150 * 2 * 131 + 65 => 101151 * 2 * 131
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
      even : 3676,90974,294408,613978,1049684,1601526  -> 2(29034 * n ** 2 - 43453 * n + 16257)
      odds: 32808,178174,439676,817314,1311088,1920998 -> 2(29034 * n ** 2 - 43453 * n + 16257)
    - so the pattern is 2 (16257 - 43453 n + 29034 n^2), n= steps // (131 *2) + 1
      ANSWER>>> https://www.wolframalpha.com/input?i=2+%2816257+-+43453+n+%2B+29034+n%5E2%29%2C+n%3D%28floor%2826501365+%2F+262%29+%2B+1%29
    - I've tried al combinations and yes I had to wait minutes before I could enter a new answer
    - I've got the second star but I don't understand it. Wolfram Alpha is my friend here
    - I just found patterns and applied the formula and it worked after a lot of one offs and trials.
    - I really want to understand this!
    - going to look at solutions now from others
    - for reference and learning I will commit this code as is
    - I chose the odds formula as the steps was an odd number (tried the other one also :-))
    - I am pretty sure this solution is for my input only and not a general solution!
    -======== Now for Generalisation... =====
    - research tells me that this is a quadratic sequence and the formula for that is always -> an^2 + bn + c
    - I want to generify this solution so it works for all inputs
    - I need to prove that the pattern is actually a quadratic sequence
    - because of the former observations I know that the shortest path to the edge of the grid is 65 steps as there
      are no obstacles in the way
    - so that is my offset. I need to bfs a couple of samples to get the possible quadratic sequence
      (which I did earlier but now with understanding :-)
    - either on 0 + x * 131 or 65 + x * 131 lets try both...--> 65 it is after I tried both
    - look at this site to understand my equations better:
      https://www.radfordmathematics.com/algebra/sequences-series/difference-method-sequences/quadratic-sequences.html
    - first we have to recognise there is a quadratic sequence:
    - given sequence:    3676     90974     294408      613978      1049684      1601526
                            \     /   \    /     \    /     \     /       \     /
    - first differences:     872237    203434     319570       435706      551842
                                 \    /    \    /      \     /      \     /
    - Second differences:        116136    116136      116136       116136
    - so the second differences are all the same so we have a quadratic sequence -> len(set(second diffs)) == 1
    - we need to find a, b and c of the given quadratic sequence equation: an^2 + bn + c
    - in order to do that we have 3 formulas:
    - 1) 2a = 2nd diff ->  a = 1/2 * (2nd diff) = 1/2 * 116136 = 58068
    - 2) 3a + b = 1st diff = u2 - u1 -> 3a + b = 90974 - 3676 = 87298 -> b = 87298 - 3a = 87298 - 3 * 58068 = -115760
    - 3) a + b + c = 1st term = u1 -> c = 1st term - a - b = 3676 - 58068 - (-115760) = 57693
    - so the formula is: 58068 * n ** 2 - 115760 * n + 57693
    - now we can calculate the steps for my input -> see code...
    - but how do I derive what n should be in the quadratic sequence -> n = floor(steps / (131 * 2)) + 1
    - Here, steps is the total number of steps you want to take, 131 is the width of the grid, and 2 is used to
      account for both horizontal and vertical directions. The floor function is used to round down to the nearest
      whole number, and 1 is added to the result.
    - The `1` is added to the result in the formula  to adjust the term number `n` in the quadratic sequence.
    - In the context of the code, the term number `n` is calculated based on the number of steps you want to
      take. The `floor` function is used to round down to the nearest whole number. However, in a quadratic sequence,
      the term number starts from `1` (for the first term), not `0`. Therefore, `1` is added to the result of the
      floor division to correctly calculate the term number `n` in the quadratic sequence.
    - I need to do de bfs with the unbounded_invalid_test for enough steps to get to the edge of the grid and then
      get enough samples to determine the quadratic sequence and then calculate the answer
    """
    start, grid = parse(source)

    assert len(grid) == len(grid[0])  # grid is square (important)
    assert len(grid) % 2 == 1  # grid is odd (important)

    # 6 is enough to get the pattern and fast enough to still work
    # qso stands for quadratic sequence odd numbers
    qso = try_sequence(grid, start, samples=6, odd=True)
    return qso(steps // (len(grid) * 2) + 1)


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(2, part_1(self.test_source, 1))
        self.assertEqual(6, part_1(self.test_source, 3))
        self.assertEqual(16, part_1(self.test_source, 6))

    def test_part_1(self) -> None:
        self.assertEqual(3578, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        """
        It seems that the same formula can be used for both part 1 as part 2 but it is to slow for
        part 2. The only difference in the formula is the invalid test function.
        so above 1000 steps it is too slow so I needed to optimize.
        Through observation I noticed stuff and the optimizations has a couple of assumptions that does not hold true
        for the test input. I leave this here for reference and proof of my thinking process.
        """
        self.assertEqual(16, part_1(self.test_source, 6, unbounded_invalid_test))
        self.assertEqual(50, part_1(self.test_source, 10, unbounded_invalid_test))
        self.assertEqual(1594, part_1(self.test_source, 50, unbounded_invalid_test))
        self.assertEqual(6536, part_1(self.test_source, 100, unbounded_invalid_test))
        self.assertEqual(167004, part_1(self.test_source, 500, unbounded_invalid_test))
        # self.assertEqual(668697, part_1(self.test_source, 1000))
        # self.assertEqual(16733044, part_2(self.test_source, 5000))

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
