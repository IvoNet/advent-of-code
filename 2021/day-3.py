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

from ivonet import get_data


def part_1(data):
    gamma = ""
    epsilon = ""
    for idx in range(len(data[0])):
        new_bin = ""
        for bin in data:
            new_bin += bin[idx]
        c1 = new_bin.count("0")
        c2 = new_bin.count("1")
        if c1 > c2:
            gamma += "1"
            epsilon += "0"
        else:
            gamma += "0"
            epsilon += "1"
    gamma = int(gamma, 2)
    epsilon = int(epsilon, 2)
    return gamma * epsilon


def filter(data, idx, value):
    ret = []
    for x in data:
        if x[idx] == value:
            ret.append(x)
    return ret


def oxygen(data, idx, max=11):
    if idx > max:
        print(data)
        return data
    if len(data) == 1:
        return data[0]

    new_bin = ""
    for bin in data:
        new_bin += bin[idx]
    c1 = new_bin.count("0")
    c2 = new_bin.count("1")
    if c1 > c2:
        new_data = filter(data, idx, "0")
    else:
        new_data = filter(data, idx, "1")

    return oxygen(new_data, idx + 1)


def co_two(data, idx, max=11):
    print(data, idx)
    # if idx > max:
    #     print(data)
    #     return data
    if len(data) == 1:
        return data

    new_bin = ""
    for bin in data:
        new_bin += bin[idx]
    c1 = new_bin.count("0")
    c2 = new_bin.count("1")
    if c1 <= c2:
        new_data = filter(data, idx, "0")
    else:
        new_data = filter(data, idx, "1")

    return co_two(new_data, idx + 1)


def part_2(data):
    ox = int(oxygen(data, 0)[0], 2)
    co = int(co_two(data, 0)[0], 2)
    return ox * co


if __name__ == '__main__':
    source = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010""".split()
    source = get_data("day-3.txt")
    print("Part 1:", part_1(source))  #
    print("part 2:", part_2(source))  #
