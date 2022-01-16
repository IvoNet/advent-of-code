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

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def process(source):
    chonological = sorted(source, key=lambda x: (x[6:8], x[9:11], x[12:14], x[15:17]))
    sleep = defaultdict(lambda: defaultdict(list))  # sleep[guard][day] = [minute,...]
    guard = None
    falls = None
    for line in chonological:
        _(line)
        numbers = ints(line)
        day = "-".join(str(x) for x in numbers[:3])
        if "Guard" in line:
            guard = numbers[-1]
            falls = None
        elif "falls" in line:
            falls = numbers[4]
        elif "wakes" in line:
            wakes = numbers[4]
            assert falls is not None, line
            sleep[guard][day].extend(range(falls, wakes))
            falls = None
    return sleep


def sleepiest_guard(sleep):
    """The guard with the most minutes asleep"""
    return max(sleep, key=lambda guard: sum(map(len, sleep[guard].values())))


def sleepiest_minute(guard, sleep):
    """Which minute is he asleep the most often"""

    def times_asleep(minute):
        """Counts the number of times this guard is asleep on a specific minute"""
        return sum(minute in minutes for minutes in sleep[guard].values())

    return max(range(60), key=times_asleep)


def part_1(source):
    sleep = process(source)
    guard = sleepiest_guard(sleep)
    minute = sleepiest_minute(guard, sleep)
    _(guard, minute)
    return guard * minute


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up""")

    def test_example_data_part_1(self):
        self.assertEqual(240, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(3212, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
