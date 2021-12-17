#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
--- Day 17: Trick Shot ---
You finally decode the Elves' message. HI, the message says. 
You continue searching for the sleigh keys.

Ahead of you is what appears to be a large ocean trench. Could the keys 
have fallen into it? You'd better send a probe to investigate.

The probe launcher on your submarine can fire the probe with any integer 
velocity in the x (forward) and y (upward, or downward if negative) 
directions. For example, an initial x,y velocity like 0,10 would fire 
the probe straight up, while an initial velocity like 10,-1 would fire
 the probe forward at a slight downward angle.

The probe's x,y position starts at 0,0. Then, it will follow some 
trajectory by moving in steps. On each step, these changes occur in the following order:

- The probe's x position increases by its x velocity.
- The probe's y position increases by its y velocity.
- Due to drag, the probe's x velocity changes by 1 toward the value 0; 
  that is, it decreases by 1 if it is greater than 0, increases by 1 if it 
  is less than 0, or does not change if it is already 0.
- Due to gravity, the probe's y velocity decreases by 1.

For the probe to successfully make it into the trench, the probe must be on 
some trajectory that causes it to be within a target area after any step. The 
submarine computer has already calculated this target area (your puzzle input). 

For example:

target area: x=20..30, y=-10..-5

This target area means that you need to find initial x,y velocity values such that
after any step, the probe's x position is at least 20 and at most 30, and the 
probe's y position is at least -10 and at most -5.

Given this target area, one initial velocity that causes the probe to 
be within the target area after any step is 7,2:

.............#....#............
.......#..............#........
...............................
S........................#.....
...............................
...............................
...........................#...
...............................
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTT#TT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT

In this diagram, S is the probe's initial position, 0,0. The x coordinate 
increases to the right, and the y coordinate increases upward. In the bottom 
right, positions that are within the target area are shown as T. After 
each step (until the target area is reached), the position of the probe 
is marked with #. (The bottom-right # is both a position the probe 
reaches and a position in the target area.)

Another initial velocity that causes the probe to be within the 
target area after any step is 6,3:

...............#..#............
...........#........#..........
...............................
......#..............#.........
...............................
...............................
S....................#.........
...............................
...............................
...............................
.....................#.........
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................T#TTTTTTTTT
....................TTTTTTTTTTT

Another one is 9,0:

S........#.....................
.................#.............
...............................
........................#......
...............................
....................TTTTTTTTTTT
....................TTTTTTTTTT#
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT

One initial velocity that doesn't cause the probe to be within the 
target area after any step is 17,-4:

S..............................................................
...............................................................
...............................................................
...............................................................
.................#.............................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT..#.............................
....................TTTTTTTTTTT................................
...............................................................
...............................................................
...............................................................
...............................................................
................................................#..............
...............................................................
...............................................................
...............................................................
...............................................................
...............................................................
...............................................................
..............................................................#

The probe appears to pass through the target area, but is never within it
after any step. Instead, it continues down and to the right - only the 
first few steps are shown.

If you're going to fire a highly scientific probe out of a super cool 
probe launcher, you might as well do it with style. How high can you 
make the probe go while still reaching the target area?

In the above example, using an initial velocity of 6,9 is the best you 
can do, causing the probe to reach a maximum y position of 45. 
(Any higher initial y velocity causes the probe to overshoot the 
target area entirely.)

Find the initial velocity that causes the probe to reach the highest 
y position and still eventually be within the target area after 
any step. What is the highest y position it reaches on this trajectory?
"""

import sys
import unittest
from pathlib import Path

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True


def step(position: tuple[int, int], trajectory: tuple[int, int]) -> tuple[tuple[int, int], tuple[int, int]]:
    px, py = position
    tx, ty = trajectory
    tx += -1 if tx > 0 else 1
    ty -= 1
    px += tx
    py += ty
    return (px, py), (tx, ty)


def target_area(s: str) -> tuple[tuple[int, int], tuple[int, int]]:
    sx, ex, sy, ey = ints(s)
    return (sx, ey), (ex, sy)


def area_contains(area: tuple[tuple[int, int], tuple[int, int]], point: tuple[int, int]) -> bool:
    top_left, bottom_right = area
    tx, ty = top_left
    bx, by = bottom_right
    px, py = point
    return tx <= px <= bx and by <= py <= ty  # <= because boundary is inclusive


def beyond_area(area: tuple[tuple[int, int], tuple[int, int]], point: tuple[int, int]) -> bool:
    top_left, bottom_right = area
    # tx, ty = top_left
    bx, by = bottom_right
    px, py = point
    return px > bx or py < by


def part_1(source):  # 6,9
    target = target_area(source)
    current = (0, 0)
    best = (0, 0)
    highest = (0, 0)
    total_steps = 0
    for x in range(0, 1000):
        for y in range(0, 1000):
            current = (x, y)
            steps = 0
            hpoint = (0, 0)
            position = (0, 0)
            trajectory = (x, y)
            while not beyond_area(target, position):
                position, trajectory = step(position, trajectory)
                if position[1] > hpoint[1]:
                    hpoint = position
                steps += 1
                # print(steps, position)
                if area_contains(target, position):
                    if hpoint[1] > highest[1]:
                        highest = hpoint
                        best = (x, y)
                        total_steps = steps
                        break

    print(total_steps, highest, best, current)
    # print(target)
    # print(area_contains(target, (20, -5)))
    # print(beyond_area(target, (30, -11)))
    return total_steps


def part_2(source):
    return 0


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = ints(Path(__file__).name)[0]
        self.source = read_data(f"day_{day}.txt")
        self.test_source = read_data("""target area: x=20..30, y=-10..-5""")

    def test_example_data_part_1(self):
        self.assertEqual(45, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(None, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
