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

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def prepare(source):
    return [x.split() for x in source]


def reg(register, value):
    """This simple method eliminates quite a bit of plumbing code for the assembler"""
    try:
        return int(value)
    except ValueError:
        return register.get(value, 0)


def duet(program, q_in, q_out=None, v1=False):
    """Made it into a generator to make duality a possibility without actual multithreading"""
    register = {"p": q_in.pop(0)}
    if q_out is None:
        q_out = []
    i = 0
    while 0 <= i < len(program):
        instruction = program[i]
        cmd = instruction[0]
        left = reg(register, instruction[1])
        if cmd == "snd":
            q_out.append(left)
        elif cmd == "rcv":
            if v1:
                if left != 0:
                    yield q_out[-1]
                    return
            else:
                if not q_in:
                    yield None
                register[instruction[1]] = q_in.pop(0)
        else:
            right = reg(register, instruction[2])
            if cmd == "set":
                register[instruction[1]] = right
            elif cmd == "add":
                register[instruction[1]] = left + right
            elif cmd == "mul":
                register[instruction[1]] = left * right
            elif cmd == "mod":
                register[instruction[1]] = left % right
            elif cmd == "jgz" and left > 0:
                i += right - 1
        i += 1


def part_1(source):
    program = prepare(source)
    return next(duet(program, [0], v1=True))


def part_2(source):
    program = prepare(source)
    q0 = [0]
    q1 = [1]
    p0 = duet(program, q0, q1)
    p1 = duet(program, q1, q0)
    p1_sounds = 0

    while q0:
        if q0:
            try:
                next(p0)
            except StopIteration:
                q0 = None
        if q1:
            try:
                next(p1)
            except StopIteration:
                break
            finally:
                _(q0, q1, p1_sounds, len(q0))
                p1_sounds += len(q0)

    return p1_sounds


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2""")

    def test_example_data_part_1(self):
        self.assertEqual(4, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(1187, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(5969, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
