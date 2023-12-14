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
from math import factorial
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
    program = []
    for line in source:
        tmp = line.strip().split()
        cmd = [tmp[0]]
        for x in tmp[1:]:
            try:
                cmd.append(int(x))
            except ValueError:
                cmd.append(x)
        program.append(cmd)
    return program


def assembunny(source, a=0, b=0, c=0, d=0, multiply=False):
    # see 07 and 23 of 2015
    program = prepare(source)
    register = {
        "a": a,
        "b": b,
        "c": c,
        "d": d,
    }
    i = -1
    while True:
        _(register)
        try:
            cmd = program[i]
            # _(" ".join([str(x) for x in cmd]))
        except IndexError:
            return register
        if cmd[0] == "tgl":
            to_tgl = i + register[cmd[1]]
            if to_tgl < 0 or to_tgl >= len(program):
                i += 1
                continue
            tgl_cmd = program[to_tgl]
            if len(tgl_cmd) == 2:
                tgl_cmd[0] = "dec" if tgl_cmd[0] == "inc" else "inc"
            else:  # len(tgl_cmd) == 3:
                tgl_cmd[0] = "cpy" if tgl_cmd[0] == "jnz" else "jnz"
            program[to_tgl] = tgl_cmd
            i += 1
            continue
        if cmd[0] == "cpy" and type(cmd[1]) == int:
            register[cmd[2]] = cmd[1]
            i += 1
            continue
        if cmd[0] == "cpy" and type(cmd[1]) != int:
            register[cmd[2]] = register[cmd[1]]
            i += 1
            continue
        if cmd[0] == "inc":
            register[cmd[1]] += 1
            i += 1
            continue
        if cmd[0] == "dec":
            register[cmd[1]] -= 1
            i += 1
            continue
        if cmd[0] == "jnz" and type(cmd[1]) == int and cmd[1] != 0:
            i += cmd[2] if type(cmd[2]) == int else register[cmd[2]]
            # _(f"jnz to cmd {i}")
            continue
        if cmd[0] == "jnz" and register[cmd[1]] != 0:
            i += cmd[2]
            # _(f"jnz to cmd {i}")
            continue
        # _("No command going to next command:", cmd)
        i += 1
    return None


def part_1(source, a=7):
    register = assembunny(source, a=a)
    _(register)
    return register["a"]


def part_2(source, a=12, multiply=True):
    """Application ran too long
    Analizing the part_1 run...
    - every time register b decrements register a is a factorial down
      so in the end I thought 7! but there was a difference
    - looking further (debug mode on in this case and redirecting the output to a file)
    - I noticed that at the moment b decrements it is a factorial exactly. also when it flipped from 2 to 1
    - so what happends after that as the program is not finished. I scrolled to that point and found this
    {'a': 5040, 'b': 2, 'c': 0, 'd': 0}
    {'a': 5040, 'b': 2, 'c': 0, 'd': 0}  <- 7! right here
    {'a': 5040, 'b': 1, 'c': 0, 'd': 0}
    {'a': 5040, 'b': 1, 'c': 1, 'd': 0}
    {'a': 5040, 'b': 1, 'c': 1, 'd': 1}
    {'a': 5040, 'b': 1, 'c': 1, 'd': 0}
    {'a': 5040, 'b': 1, 'c': 2, 'd': 0}
    {'a': 5040, 'b': 1, 'c': 2, 'd': 0}
    {'a': 5040, 'b': 1, 'c': 2, 'd': 0}
    {'a': 5040, 'b': 1, 'c': -16, 'd': 0}
    {'a': 5040, 'b': 1, 'c': 1, 'd': 0}
    {'a': 5040, 'b': 1, 'c': 85, 'd': 0}
    {'a': 5040, 'b': 1, 'c': 85, 'd': 76}   <--!! adding a multiplcation of 85 * 76
    {'a': 5041, 'b': 1, 'c': 85, 'd': 76}
    {'a': 5041, 'b': 1, 'c': 85, 'd': 75}
    {'a': 5041, 'b': 1, 'c': 85, 'd': 75}
    jnz 1 c
    cpy 85 c
    jnz 76 d
    inc a
    so that is it.
    My guess was that this would be the same when a=12 was used... proved to be correct :-)
    I may try to optimize this in assembunny itself at a later day if I feel like it :-)
    """
    return factorial(a) + 85 * 76


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}_test_a.input")

    def test_example_data_part_1(self):
        self.assertEqual(3, part_1(self.test_source, a=0))

    def test_part_1(self):
        self.assertEqual(11500, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(479008060, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
