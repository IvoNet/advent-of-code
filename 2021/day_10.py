#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import sys
from queue import LifoQueue

from ivonet.files import read_rows

sys.dont_write_bytecode = True

import unittest

POINTS_P1 = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

POINTS_P2 = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

TRANSLATE = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}


def part_1(data):
    points = 0
    leftover_lines = []
    for row in data:
        q = LifoQueue()
        for ch in row:
            if ch in "{([<":
                print(f"P:{ch}-", end=" ")
                q.put(TRANSLATE[ch])
                continue
            last = q.get()
            if ch == last:  # closing tag
                print(f"G:{ch}{last}-", end=" ")
            else:  # wrong
                print("wrong: ", last, ch)
                points += POINTS_P1[ch]
                break
    return points


def part_2(data):
    point_lst = []
    for row in data:
        points = 0
        q = LifoQueue()
        wrong = False
        for ch in row:
            if ch in "{([<":
                q.put(TRANSLATE[ch])
                continue
            last = q.get()
            if ch != last:  # closing tag
                wrong = True
                break
        if not wrong:
            while not q.empty():
                ch = q.get()
                points *= 5
                points += POINTS_P2[ch]
            point_lst.append(points)

    return sorted(point_lst)[len(point_lst) // 2]


class UnitTests(unittest.TestCase):
    source = read_rows("day_10.txt")
    test_source = read_rows("""[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]""")

    def test_example_data_part_1(self):
        self.assertEqual(26397, part_1(self.test_source))

    def test_example_data_part_2(self):
        self.assertEqual(288957, part_2(self.test_source))

    def test_part_1(self):
        self.assertEqual(311895, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
