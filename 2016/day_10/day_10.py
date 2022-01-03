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
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class SubInstruction(NamedTuple):
    type: str
    bot: int


class Instructions(NamedTuple):
    low: SubInstruction
    high: SubInstruction


class Factory:

    def __init__(self, source) -> None:
        self.source = source
        self.stack = []
        self.instructions = {}
        self.outputs = {}
        self.bots = defaultdict(list)
        self.__initialize()
        _(self.stack)

    def __initialize(self):
        """Parse the source into usable data

        """
        for items in [x.split() for x in self.source]:
            if items[0] == "value":
                bot = int(items[-1])
                self.bots[bot].append(int(items[1]))
                if len(self.bots[bot]) == 2:
                    self.stack.append(bot)
            else:
                bot = int(items[1])
                low = SubInstruction(items[5], int(items[6]))
                high = SubInstruction(items[-2], int(items[-1]))
                self.instructions[bot] = Instructions(low, high)

    def go(self, version=1) -> int:
        while self.stack:
            _(self.stack)
            bot = self.stack.pop()
            _(bot)
            instruction = self.instructions[bot]
            low = min(self.bots[bot])
            high = max(self.bots[bot])
            if version == 1 and high == 61 and low == 17:
                return bot
            if instruction.low.type == "bot":
                self.bots[instruction.low.bot].append(low)
                if len(self.bots[instruction.low.bot]) == 2:
                    self.stack.append(instruction.low.bot)
            else:
                self.outputs[instruction.low.bot] = low
            if instruction.high.type == "bot":
                self.bots[instruction.high.bot].append(high)
                if len(self.bots[instruction.high.bot]) == 2:
                    self.stack.append(instruction.high.bot)
            else:
                self.outputs[instruction.high.bot] = low
            self.bots[bot] = []
            if version == 2 and 0 in self.outputs and 1 in self.outputs and 2 in self.outputs:
                return self.outputs[0] * self.outputs[1] * self.outputs[2]
        raise ValueError("Should never reach this moment")


def part_1(source):
    return Factory(source).go(1)


def part_2(source):
    return Factory(source).go(2)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")

    def test_part_1(self):
        self.assertEqual(157, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(1085, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
