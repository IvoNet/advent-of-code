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

import pyperclip

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
    return [HailStone(*ints(line)) for line in source]


class HailStone:
    px: int
    py: int
    pz: int
    vx: int
    vy: int
    vz: int

    def __init__(self, px, py, pz, vx, vy, vz):
        self.px = px
        self.py = py
        self.pz = pz
        self.vx = vx
        self.vy = vy
        self.vz = vz

    def loc(self):
        return self.px, self.py, self.pz

    @staticmethod
    def determinant(a: tuple[int, int], b: tuple[int, int]) -> int:
        """
        Calculates the determinant of a 2x2 matrix (gotten from internet somewhere)..

        The determinant of a 2x2 matrix [[a, b], [c, d]] is calculated as a * d - b * c.

        Args:
            a (tuple): The first row of the matrix.
            b (tuple): The second row of the matrix.

        Returns:
            int: The determinant of the matrix.
        """
        return a[0] * b[1] - a[1] * b[0]

    def intersection_2d(self, other: HailStone):
        """
        There’s a nice approach to this problem that uses vector cross products.
        Define the 2-dimensional vector cross product v × w to be vx * wy − vy * wx.

        https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
        distilled from the stackoverflow answers ^^

        :return: None if parallel or intersect in a past or (x, y) of intersection
        """
        if not isinstance(other, HailStone):
            return None

        xdiff = (self.px - (self.px + self.vx), other.px - (other.px + other.vx))
        ydiff = (self.py - (self.py + self.vy), other.py - (other.py + other.vy))

        # Calculate the determinant of the differences
        div = self.determinant(xdiff, ydiff)

        # If the determinant is zero, the paths are parallel
        if div == 0:
            return None

        # Calculate the determinant of the positions of the two hailstones
        determinant = (
            self.determinant((self.px, self.py), (self.px + self.vx, self.py + self.vy)),
            self.determinant((other.px, other.py), (other.px + other.vx, other.py + other.vy))
        )

        # Calculate the x and y coordinates of the intersection point
        x = self.determinant(determinant, xdiff) / div
        y = self.determinant(determinant, ydiff) / div

        return x, y

    def intersection_in_direction_2d(self, other: HailStone):
        """
        Only return intersections that are in the direction of the velocity vector from the current position.

        :return: None if parallel or intersect in a past or (x, y) of intersection
        """

        def in_direction(coordinate, velocity, intersection_coordinate: float):
            """
            Checks if the intersection coordinate is in the direction of the velocity from the current coordinate.
            convenience method to make the code more readable.

            Args:
                coordinate (int): The current coordinate (x or y) of the hailstone.
                velocity (int): The velocity (vx or vy) of the hailstone.
                intersection_coordinate (int): The intersection coordinate (x or y) of the intersection point.

            Returns:
                bool: True if the intersection coordinate is in the direction of the velocity, False otherwise.
            """
            return (velocity < 0 and intersection_coordinate > coordinate
                    or
                    velocity > 0 and intersection_coordinate < coordinate)

        intersection = self.intersection_2d(other)
        if intersection is None:
            return None

        xi, yi = intersection
        # check if intersection is in the direction of the velocity
        # all should be in the same direction otherwise they are either
        # parallel or in the past
        for i, hailstone in enumerate((self, other)):
            if (in_direction(hailstone.px, hailstone.vx, xi)
                    or in_direction(hailstone.py, hailstone.vy, yi)):
                return None
        return intersection

    def with_adjusted_velocity(self, ax: int, ay: int, az: int) -> HailStone:
        """
        Adjusts the velocity of the hailstone by subtracting the provided acceleration
        values from the current velocity.

        This method creates a new HailStone instance with the adjusted velocities and
        returns it, leaving the original instance unchanged.

        In the context of the problem being solved, the adjust method is used to calculate
        the new velocities of the hailstones after applying a certain acceleration. This is
        done in the process of finding a common intersection point for all hailstones in a 3D space.

        Returns:
            HailStone: A new HailStone instance with the adjusted velocities.
        """
        vx = self.vx - ax
        vy = self.vy - ay
        vz = self.vz - az
        return HailStone(self.px, self.py, self.pz, vx, vy, vz)

    def get_time(self, x: int, y: int):
        """
       Calculates the time it would take for the hailstone to reach a given point in the XY plane.

       The method uses the current position and velocity of the hailstone to calculate the time.
       It first checks if the velocity in the X direction is not zero. If it's not, it calculates
       the time as the difference between the X coordinate of the point and the current X position
       of the hailstone, divided by the X velocity.

       If the X velocity is zero, it does the same calculation using the Y coordinates and the Y velocity.

       If both the X and Y velocities are zero, the method raises a ValueError, as it's not possible
       to calculate the time in this case. (should not happen in this problem)

       Returns:
           float: The time it would take for the hailstone to reach the point.

       Raises:
           ValueError: If both the X and Y velocities are zero.
       """
        if self.vx != 0:
            return (x - self.px) / self.vx
        if self.vy != 0:
            return (y - self.py) / self.vy
        raise ValueError("Hailstone has zero velocity in both X and Y directions. Not expected.")

    def z_acceleration(self, other: HailStone, intersection: tuple[int, int]) -> float | None:
        """
        Calculates the Z acceleration that would make two hailstones intersect at the same point in 3D space.

        This method compares the Z coordinate at the intersection point for the first hailstone with another hailstone.
        It first calculates the time it would take for each hailstone to reach the intersection point in the XY plane.
        If the times are equal, it means that the hailstones intersect at the same Z coordinate, and the method
        returns `None`.
        If the times are not equal, the method calculates the Z acceleration as the difference in the Z coordinates
        of the hailstones plus the difference in the Z velocities of the hailstones, divided by the difference in time.

        Args:
            other (HailStone): Another hailstone.
            intersection (tuple): The X and Y coordinates of the intersection point.

        Returns:
            float | None: The Z acceleration if the hailstones intersect at different Z coordinates, otherwise None.
        """
        time_self = self.get_time(*intersection)
        time_other = other.get_time(*intersection)
        if time_self == time_other:  # hailstones intersect at the same Z coordinate
            return None
        return (self.pz - other.pz + time_self * self.vz - time_other * other.vz) / (time_self - time_other)

    def __repr__(self):
        return f"HailStone(location({self.px}, {self.py}, {self.pz}), velocity({self.vx:>3}, {self.vy:>3}, {self.vz:>3}))"

    def __str__(self):
        return self.__repr__()


