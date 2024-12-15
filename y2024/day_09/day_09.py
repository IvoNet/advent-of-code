#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2023 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
If a part of the code is not part of the post it is probably 
code I found reusable and I may have moved it to my 'ivonet' library.
you can find that here: https://github.com/IvoNet/advent-of-code/tree/master/ivonet
"""

import collections
import os
import sys
import unittest
from collections import deque, abc
from pathlib import Path

import pyperclip

from ivonet.decorators import debug
from ivonet.decorators import timer
from ivonet.files import read_data
from ivonet.iter import ints

collections.Callable = abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


class Defragmentator:
    def __init__(self, source: str):
        self.source = source
        self.disk = [int(x) for x in source]
        self.unpacked = []

    def parse(self):
        file_queue = deque([])
        spaces = deque([])
        file_id = 0
        pos = 0
        for idx, file_or_space in enumerate(self.disk):
            if idx % 2 == 0:
                for _ in range(file_or_space):
                    self.unpacked.append(file_id)
                    file_queue.append((pos, 1, file_id))
                    pos += 1
                file_id += 1
            else:
                spaces.append((pos, file_or_space))
                for _ in range(file_or_space):
                    self.unpacked.append(None)
                    pos += 1
        p(self.unpacked)

        for (pos, sz, file_id) in reversed(file_queue):
            for space_idx, (space_pos, space_sz) in enumerate(spaces):
                if space_pos < pos and sz <= space_sz:
                    for i in range(sz):
                        self.unpacked[pos + i] = None
                        self.unpacked[space_pos + i] = file_id
                    spaces[space_idx] = (space_pos + sz, space_sz - sz)
                    break

        answer = 0
        for pos, c in enumerate(self.unpacked):
            if c is not None:
                answer += pos * c
        p(self.unpacked)
        return answer

@debug
@timer
def part_1(source) -> int | None:
    answer = 0
    d = Defragmentator(source)
    answer = d.parse()
    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:
    answer = 0
    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(1928, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(6461289671426, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(None, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_data(f"{folder}/day_{day}.input")
        self.test_source = read_data(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
