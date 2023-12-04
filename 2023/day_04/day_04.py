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
import unittest
from pathlib import Path
from queue import Queue

import sys

from ivonet.collection import Queue
from ivonet.files import read_rows
from ivonet.iter import ints, rangei

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def double_it(value):
    return value + value


def part_1(source):
    answer = 0
    for line in source:
        card = []
        crd = True
        ret = 0
        for v in line.strip().split(":")[1].strip().split(" "):
            if v.isdigit() and crd:
                card.append(int(v))
                continue
            if v == "|":
                crd = False
                continue
            if v.isdigit() and not crd:
                if int(v) in card:
                    if ret == 0:
                        ret = 1
                    else:
                        ret = double_it(ret)
        answer += ret

    return answer


def part_2(source):
    ans = 0
    card_dict = {}
    q = Queue()

    for line in source:
        card_id, numbers = line.split(':')
        card_id = int(card_id[4:])
        winner, ours = numbers.split('|')
        ws = set(winner.split())
        us = set(ours.split())
        matches = ws & us
        card_dict[card_id] = len(matches)
        q.push(card_id)

    while not q.empty:
        ans += 1
        card = q.pop()
        for i in rangei(card + 1, card + card_dict[card]):
            q.push(i)

    return ans


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""")
        self.test_source2 = read_rows("""""")

    def test_example_data_part_1(self):
        self.assertEqual(13, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(25004, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(30, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(14427616, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
