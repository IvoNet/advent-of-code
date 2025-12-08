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
from pathlib import Path

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


def parse(source):
    gates = {}
    formulae = {}
    for line in source:
        if ": " in line:
            left, right = line.split(": ")
            gates[left] = int(right)
            continue
        if "->" in line:
            left, op, right, result = line.replace(" -> ", " ").split()
            formulae[result] = (op, left, right)
    return gates, formulae


class MonitoringDevice:
    OPERATORS = {
        "OR": lambda x, y: x | y,
        "AND": lambda x, y: x & y,
        "XOR": lambda x, y: x ^ y,
    }

    def __init__(self, source):
        self.gates, self.formulae = parse(source)
        self.memory = {}
        self.bits = []

    def calc(self, wire):
        if wire in self.gates:
            return self.gates[wire]
        op, left, right = self.formulae[wire]
        self.gates[wire] = self.OPERATORS[op](self.calc(left), self.calc(right))
        return self.gates[wire]

    def part_1(self, tries=1000):
        for i in range(tries):
            key = f"z{i:02}"
            if key not in self.formulae:
                p(f"not found {key}")
                break
            self.bits.append(self.calc(key))
        p(self.bits)
        return int("".join(map(str, self.bits[::-1])), 2)


@debug
@timer
def part_1(source) -> int | None:
    md = MonitoringDevice(source)
    answer = md.part_1()

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

    def test_operartors(self):
        md = MonitoringDevice([])
        self.assertEqual(1, md.OPERATORS["OR"](1, 0))
        self.assertEqual(1, md.OPERATORS["OR"](1, 1))
        self.assertEqual(0, md.OPERATORS["AND"](1, 0))
        self.assertEqual(1, md.OPERATORS["AND"](1, 1))
        self.assertEqual(1, md.OPERATORS["XOR"](1, 0))
        self.assertEqual(0, md.OPERATORS["XOR"](1, 1))

    def test_example_data_part_1(self) -> None:
        self.assertEqual(4, part_1(self.test_source))

    def test_example_data_part_1_a(self) -> None:
        self.assertEqual(2024, part_1(self.test_source_1))

    def test_part_1(self) -> None:
        self.assertEqual(47666458872582, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(None, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = Path(__file__).resolve().parent
        day = f"{ints(Path(__file__).stem)[0]:02}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")
        self.test_source_1 = read_rows(f"{folder}/test_{day}_1.input")


if __name__ == '__main__':
    unittest.main()
