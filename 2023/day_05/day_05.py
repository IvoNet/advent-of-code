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

import os
import sys
import unittest
from collections import defaultdict
from pathlib import Path

from ivonet import infinite
from ivonet.files import read_rows
from ivonet.iter import ints, lmap

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


class Almanac(object):

    def __init__(self, source):
        super().__init__()
        self.start = "seed"
        self.seeds = []
        self.ranges = defaultdict(list)
        self.lines = self.parse_input(source)

    def find(self, ranges, num):
        res = infinite
        for dst, src, length in ranges:
            if src <= num < src + length:
                res = num - src + dst
        return res if res != infinite else num

    def parse_input(self, source):
        for line in source:
            if line.startswith("seeds:"):
                self.seeds = lmap(int, line.split(": ")[1].split())
                continue
            if "map:" in line:
                src, dst = line.split(" ")[0].split("-to-")
                continue
            if line.strip():
                self.ranges[src, dst].append(lmap(int, line.split(' ')))

    def convert(self, source, number):
        return self.maps[source].get(number, number)

    def find_min_location(self):
        result = infinite
        txt = ""
        for seed in self.seeds:
            txt += f"Seed {seed:3d} "
            soil = self.find(self.ranges['seed', 'soil'], seed)
            txt += f"-> Soil {soil:3d} "
            fertilizer = self.find(self.ranges['soil', 'fertilizer'], soil)
            txt += f"-> Fertilizer {fertilizer:3d} "
            water = self.find(self.ranges['fertilizer', 'water'], fertilizer)
            txt += f"-> Water {water:3d} "
            light = self.find(self.ranges['water', 'light'], water)
            txt += f"-> Light {light:3d} "
            temperature = self.find(self.ranges['light', 'temperature'], light)
            txt += f"-> Temperature {temperature:3d} "
            humidity = self.find(self.ranges['temperature', 'humidity'], temperature)
            txt += f"-> Humidity {humidity:3d} "
            location = self.find(self.ranges['humidity', 'location'], humidity)
            txt += f"-> Location {location:3d} "
            result = min(result, location)
            txt += f"-> Result {result:3d} "
            _(txt)
            txt = ""
        return result


def part_1(source):
    almanac = Almanac(source)
    return almanac.find_min_location()


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""")
        self.test_source2 = read_rows("""""")

    def test_example_data_part_1(self):
        self.assertEqual(35, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(None, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
