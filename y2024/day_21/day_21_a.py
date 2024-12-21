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
import unittest
from collections import deque, abc, defaultdict
from pathlib import Path

import pyperclip
import sys
from ivonet.decorators import debug, memoize
from ivonet.decorators import timer
from ivonet.files import read_rows
from ivonet.iter import ints

collections.Callable = abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


@memoize
def bfs(grid, start, end):
    """Breadth First Search
    to find all the shortest paths to a given end point on the numeric pad
    it returns the paths to get there in the form of directions ><^v.
    """
    height = len(grid)
    width = len(grid[0])
    queue = deque([(start, "")])
    visited = set()
    shortest_paths = []
    shortest_length = float('inf')

    while queue:
        (row, col), path = queue.popleft()
        if (row, col) == end:
            if len(path) < shortest_length:
                shortest_length = len(path)
                shortest_paths = [path]
            elif len(path) == shortest_length:
                shortest_paths.append(path)
            continue
        for dr, dc, direction in zip([-1, 1, 0, 0], [0, 0, -1, 1], "^v<>"):
            new_row, new_col = row + dr, col + dc
            if new_row in range(height) and new_col in range(width) and grid[new_row][new_col] != " ":
                if (new_row, new_col) not in visited or len(path) + 1 <= shortest_length:
                    visited.add((new_row, new_col))
                    queue.append(((new_row, new_col), path + direction))
    return shortest_length, shortest_paths


class NumericKeyPad:
    NUMERIC_KEYPAD = [
        ["7", "8", "9"],
        ["4", "5", "6"],
        ["1", "2", "3"],
        [" ", "0", "A"]  # gap, 0, Activate
    ]

    def __init__(self):
        self.r, self.c = self.start
        self.paths = defaultdict(list)
        self.memory = {}
        self.all_paths()

    def __move(self, action):
        if action == "^":
            self.r -= 1
        elif action == "v":
            self.r += 1
        elif action == "<":
            self.c -= 1
        elif action == ">":
            self.c += 1
        elif action == "A":
            return self.NUMERIC_KEYPAD[self.r][self.c]
        return ""

    def act(self, code):
        return "".join(self.__move(c) for c in code)

    @memoize
    def loc(self, key):
        for r, row in enumerate(self.NUMERIC_KEYPAD):
            for c, col in enumerate(row):
                if col == str(key):
                    return r, c
        return None

    @property
    def start(self):
        return self.loc("A")

    def all_paths(self):
        for s in "1234567890A":
            for e in "1234567890A":
                start = self.loc(s)
                end = self.loc(e)
                length, paths = bfs(self.NUMERIC_KEYPAD, start, end)
                self.paths[(start, end)] = paths
                self.memory[(start, end)] = length

    def path(self, code):
        start = (self.r, self.c)
        mem = []
        for c in code:
            mem.append((c, self.paths[(start, self.loc(c))]))
            start = self.loc(c)
        return mem

    def generate_combinations(self, code, index, current_path, paths, results):
        if index == len(code):
            results.append(current_path)
            return

        value, possible_paths = paths[index]
        for path in possible_paths:
            self.generate_combinations(code, index + 1, current_path + path + 'A', paths, results)

    def get_all_answers(self, code):
        results = []
        self.generate_combinations(code, 0, "", self.path(code), results)
        return list(set(results))

    def directions(self, code):
        return "A".join(x[1][0] for x in self.path(code))+"A"

    def reset(self):
        self.r, self.c = self.start


class DirectionKeyPad:
    DIRECTIONAL_KEYPAD = [
        [" ", "^", "A"],  # gap, Up Activate
        ["<", "v", ">"],  # Left, Down, Right
    ]

    def __init__(self):
        self.r, self.c = self.start
        self.paths = defaultdict(list)
        self.memory = {}
        self.all_paths()

    @memoize
    def loc(self, key):
        for r, row in enumerate(self.DIRECTIONAL_KEYPAD):
            for c, col in enumerate(row):
                if col == key:
                    return r, c
        return None

    @property
    def start(self):
        return self.loc("A")

    def all_paths(self):
        for s in "^v<>A":
            for e in "^v<>A":
                start = self.loc(s)
                end = self.loc(e)
                length, paths = bfs(self.DIRECTIONAL_KEYPAD, start, end)
                self.paths[(start, end)] = paths
                self.memory[(start, end)] = length

    def __move(self, action):
        if action == "^":
            self.r -= 1
        elif action == "v":
            self.r += 1
        elif action == "<":
            self.c -= 1
        elif action == ">":
            self.c += 1
        elif action == "A":
            return self.DIRECTIONAL_KEYPAD[self.r][self.c]
        return ""

    def act(self, code):
        return "".join(self.__move(c) for c in code)

    def path(self, code):
        start = (self.r, self.c)
        mem = []
        for c in code:
            mem.append((c, self.paths[(start, self.loc(c))]))
            start = self.loc(c)
        return mem

    def generate_combinations(self, code, index, current_path, paths, results):
        if index == len(code):
            results.append(current_path)
            return

        value, possible_paths = paths[index]
        for path in possible_paths:
            self.generate_combinations(code, index + 1, current_path + path + 'A', paths, results)

    def get_all_answers(self, codes: list[str]):
        results = []
        for code in codes:
            self.generate_combinations(code, 0, "", self.path(code), results)
        # determine the shortest items in the result and only keep them
        results = set(results)
        shortest = min(len(x) for x in results)
        results = [x for x in results if len(x) == shortest]
        return results

    def directions(self, code):
        return "A".join(x[1][0] for x in self.path(code))

    def reset(self):
        self.r, self.c = self.start


@debug
@timer
def part_1(source) -> int | None:
    answer = 0
    np = NumericKeyPad()
    dp = DirectionKeyPad()
    for line in source:
        print(80 * '=')
        print(line)
        print(80 * '=')
        ret = np.get_all_answers(line)[0]
        dp.reset()
        for i in range(2):
            ret = dp.get_all_answers([ret])[0]
        print(f"Answer: {ret}, {len(ret)} * {ints(line)[0]} = {len(ret) * ints(line)[0]}")
        answer += len(ret) * ints(line)[0]
    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:
    answer = 0
    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_first_Steps(self) -> None:
        np = NumericKeyPad()
        dp = DirectionKeyPad()
        sols = {
            "029A": "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A",
            "980A": "<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A",
            "179A": "<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A",
            "456A": "<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A",
            "379A": "<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A",
        }
        for line in self.test_source:
            r1 = np.get_all_answers(line)
            r2 = dp.get_all_answers(r1)
            r3 = dp.get_all_answers(r2)
            self.assertTrue(sols[line] in r3)
            for instr in r3:
                r3 = dp.act(instr)
                r2 = dp.act(r3)
                r1 = np.act(r2)
                self.assertEqual(line, r1)

    def test_path(self) -> None:
        np = NumericKeyPad()
        dp = DirectionKeyPad()
        for line in self.test_source:
            print(80 * '=')
            print(line)
            print(80 * '=')
            code = np.directions(line)
            print(code)
            p1 = dp.directions(code)
            p2 = dp.directions(p1)
            print(p2, len(p2), line)

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
