#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """"""

import os
import sys
import unittest
from itertools import count
from pathlib import Path
from typing import Optional

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def p(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def parse(source) -> dict[[int], SecurityScanner]:
    """Deprecated
    Used in the first (old) version"""
    firewall = {}
    for line in source:
        k, v = ints(line)
        firewall[k] = SecurityScanner(v)
    return firewall


class SecurityScanner:
    """Deprecated
    Left here for learning purposes but toooo slow
    """

    def __init__(self, depth) -> None:
        self.depth = depth
        self._iterator = self.__scanner()

    def __scanner(self):
        while True:
            for i in range(self.depth - 1):
                yield i
            for i in range(self.depth - 1, 0, -1):
                yield i

    def reset(self):
        self._iterator = None
        self._iterator = self.__scanner()

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._iterator)


def move_layer(firewall, steps) -> list[Optional[int]]:
    """Deprecated"""
    state = []
    for k in range(steps):
        if fw := firewall.get(k):
            state.append(next(fw))
        else:
            state.append(None)
    return state


def firewall_cost(firewall, cost_free=False):
    """Deprecated"""
    stepst_to_take = max(firewall) + 1

    for delay in count():
        cost = 0
        for i in range(stepst_to_take):
            state = move_layer(firewall, stepst_to_take)
            delay += 1
            # p(i, state)
            if state[i] is None:
                continue
            if state[i] == 0:
                cost += i * firewall[i].depth
        if not cost_free:
            return cost
        if delay % 1000 == 0:
            print("Delay:", delay)
        if cost == 0:
            return delay - 1


def scanner(depth, time):
    """First version seems to work ut slow... (see git history) lets see if a formula can be found
    - the scanner moves up and down so twice the time to get back to 0
    - offset is something like time % depth * 2 -> can have a minus 1 thingy in there as depth is probably not 0 based
    - the depth is also twice so place in the firewall is
      2 * (depth -1) - offset or somtehing
    - lets try
    """
    corrected_depth = depth - 1
    offset = time % (corrected_depth * 2)
    return 2 * corrected_depth - offset if offset > corrected_depth else offset


def find_delay(firewall):
    """The longer more readable? version of part 2"""
    for delay in count():
        found = True
        for pos, depth in firewall:
            if scanner(depth, delay + pos) == 0:
                found = False
        if found:
            return delay


def part_1(source):
    firewall = [ints(line) for line in source]
    return sum(pos * depth for pos, depth in firewall if scanner(depth, pos) == 0)


def part_2(source, tuned_start_delay=0):
    """I have added a stuned_start_delay option for performance reasons
    Just run from 0 to do the 'real' test :-)"""
    firewall = [ints(line) for line in source]
    # return find_delay(firewall)  # second option reduced to line below to practice
    return next(delay for delay in count(tuned_start_delay) if
                not any(scanner(depth, delay + pos) == 0 for pos, depth in firewall))


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""0: 3
1: 2
4: 4
6: 4""")

    def test_example_data_part_1(self):
        self.assertEqual(24, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(2164, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(10, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(3861798, part_2(self.source, tuned_start_delay=3861700))


if __name__ == '__main__':
    unittest.main()