def find_stone(hailstones: list[HailStone], times: int = 1000, samples: int = 3) -> int | None:
    """
    This method is used to find the right acceleration for a stationary object (a stone)
    to intersect with all the hailstones at the same point in space.

    The method takes two arguments: `hailstones` which is a list of hailstone objects and
    `times` which is the maximum number of iterations the method will try to find a solution.

    The method starts a loop that will run for a maximum of `times` iterations. This is to
    prevent an infinite loop in case a solution cannot be found.

    For each iteration, it generates all possible combinations of acceleration values for X and Y (aX and aY).
    The range of these values is determined by the variable `counter`, which is incremented in each iteration of the outer
    loop.

    For each combination of aX and aY, the method adjusts the velocity of each hailstone by subtracting
    the current acceleration from the hailstone's velocity.

    The method then checks if all hailstones intersect at a common point in the XY plane. This is done by
    comparing the intersection point of the first hailstone with a sample number of other hailstones (brute force).
    If these sampled hailstones intersect at the same point, the method proceeds to the next step.
    If not, it continues with the next combination of aX and aY.

    If a common intersection point in the XY plane is found, the method calculates the Z acceleration (aZ)
    that would make all hailstones intersect at the same point in 3D space. This is done by comparing the Z
    coordinate at the intersection point for the first hailstone with the sample number other hailstones.
    If the sampled hailstones intersect at the same Z coordinate, the method has found a solution.
    It now only has to calculate the Z acceleration. The Z
    The method continues this process until it finds a solution or exhausts all possible combinations of aX and aY.
    If a solution is found, it returns the sum of the X, Y, and Z coordinates of the intersection point.
    If no solution is found after `times` iterations, it returns `None`.

    NOTE:
    Yes I had quite a bit of help from internet to get this one solved. I am not a mathematician...
    Thanks FatalisticFeline for your awesome explanation on reddit.
    I understand it right now but don't ask me in two days :-) this was really hard and I could not have
    done it without the help of the internet. I am not ashamed to admit it. I have like 25+ tabs open explaining
    stuff to me :-) and it took my almost the whole day.

    Args:
        hailstones (list): A list of HailStone objects.
        times (int, optional): The maximum number of iterations to try to find a solution. Defaults to 1000.
        samples (int, optional): The number of hailstones to consider for finding a common intersection.

    Returns:
        int | None: The sum of the X, Y, and Z coordinates of the intersection point if a solution is found,
        otherwise None.
    """
    for counter in range(times):  # arbitrary tries to not go into endless loop
        for x in range(counter + 1):  # all possible acceleration values for x and y
            y = counter - x
            for flipper_x in (-1, 1):  # negative and positive acceleration for x
                for flipper_y in (-1, 1):  # negative and positive acceleration for y
                    acceleration_x: int = x * flipper_x
                    acceleration_y: int = y * flipper_y
                    # p(f"checking v=<{acceleration_x},{acceleration_y},?>")
                    # A copy of the first hailstone is used as a reference point
                    left_hailstone: HailStone = hailstones[0].with_adjusted_velocity(acceleration_x, acceleration_y, 0)
                    intersection: tuple[int, int] | None = None
                    right_hailstone: HailStone
                    for right_hailstone in hailstones[1:samples + 1]:
                        # A copy of the another hailstone is adjusted by the acceleration values
                        # to test if it intersects with the first hailstone.
                        right_hailstone = right_hailstone.with_adjusted_velocity(acceleration_x, acceleration_y, 0)
                        # p(f"comparing v {right_hailstone}")
                        intersection = left_hailstone.intersection_in_direction_2d(right_hailstone)
                        if not intersection:
                            break
                    if intersection is None:
                        continue
                    p(f"{counter:<3}potential common intersection v=<{acceleration_x},{acceleration_y},?>, p=<{intersection[0]},{intersection[1]},?>")
                    acceleration_z = None
                    potential_acceleration = None
                    for right_hailstone in hailstones[1:samples + 1]:
                        # As I use copies of the hailstones, I need to adjust the acceleration again in the new loop
                        # my left reference point is still the same. I forgot to do this, and it took me a while to
                        # figure out why I was not getting the right answer.
                        right_hailstone = right_hailstone.with_adjusted_velocity(acceleration_x, acceleration_y, 0)

                        potential_acceleration = left_hailstone.z_acceleration(right_hailstone, intersection)
                        if not potential_acceleration:
                            break
                        if not acceleration_z:
                            acceleration_z = potential_acceleration
                            continue
                        if potential_acceleration != acceleration_z:
                            break
                    if not potential_acceleration or potential_acceleration != acceleration_z:
                        continue
                    p(f"found intersection: {intersection} at try {counter}.")
                    stone_x, stone_y = intersection
                    stone_z = (  # calculate the z coordinate of the intersection point: z = z0 + t * vz
                            left_hailstone.pz +
                            left_hailstone.get_time(*intersection) *
                            (left_hailstone.vz - acceleration_z)
                    )
                    return int(stone_x + stone_y + stone_z)
    return None


