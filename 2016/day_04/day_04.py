#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


@dataclass
class Room:
    name: str
    sector: int
    checksum: list

    def valid(self) -> bool:
        code = sorted(self.name)
        groups = Counter(code).most_common(5)
        left = [x[0] for x in groups]
        _(left, self.checksum, left == self.checksum)
        return left == self.checksum


def prepare(source):
    ret = []
    for line in source:
        d = line.split("-")
        room = "".join(d[:-1])
        sector = ints(d[-1])[0]
        checksum = d[-1].split("[")[1][:-1]
        ret.append(Room(room, sector, list(checksum)))
    return ret


def part_1(source):
    potentials = prepare(source)
    return sum(room.sector for room in potentials if room.valid())


def part_2(source):
    return 0


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"day_{day.zfill(2)}.input")

    def test_example_data_1_part_1(self):
        self.assertEqual(123, part_1(read_rows("aaaaa-bbb-z-y-x-123[abxyz]")))

    def test_example_data_2_part_1(self):
        self.assertEqual(987, part_1(read_rows("a-b-c-d-e-f-g-h-987[abcde]")))

    def test_example_data_3_part_1(self):
        self.assertEqual(404, part_1(read_rows("not-a-real-room-404[oarel]")))

    def test_part_1(self):
        self.assertEqual(158835, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
