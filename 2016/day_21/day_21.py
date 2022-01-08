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

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def swap_position(data: str, x: int, y: int):
    ret = list(data)
    ret[x], ret[y] = ret[y], ret[x]
    return "".join(ret)


def swap_letter(data: str, a: str, b: str):
    return swap_position(data, data.index(a), data.index(b))


def rotate_right(data: str, steps: int):
    steps = steps % len(data)
    return data[-steps:] + data[:-steps]


def rotate_left(data: str, steps: int):
    steps = steps % len(data)
    return data[steps:] + data[:steps]


def rotate_based(data: str, letter: str):
    pos = data.index(letter)
    data = rotate_right(data, 1)
    data = rotate_right(data, pos)
    if pos >= 4:
        data = rotate_right(data, 1)
    return data


def move_pos(data: str, x: int, y: int):
    l = data[x]
    lst = list(data)
    lst.remove(l)
    lst.insert(y, l)
    return "".join(lst)


def reverse_positions(data: str, x: int, y: int):
    ret = data[:x]
    ret += data[x:y + 1][::-1]
    tail = len(data) - 1 - y
    if tail > 0:
        ret += data[-tail:]
    return ret


def scramble(source, password):
    data = password
    for line in source:
        cmd = line.split()
        if cmd[0] == "swap":
            if cmd[1] == "position":
                data = swap_position(data, int(cmd[2]), int(cmd[5]))
                continue
            if cmd[1] == "letter":
                data = swap_letter(data, cmd[2], cmd[5])
                continue
        if cmd[0] == "rotate":
            if cmd[1] == "left":
                data = rotate_left(data, int(cmd[2]))
                continue
            if cmd[1] == "right":
                data = rotate_right(data, int(cmd[2]))
                continue
            if cmd[1] == "based":
                data = rotate_based(data, cmd[-1])
                continue
        if cmd[0] == "reverse":
            data = reverse_positions(data, int(cmd[2]), int(cmd[4]))
            continue
        if cmd[0] == "move":
            data = move_pos(data, int(cmd[2]), int(cmd[5]))
    return data


def unscramble(source, password):
    data = password
    for line in source[::-1]:
        cmd = line.split()
        if cmd[0] == "swap":
            if cmd[1] == "position":  # untouched
                data = swap_position(data, int(cmd[2]), int(cmd[5]))
                continue
            if cmd[1] == "letter":  # untouched
                data = swap_letter(data, cmd[2], cmd[5])
                continue
        if cmd[0] == "rotate":
            if cmd[1] == "left":  # left becomes right
                data = rotate_right(data, int(cmd[2]))
                continue
            if cmd[1] == "right":  # richt becomes left
                data = rotate_left(data, int(cmd[2]))
                continue
            if cmd[1] == "based":  # biggest change
                # idx  shft npos sht
                # 0   r:1  1    l:1
                # 1   r:2  3    l:2
                # 2   r:3  5    l:3
                # 3   r:4  7    l:4
                # 4   r:6  2    l:6
                # 5   r:7  4    l:7  8 = len passwd
                # 6   r:8  6    l:8 (8 is same place)
                # 7   r:9  0    l:9 (mod 8) -> build in rotate_left
                c = cmd[-1]
                i = data.index(c)
                m = {0: 9, 1: 1, 2: 6, 3: 2, 4: 7, 5: 3, 6: 8, 7: 4, }
                data = rotate_left(data, m[i])
                continue
        if cmd[0] == "reverse":  # untouched
            data = reverse_positions(data, int(cmd[2]), int(cmd[4]))
            continue
        if cmd[0] == "move":  # swapped to unscramble
            data = move_pos(data, int(cmd[5]), int(cmd[2]))
    return data


def part_1(source, password="abcdefgh"):
    return scramble(source, password)


def part_2(source, password="fbgdceah"):
    return unscramble(source, password)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d""")

    def test_swap_position(self):
        self.assertEqual("abhdefgc", swap_position("abcdefgh", 2, 7))

    def test_swap_letter(self):
        self.assertEqual("abhdefgc", swap_letter("abcdefgh", "c", "h"))
        self.assertEqual("bacdefgh", swap_letter("abcdefgh", "a", "b"))

    def test_rotate_right(self):
        self.assertEqual("dabc", rotate_right("abcd", 1))

    def test_rotate_left(self):
        self.assertEqual("bcda", rotate_left("abcd", 1))

    def test_rotate_based(self):  # ..................................idx shft nps shift
        self.assertEqual("habcdefg", rotate_based("abcdefgh", "a"))  # 0  r:1   1   l:1
        self.assertEqual("ghabcdef", rotate_based("abcdefgh", "b"))  # 1  r:2   3   l:2
        self.assertEqual("fghabcde", rotate_based("abcdefgh", "c"))  # 2  r:3   5   l:3
        self.assertEqual("efghabcd", rotate_based("abcdefgh", "d"))  # 3  r:4   7   l:4
        self.assertEqual("cdefghab", rotate_based("abcdefgh", "e"))  # 4  r:6   2   l:6
        self.assertEqual("bcdefgha", rotate_based("abcdefgh", "f"))  # 5  r:7   4   l:7
        self.assertEqual("abcdefgh", rotate_based("abcdefgh", "g"))  # 6  r:8   6   l:8
        self.assertEqual("habcdefg", rotate_based("abcdefgh", "h"))  # 7  r:9   0   l:9

    def test_reverse_positions(self):
        self.assertEqual("abedcfgh", reverse_positions("abcdefgh", 2, 4))

    def test_move_pos(self):
        self.assertEqual("abdecfgh", move_pos("abcdefgh", 2, 4))

    def test_example_data_part_1(self):
        self.assertEqual("decab", part_1(self.test_source, password="abcde"))

    def test_part_1(self):
        self.assertEqual("gbhcefad", part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual("abcde", part_2(self.test_source, password="decab"))

    def test_part_2(self):
        self.assertEqual("gahedfcb", part_2(self.source))


if __name__ == '__main__':
    unittest.main()
