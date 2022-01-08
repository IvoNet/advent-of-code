#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

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
    program = []
    for line in source:
        cmd = line.replace(",", "").strip().split()
        if cmd[0] in ("jio", "jmp", "jie"):
            del (cmd[-1])
            cmd.insert_at_end(ints(line)[0])
        program.append(cmd)
    return program


def part_1(source, a=0, b=0):
    program = prepare(source)
    register = {
        "a": a,
        "b": b
    }
    i = 0
    while True:
        try:
            cmd = program[i]
        except IndexError:
            return register["b"]
        if cmd[0] == "inc":
            register[cmd[1]] += 1
            _(f"inc {cmd[1]} to {register[cmd[1]]}")
            i += 1
            continue
        if cmd[0] == "tpl":
            register[cmd[1]] *= 3
            _(f"tpl {cmd[1]} to {register[cmd[1]]}")
            i += 1
            continue
        if cmd[0] == "hlf":
            register[cmd[1]] //= 2
            _(f"hlf {cmd[1]} to {register[cmd[1]]}")
            i += 1
            continue
        if cmd[0] == "jmp":
            i += cmd[1]
            _(f"jmp to cmd {i}")
            continue
        if cmd[0] == "jio" and register[cmd[1]] == 1:
            i += cmd[2]
            _(f"jio {cmd[1]} to {i}")
            continue
        if cmd[0] == "jie" and register[cmd[1]] % 2 == 0:
            i += cmd[2]
            _(f"jie {cmd[1]} to {i}")
            continue
        _("No command going to next command:", cmd)
        i += 1
    return None


def part_2(source):
    return part_1(source, a=1)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}.input")))

    def test_part_1(self):
        self.assertEqual(170, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(247, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
