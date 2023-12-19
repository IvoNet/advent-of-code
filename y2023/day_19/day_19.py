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

from ivonet.files import read_data
from ivonet.iter import ints

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


class Aplenty:

    def __init__(self, source: str, start="in"):
        self.operator_functions = {
            ">": lambda left, right: left > right,
            "<": lambda left, right: left < right,
        }
        self.parts = []
        self.rulez = collections.defaultdict(list)
        self.start = start
        self.result = collections.defaultdict(list)
        self._parse(source)

    def _parse(self, source):
        flow, state = source.split("\n\n")
        for line in flow.strip().splitlines():
            ins = line.replace("{", " ").replace("}", "").replace(",", " ").split()
            name = ins[0]
            rest = ins[1:]
            for i in rest:
                ia = i.split(":")
                if len(ia) == 1:
                    self.rulez[name].append(ia[0])
                else:
                    left, operator, right = ia[0][0], ia[0][1], int(ia[0][2:])
                    self.rulez[name].append((left, operator, right, ia[1]))
        p(self.rulez)
        for line in state.strip().splitlines():
            x, m, a, s = ints(line)
            self.parts.append({"x": x, "m": m, "a": a, "s": s})
        p(self.parts)

    def process(self):
        for part in self.parts:
            flow = self.rulez[self.start]
            idx = 0
            while flow:
                ins = flow[idx]
                idx += 1
                if isinstance(ins, str):
                    if ins in self.rulez:
                        flow = self.rulez[ins]
                        idx = 0
                        continue
                    self.result[ins].append(part)
                    break
                else:
                    left, operator, right, goto = ins
                    if self.operator_functions[operator](part[left], right):
                        if goto in self.rulez:
                            flow = self.rulez[goto]
                            idx = 0
                            continue
                        self.result[goto].append(part)
                        break
        return sum(sum(x.values()) for x in self.result["A"])

    def count(self, ranges, name=None):
        """
        Calculate the total number of acceptable combinations of values for the variables x, m, a, and s
        that satisfy the rules defined in the rulez attribute of the class.

        Parameters:
        ranges (dict): A dictionary where the keys are the variable names (x, m, a, s) and the values
                       are tuples representing the range of acceptable values for each variable.
        name (str): A string representing the current rule being processed. Default is self.start.

        Returns:
        int: The total number of acceptable combinations.
        """
        if not name:
            name = self.start

        # terminator 1: if name is not in the rulez then it is a terminator and when R rejected so 0
        if name == "R":
            return 0
        # terminator 2: if name is A then we have a winner
        if name == "A":
            # we need to return all the accepted
            product = 1
            for lo, hi in ranges.values():
                product *= hi - lo + 1  # one off inclusive
            return product

        rules = self.rulez[name][:-1]  # last one is the fallback
        fallback = self.rulez[name][-1]

        total = 0
        for left, operator, right, target in rules:
            lo, hi = ranges[left]  # start with the current range
            if operator == "<":
                # because the operator is not inclusive -1 is needed and yes I did this wrong the first time
                true_range = (lo, right - 1)
                false_range = (right, hi)
            else:  # operator == ">":
                true_range = (right + 1, hi)
                false_range = (lo, right)

            if true_range[0] <= true_range[1]:
                # send the true range to the next rule (workflow)
                total += self.count({**ranges, left: true_range}, target)
            if false_range[0] <= false_range[1]:
                # actually changes the ranges by first copying it and then adding the new range
                ranges = {**ranges, left: false_range}
            else:
                break
        else:
            # if we get here we have not broken out of the loop, and thus we have a fallback
            total += self.count(ranges, fallback)

        return total

    def acceptable_combinations(self):
        """Only the first block of the data is used for this (flow)"""
        return self.count({key: (1, 4000) for key in ["x", "m", "a", "s"]})

def part_1(source: str | list[str]) -> int | None:
    aplenty = Aplenty(source)
    return aplenty.process()


def part_2(source: str | list[str]) -> int | None:
    aplenty = Aplenty(source)
    return aplenty.acceptable_combinations()


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(19114, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(376008, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(167409079868000, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(124078207789312, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_data(f"{folder}/day_{day}.input")
        self.test_source = read_data(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