def part_1(source: list[str], low: int = 200000000000000, high: int = 400000000000000) -> int | None:
    """
    When I thought of implementing a Hailstone class and giving it the correct behavior part 1 was actually
    pretty ok to solve. I still had to google for the correct formula to calculate the intersection of two,
    but that is allowed :-)
    """
    hailstones = parse(source)

    answer = 0
    for i in range(len(hailstones)):
        for j in range(i + 1, len(hailstones)):
            hailstone = hailstones[i]
            hailstone2 = hailstones[j]
            intersects = hailstone.intersection_in_direction_2d(hailstone2)
            p(f"{hailstone} / {hailstone2}->", end=" ")
            if intersects:
                if low <= intersects[0] <= high and low <= intersects[1] <= high:
                    p(f"{intersects}")
                    answer += 1
                else:
                    p(f"outside {intersects}")
            else:
                p(f"in past or parallel or: {hailstone.intersection_2d(hailstone2)}")
    pyperclip.copy(str(answer))
    return answer


def part_2(source: list[str]) -> int | None:
    """
    - hmm this is a really tough one. I have no idea how to solve this. I am not a mathematician.
      some googling tells me that this is a 3D problem and that I need to solve it with
      linear algebra. I know soo much more now :-)
    - more research... Too many variables to solve for my taste, I need to find a way to reduce them.
    - can I let all Hailstones move and let my rock stand still? Then I  need to find
      the right acceleration for the rock to intersect with all the Hailstones. or something ...
    - after hours and hours on the internet and yes getting some hints from reddit I was able to construct
      a pure python solution that works.
    - it is a sort of brute force solution and I reduced the number of hailstones to check against assuming if I
      find a common intersection for 3 hailstones it will be the same for all of them.
    - as I "cheated" with part 2 I waited for my company competitor to solve it and I only submitted my solution
      after he did. fair is fair :-)
    """
    hailstones = parse(source)
    answer = find_stone(hailstones)
    pyperclip.copy(str(answer))
    return answer


def part_2_2(source: list[str]) -> int | None:
    """
    solution from internet (thanks hyper-neutrino) with 3rd party tool sympy
    (against my personal rules but for learning's sake)
    """
    import sympy

    hailstones = [ints(line) for line in source]

    xr, yr, zr, vxr, vyr, vzr = sympy.symbols("xr, yr, zr, vxr, vyr, vzr")

    equations = []

    answers: list[dict] = []
    for i, (sx, sy, sz, vx, vy, vz) in enumerate(hailstones):
        equations.append((xr - sx) * (vy - vyr) - (yr - sy) * (vx - vxr))
        equations.append((yr - sy) * (vz - vzr) - (zr - sz) * (vy - vyr))
        if i < 2:
            continue
        answers = [soln for soln in sympy.solve(equations) if all(x % 1 == 0 for x in soln.values())]
        if len(answers) == 1:
            break
    if answers:
        answer = answers[0]
        return answer[xr] + answer[yr] + answer[zr]
    raise ValueError("No solution found")


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(2, part_1(self.test_source, low=7, high=27))

    def test_part_1(self) -> None:
        self.assertEqual(16779, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(47, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(871983857253169, part_2(self.source))

    def test_part_2_2(self) -> None:
        self.assertEqual(871983857253169, part_2_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
