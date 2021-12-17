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
    px += tx
    py += ty
    tx += -1 if tx > 0 else 1
    ty -= 1
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


def trace(area, position, trajectory):
    print(f"start[{position}], trajectory[{trajectory}]")
    if area_contains(area, position):
        print("Hit!")
        return
    if beyond_area(area, position):
        print("Fail!")
        return
    position, trajectory = step(position, trajectory)
    return trace(area, position, trajectory)


def part_1(source):  # 6,9
    target = target_area(source)
    top_left, bottom_right = target
    current = (0, 0)
    best = (0, 0)
    highest = (0, 0)
    total_steps = 0
    for x in range(0, bottom_right[0] + 1):
        for y in range(1000, -1000, -1):
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
                    print(f"start[{current}], position[{position}], steps[{steps}], highest[{hpoint}]")
                    if hpoint[1] > highest[1]:
                        highest = hpoint
                        best = (x, y)
                        total_steps = steps
                        # print(hpoint, end=' ')
                        break

    print()
    print(total_steps, highest, best, current)
    return highest[1]


def part_2(source):
    target = target_area(source)
    top_left, bottom_right = target
    # trace(target, (0, 0), (7, 2))
    good_list = []
    good_start_velocities = set()
    for x in range(0, bottom_right[0] + 1):
        for y in range(bottom_right[1] - 1, 1000):
            current = (x, y)
            position = (0, 0)
            trajectory = (x, y)
            while not beyond_area(target, position):
                position, trajectory = step(position, trajectory)
                if area_contains(target, position):
                    good_start_velocities.add(current)
                    good_list.append(current)

    print(good_start_velocities, good_list)
    print(len(good_start_velocities), len(good_list))
    return good_start_velocities


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = ints(Path(__file__).name)[0]
        self.source = read_data(f"day_{day}.txt")
        self.test_source = read_data("""target area: x=20..30, y=-10..-5""")
        self.test_coordinates = (
            (23, -10), (25, -9), (27, -5), (29, -6), (22, -6), (21, -7), (9, 0), (27, -7), (24, -5),
            (25, -7), (26, -6), (25, -5), (6, 8), (11, -2), (20, -5), (29, -10), (6, 3), (28, -7),
            (8, 0), (30, -6), (29, -8), (20, -10), (6, 7), (6, 4), (6, 1), (14, -4), (21, -6),
            (26, -10), (7, -1), (7, 7), (8, -1), (21, -9), (6, 2), (20, -7), (30, -10), (14, -3),
            (20, -8), (13, -2), (7, 3), (28, -8), (29, -9), (15, -3), (22, -5), (26, -8), (25, -8),
            (25, -6), (15, -4), (9, -2), (15, -2), (12, -2), (28, -9), (12, -3), (24, -6), (23, -7),
            (25, -10), (7, 8), (11, -3), (26, -7), (7, 1), (23, -9), (6, 0), (22, -10), (27, -6),
            (8, 1), (22, -8), (13, -4), (7, 6), (28, -6), (11, -4), (12, -4), (26, -9), (7, 4),
            (24, -10), (23, -8), (30, -8), (7, 0), (9, -1), (10, -1), (26, -5), (22, -9), (6, 5),
            (7, 5), (23, -6), (28, -10), (10, -2), (11, -1), (20, -9), (14, -2), (29, -7), (13, -3),
            (23, -5), (24, -8), (27, -9), (30, -7), (28, -5), (21, -10), (7, 9), (6, 6), (21, -5),
            (27, -10), (7, 2), (30, -9), (21, -8), (22, -7), (24, -9), (20, -6), (6, 9), (29, -5),
            (8, -2), (27, -8), (30, -5), (24, -7),
        )

    def test_example_data_part_1(self):
        self.assertEqual(45, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(4186, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(sorted(self.test_coordinates), sorted(part_2(self.test_source)))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
