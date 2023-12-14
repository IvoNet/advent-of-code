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
from pathlib import Path

from ivonet.cdll import CircularDoublyLinkedList
from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def part_1(source):
    """Just having fun with my circular doubly linked list
    - make the input into a cdll and then walk the walk
    - added a convenience method walk the length of a cycle once
      by asking cdll if it is done.
    - as we walk until done we also check if the last matches
      the first
    """
    cdll = CircularDoublyLinkedList()
    cdll.extend(int(x) for x in source)
    total = 0
    while not cdll.done():
        if cdll.current().data == cdll.next().data:
            # Note that this current is not the same as the
            # current in the if statement but the "next" :-)
            total += cdll.current().data
    return total


def part_2(source):
    """Get the opposite node without updateding the internal
    current node status and walk both walks until done
    """
    cdll = CircularDoublyLinkedList()
    cdll.extend(int(x) for x in source)
    total = 0
    opposite = cdll.node(len(cdll) // 2, update_current=False)
    current = cdll.current()
    while not cdll.done():
        if current.data == opposite.data:
            total += current.data
        opposite = opposite.next
        current = cdll.next()
    return total


def part_1a(source):
    """sum occurrences as long as the next is the same
    the modulo function is a nice way to wrap the last around to the first
    """
    return sum(int(source[i]) for i in range(len(source)) if source[i] == source[(i + 1) % len(source)])


def part_2a(source):
    return sum(int(source[i]) for i in range(len(source)) if source[i] == source[(i + len(source) // 2) % len(source)])


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")

    def test_part_testdata_1(self):
        self.assertEqual(3, part_1("1122"))

    def test_part_testdata_2(self):
        self.assertEqual(4, part_1("1111"))

    def test_part_testdata_3(self):
        self.assertEqual(0, part_1("1234"))

    def test_part_testdata_4(self):
        self.assertEqual(9, part_1("91212129"))

    def test_part_1(self):
        self.assertEqual(1069, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(1268, part_2(self.source))

    def test_part_1a(self):
        self.assertEqual(1069, part_1a(self.source))

    def test_part_2a(self):
        self.assertEqual(1268, part_2a(self.source))


if __name__ == '__main__':
    unittest.main()
