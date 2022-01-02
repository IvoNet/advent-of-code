#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import unittest
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints


def parse(instruction):
    cmd, offset = instruction.split(" ")
    return cmd, int(offset)


def part_1(data):
    history = set()
    accumulator = 0
    idx = 0
    step = data[idx]
    running = True
    while running:
        if idx in history:
            break
        history.add(idx)

        cmd, offset = parse(step)
        if cmd == 'nop':
            idx += 1
            step = data[idx]
        elif cmd == "acc":
            accumulator += offset
            idx += 1
        else:
            idx += offset
        if idx >= len(data):
            running = False
        else:
            step = data[idx]

    return accumulator, running


def part_2(data):
    my_app = data.copy()
    for idx, command in enumerate(data):
        cmd, offset = parse(command)
        if cmd == "nop" and offset != 0:
            my_app[idx] = f"jmp {offset}"
        if cmd == "jmp":
            my_app[idx] = f"nop {offset}"
        if cmd == "acc":
            continue
        accumulator, running = part_1(my_app)
        if not running:
            # print(idx, data[idx])
            return accumulator
        my_app = data.copy()


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}.input")))

    def test_part_1(self):
        self.assertEqual(1489, part_1(self.source)[0])

    def test_part_2(self):
        self.assertEqual(1539, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
