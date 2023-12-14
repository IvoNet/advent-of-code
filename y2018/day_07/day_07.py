#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
Thought to solve this one as a 'Constraint-satisfaction Problem' but could not get it to work
still think is should be possible.... 
"""

import os
import re
import sys
import unittest
from itertools import count
from nis import cat
from pathlib import Path

from ivonet import infinite
from ivonet.files import read_rows
from ivonet.iter import ints, multimap, quantify, flatten
from ivonet.str import cat

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def parse_instruction(line):
    return re.findall(' ([A-Z]) ', line)


def order(pairs):
    """Yield steps in order, respecting (before, after) pairs; break ties lexically."""
    steps = {*flatten(pairs)}
    constraints = multimap((A, B) for [B, A] in pairs)

    def ready(step):
        return all(pre not in steps for pre in constraints[step])

    while steps:
        step = min(filter(ready, steps))
        steps.remove(step)
        yield step


def schedule(pairs, workers=5, seconds=60):
    """Create a schedule map with times based on the step_time and number of workers
    Flow:

    """
    steps = {*flatten(pairs)}
    constraints = multimap((b, a) for a, b in pairs)
    end_time = {step: infinite for step in steps}
    for spend in count(1):
        def ready(step, ts=spend):
            return all(end_time[p] < ts for p in constraints[step])

        available = list(filter(ready, steps))
        for step in sorted(available)[:workers]:
            end_time[step] = spend + seconds + ord(step) - ord('A')
            steps.remove(step)
            workers -= 1
        # Discover if any workers become free this time step
        workers += quantify(end_time[step] == spend for step in end_time)
        # Return answer once all steps have been scheduled
        if not steps:
            return end_time


def part_1(source):
    constrains = {tuple(parse_instruction(line)) for line in source}
    return cat(order(constrains))


def part_2(source, workers=5, seconds=60):
    steps = {tuple(parse_instruction(line)) for line in source}
    result_schedule = schedule(steps, workers=workers, seconds=seconds)
    _(result_schedule)
    return max(result_schedule.values())


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.""")

    def test_example_data_part_1(self):
        self.assertEqual("CABDFE", part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual("OUGLTKDJVBRMIXSACWYPEQNHZF", part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(15, part_2(self.test_source, workers=2, seconds=0))

    def test_part_2(self):
        self.assertEqual(929, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
