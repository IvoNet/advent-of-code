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

DEBUG = False


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
            "AND": lambda left, right: left & right,
            "OR": lambda left, right: left | right,
            "LSHIFT": lambda left, right: left << right,
            "RSHIFT": lambda left, right: left >> right,
            "NOT": lambda right: ~right & 0xFFFF
        }
        self.__init()

    def __init(self):
        for line in self.source:
            v, k = line.split(" -> ")
            value = v.split()
            self.instructions[k] = value

    def override(self, key, value) -> self:
        """Builder like function to override a cached item
        it returns self so that chaining of commands is possible
        """
        self.cache[key] = value
        return self

    def evaluate(self, item):
        """Evaluate recursively until breaking time or solving time"""
        if item in self.cache:
            return self.cache[item]

        try:
            return int(item)
        except ValueError:
            pass

        to_solve = self.instructions[item]

        if len(to_solve) == 1:  # integer value
            result = self.evaluate(to_solve[0])
        elif len(to_solve) == 2:  # NOT operator
            op, right = to_solve
            result = self.operator_functions[op](self.evaluate(right))
        else:  # expression
            left, op, right = to_solve
            result = self.operator_functions[op](self.evaluate(left), self.evaluate(right))
        self.cache[item] = result
        _(self.cache)
        return result


def part_1(source):
    return Interpreter(source).evaluate("a")


def part_2(source):
    return Interpreter(source).override("b", part_1(source)).evaluate("a")


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}.input")))
        self.test_source = read_rows("""123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i""")

    def test_example_data_part_1(self):
        self.assertEqual(72, Interpreter(self.test_source).evaluate("d"))
        self.assertEqual(507, Interpreter(self.test_source).evaluate("e"))
        self.assertEqual(492, Interpreter(self.test_source).evaluate("f"))
        self.assertEqual(114, Interpreter(self.test_source).evaluate("g"))
        self.assertEqual(65412, Interpreter(self.test_source).evaluate("h"))
        self.assertEqual(65079, Interpreter(self.test_source).evaluate("i"))
        self.assertEqual(123, Interpreter(self.test_source).evaluate("x"))
        self.assertEqual(456, Interpreter(self.test_source).evaluate("y"))

    def test_part_1(self):
        self.assertEqual(956, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(40149, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
