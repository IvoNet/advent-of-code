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

from ivonet.decorators import debug
from ivonet.decorators import timer
from ivonet.files import read_rows
from ivonet.iter import ints, rangei

PART_2_ADD = 10000000000000

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def parse(source):
    i = 0
    machines = []
    for line in source:
        i += 1
        if i == 1:
            ax, ay = ints(line)
        if i == 2:
            bx, by = ints(line)
        if i == 3:
            px, py = ints(line)
        if i == 4:
            machines.append((ax, ay, bx, by, px, py))
            ax, ay, bx, by, px, py = 0, 0, 0, 0, 0, 0
        i %= 4
    if ax and ay and bx and by and px and py:
        machines.append((ax, ay, bx, by, px, py))

    return machines


def first_try_working_but_to_slow_for_part2(machines):
    answer = 0
    for ax, ay, bx, by, px, py in machines:
        stop = False
        for ai in rangei(1, 100):
            for bi in rangei(1, 100):
                axi = ax * ai
                ayi = ay * ai
                bxi = bx * bi
                byi = by * bi
                if axi + bxi == px and ayi + byi == py:
                    tokens = ai * 3 + bi * 1
                    answer += tokens
                    p("Found solution for", ax, ay, bx, by, px, py, "tokens", tokens)
                    stop = True
                if stop:
                    break
            if stop:
                break
        if not stop:
            p("No solution found for", ax, ay, bx, by, px, py)
    return answer


def calc_tokens(ax, ay, bx, by, px, py):
    """
    https://www.mathcentre.ac.uk/resources/uploaded/mc-ty-strtlines-2009-1.pdf
    https://stackoverflow.com/questions/8954326/how-to-calculate-the-mirror-point-along-a-line

    So we need to optimize the way we calculate the tokens as the brute force method is way to slow.
    This looks like some kind of linear equation system so let's try to solve it that way.
    The linear equations to determine if two points starting from (0,0) and walking (ax, ay) and (bx, by)
    can reach a point p at (px, py) can be represented as:

    n * ax + m * bx = px
    n * ay + m * by = py

    Here, n and m are the multipliers for the steps taken by a and b respectively.
    The goal is to find integer values of n and m that satisfy both equations.

    n * ax + m * bx = px ->
    n * ax = px - m * bx ->
    n = (px - m * bx) / ax
    now we have isolated n in the first equation.
    n * ay + m * by = py ->
    n * ay = py - m * by
    n = (py - m * by) / ay
    now we have isolated n in the second equation.
    we still have m though so lets do the same for m and see where we land:
    n * ax + m * bx = px ->
    m * bx = px - n * ax ->
    m = (px - n * ax) / bx
    now we have isolated m in the first equation.
    n * ay + m * by = py ->
    m * by = py - n * ay
    m = (py - n * ay) / by
    now we have isolated m in the second equation.
    what can we do with this information?
    We can now substitute the value of n in the first equation into the second equation and vice versa.
    let's try that:
    n = (px - m * bx) / ax
    n = (py - m * by) / ay
    so:
    (px - m * bx) / ax = (py - m * by) / ay
    we can now solve this equation for m:
    (px - m * bx) / ax = (py - m * by) / ay
    (px - m * bx) = (py - m * by) * ax / ay
    move m to the left
    px - m * bx = py * ax / ay - m * by * ax / ay
    px - py * ax / ay = m * bx - m * by * ax / ay
    px - py * ax / ay = m * (bx - by * ax / ay)
    m = (px - py * ax / ay) / (bx - by * ax / ay)
    m = (px * ay - py * ax) / (bx * ay - by * ax)
    now n:
    n = (px - m * bx) / ax
    n = (py - m * by) / ay
    n = (py * bx - px * by) / (ax * by - ay * bx)
    I see a denominator:
    n = (py * bx - px * by) / (ax * by - ay * bx) ->
    n = (py * bx - px * by) / (bx * ay - by * ax)
    m = (px * ay - py * ax) / (bx * ay - by * ax)
    The last part of both equations are the same. This is the denominator.
    this means that if the denominator is zero there is no solution (divide by zero)
    if n and m are integers we have a solution.
    n steps kost 3 tokens and m steps kost 1 token.
    so the total tokens are (3 * n + m) tokens.
    I was lucky to think of the linear equation with some googling I thought it was searching in the right direction.
    took me quite a while to figure this out as I am not a mathematician.
    """
    denominator = bx * ay - by * ax
    if denominator == 0:
        return 0  # No solution if denominator is zero

    n = (py * bx - px * by) / denominator
    m = (px * ay - py * ax) / denominator

    if n.is_integer() and m.is_integer():
        return int(3 * n + m)

    return 0  # No solution found


@debug
@timer
def part_1(source) -> int | None:
    machines = parse(source)
    answer = sum([calc_tokens(ax, ay, bx, by, px, py) for ax, ay, bx, by, px, py in machines])
    # answer = first_try_working_but_to_slow_for_part2(machines)

    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:
    answer = 0
    machines = parse(source)
    for ax, ay, bx, by, px, py in machines:
        px += PART_2_ADD
        py += PART_2_ADD
        answer += calc_tokens(ax, ay, bx, by, px, py)
    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(480, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(30413, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(875318608908, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(92827349540204, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
