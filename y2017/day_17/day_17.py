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


def part_1(source, times=2017):
    """Left this one in as it is beautiful :-)
    The improved performance version is done in part 2
    """
    cdll = CircularDoublyLinkedList()
    cdll.append(0)
    for i in range(1, times + 1):
        cdll.step_right(int(source))
        cdll.insert_after_current(i)
        cdll.next()

    return cdll.next().data


def part_2(source, times=50_000_000):
    """Yeah quite a big list and that does not improve performance at all
    50 milion objects created and the like...
    So what can we do to optimize?
    analyse:
    - don't really need al these obejcts as we are working with integers
    - head starts at 0 with size 1
    - need to walk 348 times to go to position but size is 1 so walking to myself
    - so head = head % size seems plausible
    - nope even better as we need to walk om circles 348 times we need to determin where to add
    - head = (head + 348) % size -> when only size 1 this will result in 0 so insert after index 0
    - now we have 0 (1) (need to move the head to index 1) and size = 2
    - head = head + 348 % size = (1 + 348) % 2 = 1
    - not actually interested in all the other numbers only the one we insert after the head function == 0
      as that inserts the value after zero :-) so as long as we keep track of that we can speed things up a lot
    """
    the_one_after_zero = 0
    size = 1
    steps = int(source)
    head = 0
    for k in range(50_000_000):
        head = (head + steps) % size
        if head == 0:
            the_one_after_zero = size
        head += 1
        size += 1
    return the_one_after_zero

class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_data("""3""")

    def test_example_data_part_1(self):
        self.assertEqual(638, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(417, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(34334221, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
