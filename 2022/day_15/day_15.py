#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2022 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
If a part of the code is not part of the post it is probably 
code I found reusable and I may have moved it to my 'ivonet' library.
you can find that here: https://github.com/IvoNet/advent-of-code/tree/master/ivonet
"""

import os
import sys
import unittest
from pathlib import Path

from ivonet.files import read_rows
from ivonet.grid import Location, manhattan_distance
from ivonet.iter import ints, rangei

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def part_1(source, watch_row=2000000):
    filled = set()
    beacons_watch = set()
    watch_beacon_row = set()
    for line in source:
        sensor_col, sensor_row, beacon_col, beacon_row = ints(line)
        sensor = Location(sensor_row, sensor_col)
        beacon = Location(beacon_row, beacon_col)
        if beacon.row == watch_row:
            watch_beacon_row.add(beacon.col)
        md = manhattan_distance(sensor)(beacon)
        md_threshold_distance = md - abs(watch_row - sensor.row)
        _(sensor, beacon, md, md_threshold_distance)

        for col in range(sensor.col - md_threshold_distance, sensor.col + md_threshold_distance):
            filled.add(col)

    return len(filled - beacons_watch)


def part_2(source, maximum=4000000, frequency=4000000):
    row_memory = [[] for _ in rangei(0, maximum)]
    answer_row = 0
    answer_col = 0
    for line in source:
        sensor_col, sensor_row, beacon_col, beacon_row = ints(line)
        sensor = Location(sensor_row, sensor_col)
        beacon = Location(beacon_row, beacon_col)
        md = manhattan_distance(sensor)(beacon)
        _(sensor, beacon, md)
        delta_row = 0
        while md > 0:
            col_left = max(0, sensor.col - md)
            col_right = min(maximum, sensor.col + md)
            if sensor.row - delta_row >= 0:
                row_memory[sensor.row - delta_row].append([col_left, col_right])
            if sensor.row + delta_row <= maximum and delta_row:
                row_memory[sensor.row + delta_row].append([col_left, col_right])
            delta_row += 1
            md -= 1

    for row in range(maximum + 1):
        answer_row = row
        x_coordinates = row_memory[row]
        if not x_coordinates:
            continue
        x_coordinates = sorted(x_coordinates)

        latest = x_coordinates[0][1]
        for x in range(1, len(x_coordinates)):
            if latest < x_coordinates[x][0] - 1:
                break
            latest = max(latest, x_coordinates[x][1])

        if latest != maximum:
            answer_col = latest + 1
            _("!", answer_row, answer_col)
            break
    return frequency * answer_col + answer_row


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3""")

    def test_example_data_part_1(self):
        self.assertEqual(26, part_1(self.test_source, 10))

    def test_part_1(self):
        self.assertEqual(4961647, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(56000011, part_2(self.test_source, maximum=20))

    def test_part_2(self):
        self.assertEqual(12274327017867, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
