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
from ivonet.primes import is_prime

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


def duet(program, a=0, v1=True):
    """Made it into a generator to make duality a possibility without actual multithreading"""
    register = {"a": a}
    i = 0
    mul_count = 0
    while 0 <= i < len(program):
        _(register)
        instruction = program[i]
        cmd = instruction[0]
        left = reg(register, instruction[1])
        right = reg(register, instruction[2])
        if cmd == "set":
            register[instruction[1]] = right
        elif cmd == "sub":
            register[instruction[1]] = left - right
        elif cmd == "mul":
            register[instruction[1]] = left * right
            mul_count += 1
        elif cmd == "jnz" and left != 0:
            i += right - 1
        i += 1
    if v1:
        return mul_count


def part_1(source):
    program = prepare(source)
    return duet(program, v1=True)


def part_2(source):
    """Hmm don't particularly like these problems

    {'a': 1, 'b': 108400, 'c': 125400, 'f': 1, 'd': 2, 'e': 5171, 'g': -103229}
    {'a': 1, 'b': 108400, 'c': 125400, 'f': 1, 'd': 2, 'e': 5171, 'g': 2}
    {'a': 1, 'b': 108400, 'c': 125400, 'f': 1, 'd': 2, 'e': 5171, 'g': 10342}
    {'a': 1, 'b': 108400, 'c': 125400, 'f': 1, 'd': 2, 'e': 5171, 'g': -98058}
    {'a': 1, 'b': 108400, 'c': 125400, 'f': 1, 'd': 2, 'e': 5171, 'g': -98058}
    {'a': 1, 'b': 108400, 'c': 125400, 'f': 1, 'd': 2, 'e': 5172, 'g': -98058}
    {'a': 1, 'b': 108400, 'c': 125400, 'f': 1, 'd': 2, 'e': 5172, 'g': 5172}
    {'a': 1, 'b': 108400, 'c': 125400, 'f': 1, 'd': 2, 'e': 5172, 'g': -103228}
    {'a': 1, 'b': 108400, 'c': 125400, 'f': 1, 'd': 2, 'e': 5172, 'g': -103228}
    {'a': 1, 'b': 108400, 'c': 125400, 'f': 1, 'd': 2, 'e': 5172, 'g': 2}
    {'a': 1, 'b': 108400, 'c': 125400, 'f': 1, 'd': 2, 'e': 5172, 'g': 10344}
    {'a': 1, 'b': 108400, 'c': 125400, 'f': 1, 'd': 2, 'e': 5172, 'g': -98056}
    {'a': 1, 'b': 108400, 'c': 125400, 'f': 1, 'd': 2, 'e': 5172, 'g': -98056}
    {'a': 1, 'b': 108400, 'c': 125400, 'f': 1, 'd': 2, 'e': 5173, 'g': -98056}
    {'a': 1, 'b': 108400, 'c': 125400, 'f': 1, 'd': 2, 'e': 5173, 'g': 5173}
    {'a': 1, 'b': 108400, 'c': 125400, 'f': 1, 'd': 2, 'e': 5173, 'g': -103227}
    {'a': 1, 'b': 108400, 'c': 125400, 'f': 1, 'd': 2, 'e': 5173, 'g': -103227}
    {'a': 1, 'b': 108400, 'c': 125400, 'f': 1, 'd': 2, 'e': 5173, 'g': 2}
    {'a': 1, 'b': 108400, 'c': 125400, 'f': 1, 'd': 2, 'e': 5173, 'g': 10346}
    {'a': 1, 'b': 108400, 'c': 125400, 'f': 1, 'd': 2, 'e': 5173, 'g': -98054}
    {'a': 1, 'b': 108400, 'c': 125400, 'f': 1, 'd': 2, 'e': 5173, 'g': -98054}
    {'a': 1, 'b': 108400, 'c': 125400, 'f': 1, 'd': 2, 'e': 5174, 'g': -98054}
    {'a': 1, 'b': 108400, 'c': 125400, 'f': 1, 'd': 2, 'e': 5174, 'g': 5174}

    - A range between 108400 and 125400 I guess
    - register h only used ones
    - last value minus one (off one problem or last zero indexed?)
    - e counts up to 108400
    - c - b = 17000
    - but what does it do?
    See if it is a composite I guess in steps of 17
    """
    b = 108400
    c = 125400
    h = 0
    for x in range(b, c + 1, 17):
        if not is_prime(x):
            h += 1
    return h


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")

    def test_part_1(self):
        self.assertEqual(6724, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(903, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
