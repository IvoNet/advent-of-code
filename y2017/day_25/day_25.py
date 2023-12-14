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
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def p(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class State(NamedTuple):
    write: int
    move: int
    next_state: str


def parse(source):
    source = source.replace(".", "").replace(":", "")
    source = source.split("\n\n")
    p(source)
    begin = source[0].strip().splitlines()
    start = begin[0].split()[-1]
    steps = ints(begin[1])[0]
    state = {}
    for block in source[1:]:
        block = block.strip().splitlines()
        s = block[0].replace(":", "").split()[-1]
        w0 = ints(block[2])[0]
        m0 = 1 if "right" in block[3] else -1
        n0 = block[4].strip().split()[-1]
        st = {0: State(w0, m0, n0)}
        w1 = ints(block[6])[0]
        m1 = 1 if "right" in block[7] else -1
        n1 = block[8].strip().split()[-1]
        st[1] = State(w1, m1, n1)
        state[s] = st
    return start, steps, state


def part_1(source):
    start, steps, state = parse(source)
    p(start, steps, state)
    tape = defaultdict(int)
    working_state = state[start]
    position = 0
    for _ in range(steps):
        move = working_state[tape[position]].move
        next_state = working_state[tape[position]].next_state
        tape[position] = working_state[tape[position]].write
        position += move
        working_state = state[next_state]
    return list(tape.values()).count(1)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}_test.input")

    def test_example_data_part_1(self):
        self.assertEqual(3, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(3554, part_1(self.source))


if __name__ == '__main__':
    unittest.main()
