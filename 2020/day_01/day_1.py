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


def part_1(data):
    data = list(map(int, data))
    for x in data:
        for y in data[1:]:
            if x + y == 2020:
                return x, y, x * y


def part_2(data):
    data = list(map(int, data))
    for x in data:
        for y in data[1:]:
            for z in data[2:]:
                if x + y + z == 2020:
                    return x, y, z, x * y * z


if __name__ == '__main__':
    source = read_rows("day_01.input")
    print(part_1(source))  # 889779
    print(part_2(source))  # 76110336
