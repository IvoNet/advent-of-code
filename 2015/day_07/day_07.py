#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Interpreter:

    def __init__(self, source) -> None:
        self.source = source
        self.instructions = {}
        self.cache = {}
        self.operator_functions = {
            "AND": lambda left, right: int(left) & int(right),
            "OR": lambda left, right: int(left) | int(right),
            "LSHIFT": lambda left, right: (int(left) << int(right)) & 0xFFFF,
            "RSHIFT": lambda left, right: (int(left) >> int(right)) & 0xFFFF,
            "NOT": lambda right: ~right & 0xFFFF
        }
        self.__init()

    def evaluate(self, item):
        if item in self.cache:
            return self.cache[item]

        try:
            return int(item)
        except ValueError:
            pass

        todo = self.instructions[item]
        if len(todo) == 1:  # integer value
            result = self.evaluate(todo[0])
        elif len(todo) == 2:  # NOT operator
            op, right = todo
            result = self.operator_functions[op](self.evaluate(right))
        else:  # expression
            left, op, right = todo
            result = self.operator_functions[op](self.evaluate(left), self.evaluate(right))
        self.cache[item] = result
        return result

    def __init(self):
        for line in self.source:
            v, k = line.split(" -> ")
            value = v.split()
            self.instructions[k] = value


def part_1(source):
    part1 = Interpreter(source).evaluate("a")
    return part1


def indent_print(cmd):
    ind = 0
    inds = "  "
    prev = ""
    for i, c in enumerate(cmd):
        if c in "()":
            prev = c
            if c == "(":
                print(f"\n{inds * ind}{c}", end="")
                ind += 1
            if c == ")":
                ind -= 1
                print(f"\n{inds * ind}{c}", end="")
            if ind < 0:
                ind = 0
        else:
            if prev == "(":
                print(f"\n{inds * ind}{c}", end="")
                prev = ""
            else:
                print(f"{c}", end="")


def part_2(source):
    return 0


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"day_{day.zfill(2)}.input")
        self.test_source = read_rows("""123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i""")

    def test_example_data_part_1(self):
        self.assertEqual(None, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(None, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
