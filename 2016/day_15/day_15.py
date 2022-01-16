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
from dataclasses import dataclass
from itertools import count
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


@dataclass
class Disk:
    nr: int
    positions: int
    time: int
    position: int

    def slot(self, time) -> bool:
        """The slots need to be aligned at a certain moment.
        - A slot is aligned based on the offset to its first disk
        - conveniently when parsing we also parsed the disk number
        - we can use that as the offset.
        """
        return (time + self.nr + self.position) % self.positions == 0


def parse(source):
    ret = []
    for line in source:
        ret.append(Disk(*ints(line)))
    return ret


def process(disks):
    for i in count():
        if all(x.slot(i) for x in disks):
            return i


def part_1(source):
    disks = parse(source)
    return process(disks)


def part_2(source):
    disks = parse(source)
    disks.append(Disk(7, 11, 0, 0))
    return process(disks)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.""")

    def test_disk(self):
        self.assertTrue(Disk(nr=1, positions=5, time=0, position=4).slot(5))
        self.assertTrue(Disk(nr=2, positions=2, time=0, position=1).slot(5))

    def test_example_data_part_1(self):
        self.assertEqual(5, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(16824, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(3543984, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
