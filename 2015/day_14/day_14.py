#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

from ivonet.files import read_rows
from ivonet.iter import ints, sort_dict_on_values

sys.dont_write_bytecode = True

DEBUG = False
first_debug_print = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    global first_debug_print
    if DEBUG:
        if first_debug_print:
            first_debug_print = False
            print()
        print(" ".join(str(x) for x in args), end=end)


class Fly(NamedTuple):
    speed: int
    duration: int
    rest: int


def parse(source):
    ret = {}
    for line in source:
        fly = Fly(*ints(line))
        reindeer = line.split()[0]
        ret[reindeer] = fly
    return ret


def travel(fly: Fly, duration=2503) -> int:
    _(fly)
    cycle = fly.duration + fly.rest
    runs = duration // cycle
    leftover = duration % cycle
    ret = runs * fly.duration * fly.speed
    ret += min(leftover, fly.duration) * fly.speed
    _(runs, leftover)
    return ret


def part_1(source, duration=2503):
    reindeer = parse(source)
    dist = {}
    for r in reindeer:
        dist[r] = travel(reindeer[r], duration=duration)
    _(dist)
    return max(dist.values())


def part_2(source, duration=2503):
    reindeer = parse(source)
    score = defaultdict(int)
    for sec in range(1, duration + 1):
        interim_core = {}
        for r, fly in reindeer.items():
            interim_core[r] = travel(fly, duration=sec)
        interim_core = sort_dict_on_values(interim_core, reverse=True)
        high_score = -1
        first = True
        for key, value in interim_core.items():
            if first:
                first = False
                high_score = value
            if value == high_score:
                score[key] += 1
            else:
                break

    return max(score.values())


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"day_{day.zfill(2)}.input")
        self.test_source = read_rows("""Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.""")

    def test_example_data_part_1(self):
        self.assertEqual(1120, part_1(self.test_source, duration=1000))

    def test_part_1(self):
        self.assertEqual(2640, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(689, part_2(self.test_source, duration=1000))

    def test_part_2(self):
        self.assertEqual(1102, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
