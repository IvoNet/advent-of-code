#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import re
import sys
import unittest
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from ivonet.caesar import caesar_cipher
from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


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
        code = sorted([x for x in self.name if x != "-"])
        groups = Counter(code).most_common(5)
        left = [x[0] for x in groups]
        _(left, self.checksum, left == list(self.checksum))
        return left == list(self.checksum)

    def decode(self):
        return " ".join([caesar_cipher(x, self.sector) for x in self.name.split("-")]).strip()


def prepare(source):
    ret = []
    for room in source:
        match = re.match("([^\d]+)(\d+)\[(\w+)\]", room)
        groups = match.groups(0)
        ret.append(Room(groups[0], int(groups[1]), groups[2]))
    return ret


def part_1(source):
    potentials = prepare(source)
    return sum(room.sector for room in potentials if room.valid())


def part_2(source):
    potentials = prepare(source)
    _(potentials)
    for room in potentials:
        if room.valid():
            _(room.decode(), room.sector)
            if "northpole object storage" in room.decode():
                return room.sector
    return -1


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}.input")))

    def test_example_data_1_part_1(self):
        self.assertEqual(123, part_1(read_rows("aaaaa-bbb-z-y-x-123[abxyz]")))

    def test_example_data_2_part_1(self):
        self.assertEqual(987, part_1(read_rows("a-b-c-d-e-f-g-h-987[abcde]")))

    def test_example_data_3_part_1(self):
        self.assertEqual(404, part_1(read_rows("not-a-real-room-404[oarel]")))

    def test_part_1(self):
        self.assertEqual(158835, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual("very encrypted name",
                         Room(name='qzmt-zixmtkozy-ivhz-', sector=343, checksum='zimth').decode())

    def test_part_2(self):
        self.assertEqual(993, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
