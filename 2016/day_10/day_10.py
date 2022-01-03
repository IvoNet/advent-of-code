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
from ivonet.iter import ints, sort_dict_on_values

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def process(source):
    output = defaultdict(list)
    bots = defaultdict(list)
    for value, bot in [ints(x) for x in source if "value" in x]:
        bots[bot].append(value)
    _(bots)
    source = [x for x in source if "value" not in x]
    while len(source) > 0:
        for bot, values in sort_dict_on_values(bots, key=lambda x: len(x[1]), reverse=True).items():
            if len(values) < 2:
                continue
            instruction = [x for x in source if x.startswith(f"bot {bot}")]
            source = [x for x in source if not x.startswith(f"bot {bot}")]
            assert len(instruction) == 1
            instruction = instruction[0]
            bot, low, high = ints(instruction)
            items = instruction.split()
            assert items[5] in ["bot", "output"]
            assert items[-2] in ["bot", "output"]
            if items[5] == "bot":
                bots[low].append(min(values))
            elif items[5] == "output":
                output[low].append(min(values))
            if items[-2] == "bot":
                bots[high].append(max(values))
            elif items[-2] == "output":
                output[high].append(max(values))
            bots[bot] = []
            _(instruction)
            _("!!", bots)
            _(source)
            _(output)


class Instructions(NamedTuple):
    low: tuple
    high: tuple


class Factory:

    def __init__(self, source) -> None:
        self.source = source
        self.stack = []
        self.instructions = {}
        self.outputs = {}
        self.bots = defaultdict(list)
        self.__initialize()

    def __initialize(self):
        for items in [x.split() for x in self.source]:
            if items[0] == "value":
                bot = int(items[-1])
                self.bots[bot].append(int(items[1]))
                if len(self.bots[bot]) == 2:
                    self.stack.append(bot)
            else:
                bot = int(items[1])
                low = (items[5], int(items[6]))
                high = (items[-2], int(items[-1]))
                self.instructions[bot] = Instructions(low, high)

    def go(self, version=1):
        while self.stack:
            bot = self.stack.pop()
            instruction = self.instructions[bot]
            low = min(self.bots[bot])
            high = max(self.bots[bot])
            _(low, high)
            if version == 1 and high == 61 and low == 17:
                return bot
            if instruction.low[0] == "bot":
                self.bots[instruction.low[1]].append(low)
                if len(self.bots[instruction.low[1]]) == 2:
                    self.stack.append(instruction.low[1])
            else:
                self.outputs[instruction.low[1]] = low
            if instruction.high[0] == "bot":
                self.bots[instruction.high[1]].append(high)
                if len(self.bots[instruction.high[1]]) == 2:
                    self.stack.append(instruction.high[1])
            else:
                self.outputs[instruction.high[1]] = low
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
