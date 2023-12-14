#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2022 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
If a part of the code is not part of the post it is probably 
code I found reusable and I may have moved it to my 'ivonet' library.
you can find that here: https://github.com/IvoNet/advent-of-code/tree/master/ivonet
"""

import os
import sys
import unittest
from pathlib import Path

from ivonet.files import read_rows
from ivonet.grid import Location, DIRECTIONS, manhattan_distance
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def move_tail(head, tail):
    """Moves the tail so that it stays in touch with the head across or diagonally.
    - no move is done if it is already touching the head or if the head is at the same location as the tail
    - if the head is at a different location than the tail, the tail will move in the direction of the head if it is not
      touching
    $#######  H = head; 1..9 are tail positions when having to move diagonally
    ###9#1##  1) and 2) need to move SW; 3) and 4) NW; 5) and 6) NE; 7) and 8) SE to stay in touch with the head
    ##8###2#  a bit of calculation, and you get what is represented under manhattan_distance == 3
    ####H###
    ##6###3#
    ###5#4##
    ########
    """
    if manhattan_distance(head)(tail) <= 1:  # tail is touching the head or at the same location
        return tail
    if manhattan_distance(head)(tail) == 2:  # if we need to follow on same row or col or touch the head diagonally
        if head.col == tail.col:
            if head.row > tail.row:
                return tail + DIRECTIONS["S"]
            return tail + DIRECTIONS["N"]
        if head.row == tail.row:
            if head.col > tail.col:
                return tail + DIRECTIONS["E"]
            return tail + DIRECTIONS["W"]
        return tail
    if manhattan_distance(head)(tail) == 3:  # tail needs to move towards head diagonally
        if (head - tail) in [Location(-1, 2), Location(-2, 1)]:
            return tail + DIRECTIONS["NE"]
        if (head - tail) in [Location(-2, -1), Location(-1, -2)]:
            return tail + DIRECTIONS["NW"]
        if (head - tail) in [Location(1, -2), Location(2, -1)]:
            return tail + DIRECTIONS["SW"]
        if (head - tail) in [Location(2, 1), Location(1, 2)]:
            return tail + DIRECTIONS["SE"]
    if manhattan_distance(head)(tail) == 4:  # head has moved diagonally so we must follow diagonally
        if (head - tail) == Location(-2, 2):
            return tail + DIRECTIONS["NE"]
        if (head - tail) == Location(-2, -2):
            return tail + DIRECTIONS["NW"]
        if (head - tail) == Location(2, -2):
            return tail + DIRECTIONS["SW"]
        if (head - tail) == Location(2, 2):
            return tail + DIRECTIONS["SE"]
    raise ValueError(f"Illegal distance {manhattan_distance(head)(tail)}, {head}, {tail}")


def walk(compass_direction: str, head: Location, knots: list[Location]):
    """Walks the head and the knots in the given direction
    :param compass_direction: the direction to walk (N, E, S, W)
    :param head: the head Location
    :param knots: the list of knots without the head
    """
    head += DIRECTIONS[compass_direction]
    h = head
    new_knots = []
    for knot in knots:
        tail = move_tail(h, knot)
        new_knots.append(h := tail)
    _(head, new_knots)
    return head, new_knots


def planckify(source: list[str], knot_size: int = 2):
    """Planckify the source.
    Walk the head according to the source and let the knots follow the head.
    The last knot is the tail
    :param source: the source to planckify
    :param knot_size: the number of knots that are used in the rope
    """
    tail_visited: [Location] = []
    head: Location = Location(0, 0)
    knots = [Location(0, 0) for __ in range(knot_size - 1)]
    for line in source:
        uplr, distance = line[0], int(line[2:])
        if uplr == "R":
            for __ in range(distance):
                head, knots = walk("E", head, knots)
                tail_visited.append(knots[-1])
        elif uplr == "L":
            for __ in range(distance):
                head, knots = walk("W", head, knots)
                tail_visited.append(knots[-1])
        elif uplr == "U":
            for __ in range(distance):
                head, knots = walk("N", head, knots)
                tail_visited.append(knots[-1])
        elif uplr == "D":
            for __ in range(distance):
                head, knots = walk("S", head, knots)
                tail_visited.append(knots[-1])
        else:
            raise ValueError(f"Unknown direction {uplr}")

    return len(set(tail_visited))


def part_1(source):
    return planckify(source, 2)


def part_2(source):
    return planckify(source, 10)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2""")
        self.test_source2 = read_rows("""R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20""")

    def test_example_data_part_1(self):
        self.assertEqual(13, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(5619, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(1, part_2(self.test_source))
        self.assertEqual(36, part_2(self.test_source2))

    def test_part_2(self):
        self.assertEqual(2376, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
