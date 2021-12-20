#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
##############################################################################
# Part 1
##############################################################################

##############################################################################
# Part 2
##############################################################################

"""

from ivonet.files import read_rows


def part_1(data, right=3, down=1):
    trees = 0
    for i in range(1, len(data)):
        x = i * right
        y = i * down
        if y > len(data):
            break
        while x >= len(data[y]):
            data[y] += data[y]
        if data[y][x] == "#":
            trees += 1
    return trees


def part_2(data):
    a = part_1(data, right=1, down=1)
    b = part_1(data, right=3, down=1)
    c = part_1(data, right=5, down=1)
    d = part_1(data, right=7, down=1)
    e = part_1(data, right=1, down=2)
    # print(a, b, c, d, e)
    return a * b * c * d * e


if __name__ == '__main__':
    source = read_rows("day_3.txt")
    print("Part 1:", part_1(source))  # 289
    print("part 2:", part_2(source))  # 5522401584
