#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

from ivonet.files import read_rows


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


if __name__ == '__main__':
    source = read_rows("day_8.input")
    print(part_1(source)[0])  # 1489
    print(part_2(source))
