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

from ivonet.cdll import CircularDoublyLinkedList, Node
from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def create_cll(elves):
    elf_ring = CircularDoublyLinkedList()
    for i in range(1, int(elves) + 1):
        elf_ring.append(i)
    return elf_ring


def part_1(source):
    elf_ring = create_cll(source)
    active_elf: Node = elf_ring.node(0)
    while len(elf_ring) > 1:
        elf_ring.remove(active_elf.next)
        active_elf = elf_ring.next()
    return elf_ring.get()


def part_2(source):
    elf_ring = create_cll(source)
    active_elf = elf_ring.node(0)
    opposite = elf_ring.node(len(elf_ring) // 2)
    while len(elf_ring) > 1:
        elf_ring.remove(opposite)
        opposite = opposite.next if len(elf_ring) % 2 == 1 else opposite.next.next
        active_elf = active_elf.next
    return elf_ring.get()


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")

    def test_example_data_part_1(self):
        self.assertEqual(3, part_1("5"))

    def test_part_1(self):
        self.assertEqual(1842613, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(2, part_2("5"))

    def test_part_2(self):
        self.assertEqual(1424135, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
