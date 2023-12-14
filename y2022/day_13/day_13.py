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
from functools import cmp_to_key
from pathlib import Path

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def parse(source):
    """list if ints or list of lists of ints
    Used eval as it already had the correct python format otherwise
    it would have been a lot of work :-)
    """
    packets = []
    for packet in source:
        left, right = packet.split("\n")
        packets.append((eval(left), eval(right)))
    return packets


def compare_packets(left, right):
    """compare left packet to right packet
    A compare function should give -1, 0 or 1 back to give indicate smaller equal or larger
    As we are comparing different types and multiple of them we make the function recursive.
    Starting with the smallest denominator and working our way up.
    - start with comparing ints -> terminator
    - then lists -> recursive
    - then mixed lists and ints -> recursive
    all compares will eventually end up in the terminator step
    """
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return -1
        elif left == right:
            return 0
        else:
            return 1
    elif isinstance(left, list) and isinstance(right, list):
        i = 0
        while i < len(left) and i < len(right):
            cmp = compare_packets(left[i], right[i])
            if cmp == -1:
                return -1
            if cmp == 1:
                return 1
            i += 1
        if i == len(left) and i < len(right):
            return -1
        elif i == len(right) and i < len(left):
            return 1
        return 0
    elif isinstance(left, int) and isinstance(right, list):
        return compare_packets([left], right)
    else:
        return compare_packets(left, [right])


def part_1(source):
    packets = parse(source)
    part1 = 0
    for i, packet in enumerate(packets, 1):
        left, right = packet
        right_order = compare_packets(left, right)
        if right_order == -1:
            part1 += i
    _(packets)
    return part1


def part_2(source):
    """Just take all the packets add the divider packets and sort them
    as we already wrote a compare function we can use that to sort the packets,
    but now we have a challenge as I know python can sort by key but
    can it also sort with a compare function? -> YES -> functools.cmp_to_key
    found a good explanation here: https://learnpython.com/blog/python-custom-sort-function/
    """
    packets = parse(source)
    packs = []
    for i, packet in enumerate(packets, 1):
        left, right = packet
        packs.append(left)
        packs.append(right)
    packs.append([[2]])
    packs.append([[6]])

    packs = sorted(packs, key=cmp_to_key(lambda l, r: compare_packets(l, r)))
    _(packs)
    devider_1 = 1 + packs.index([[2]])
    devider_2 = 1 + packs.index([[6]])
    decoder_key = devider_1 * devider_2
    _(decoder_key)
    return decoder_key


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input").split("\n\n")
        self.test_source = read_data("""[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]""").split("\n\n")

    def test_example_data_part_1(self):
        self.assertEqual(13, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(5623, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(140, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(20570, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
