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
import unittest
from pathlib import Path
from typing import NamedTuple

import pyperclip
import sys
from ivonet.decorators import debug
from ivonet.decorators import timer
from ivonet.files import read_rows
from ivonet.iter import ints

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


NUMERIC_KEYPAD = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [" ", "0", "A"]  # gap, 0, Activate
]

DIRECTIONAL_KEYPAD = [
    [" ", "^", "A"],  # gap, Up Activate
    ["<", "v", ">"],  # Left, Down, Right
]


def get_key(pad, p1):
    r, c = p1
    if not (0 <= r < len(pad) and 0 <= c < len(pad[r])):
        return None
    if pad[r][c] == ' ':
        return None
    return pad[r][c]


def get_numeric_key(key):
    return get_key(NUMERIC_KEYPAD, key)


def get_direction_key(key):
    return get_key(DIRECTIONAL_KEYPAD, key)


def apply_pad(pad, p, move):
    r, c = p
    if move == 'A':
        return (r, c), get_key(pad, p)
    if move == '<':
        return (r, c - 1), None
    if move == '^':
        return (r - 1, c), None
    if move == '>':
        return (r, c + 1), None
    if move == 'v':
        return (r + 1, c), None


def apply_numerical_keypad(p, move):
    return apply_pad(NUMERIC_KEYPAD, p, move)


def apply_directional_pad(p, move):
    return apply_pad(DIRECTIONAL_KEYPAD, p, move)


def loc(pad, key):
    for r, row in enumerate(pad):
        for c, col in enumerate(row):
            if col == key:
                return r, c
    return None


def get_numeric_loc(key):
    return loc(NUMERIC_KEYPAD, key)


def get_direction_loc(key):
    return loc(DIRECTIONAL_KEYPAD, key)


class VisitedKey(NamedTuple):
    direction: str
    previous_direction: str
    robots: int


class BFSKey(NamedTuple):
    distance: int
    start: tuple[int, int]
    end: str
    out: str
    path: str


class Cost(NamedTuple):
    distance: int
    start: str
    end: str


class RendeerClassStarship:

    def __init__(self, source, robots=2):
        self.source = source
        self.memory = {}
        self.robots = robots
        self.directions = "^<v>A"
        self.start_positions = {key: get_direction_loc(key) for key in
                                self.directions}  # cheaper than calling get_direction_loc every time

    def bfs(self, code):
        start = BFSKey(0, get_numeric_loc("A"), 'A', '', '')
        queue = []
        heapq.heappush(queue, start)
        visited = {}
        while queue:
            bk = heapq.heappop(queue)
            if bk.out == code:
                return bk.distance
            if not code.startswith(bk.out):
                continue
            if get_numeric_key(bk.start) is None:
                continue
            key = VisitedKey(bk.start, bk.end, bk.out)
            if key in visited:
                continue
            visited[key] = bk.distance
            for move in self.directions:
                new_out = bk.out
                new_start, output = apply_numerical_keypad(bk.start, move)
                if output is not None:
                    new_out = bk.out + output
                cost_move = self.extra_robots_cost(move, bk.end, self.robots)
                heapq.heappush(queue, BFSKey(bk.distance + cost_move, new_start, move, new_out, bk.path))

    def extra_robots_cost(self, direction, previous_direction, robots):
        key = (direction, previous_direction, robots)
        if key in self.memory:
            return self.memory[key]
        if robots == 0:
            return 1
        else:
            queue = []
            start_pos = self.start_positions[previous_direction]
            heapq.heappush(queue, [0, start_pos, 'A', '', ''])
            visited = {}
            while queue:
                d, p, prev, out, path = heapq.heappop(queue)
                if get_direction_key(p) is None:
                    continue
                if out == direction:
                    self.memory[key] = d
                    return d
                elif len(out) > 0:
                    continue
                seen_key = (p, prev)
                if seen_key in visited:
                    continue
                visited[seen_key] = d
                for move in self.directions:
                    new_p, output = apply_directional_pad(p, move)
                    cost_move = self.extra_robots_cost(move, prev, robots - 1)
                    new_d = d + cost_move  # len(cost_move)
                    new_out = out
                    if output is not None:
                        new_out = new_out + output
                    heapq.heappush(queue, [new_d, new_p, move, new_out, path])

    def process(self):
        answer = 0
        for line in self.source:
            sol = self.bfs(line)
            answer += sol * ints(line)[0]
        return answer


@debug
@timer
def part_1(source) -> int | None:
    rcs = RendeerClassStarship(source, 2)
    answer = rcs.process()
    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:
    rcs = RendeerClassStarship(source, 25)
    answer = rcs.process()
    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(126384, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(215374, part_1(self.source))

    def test_part_2(self) -> None:
        self.assertEqual(260586897262600, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = Path(__file__).resolve().parent
        day = f"{ints(Path(__file__).stem)[0]:02}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
