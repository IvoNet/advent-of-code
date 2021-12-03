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


def filter_binaries_on_idx_value(data, idx, value):
    ret = []
    for x in data:
        if x[idx] == value:
            ret.append(x)
    return ret


def binair_counter(data, idx):
    """creates a binary str from the idx of the data list and then counts the 1 and 0"""
    new_bin = "".join([x[idx] for x in data])
    c0 = new_bin.count("0")
    c1 = new_bin.count("1")
    return c0, c1


def oxygen(data, idx):
    """Recursive function to calculate the one binary based on the oxygen rule"""
    if len(data) == 1:
        return data

    c0, c1 = binair_counter(data, idx)
    if c0 > c1:
        new_data = filter_binaries_on_idx_value(data, idx, "0")
    else:
        new_data = filter_binaries_on_idx_value(data, idx, "1")

    return oxygen(new_data, idx + 1)


def co_two(data, idx):
    """Recursive function to calculate the one binary based on the co2 rule"""
    if len(data) == 1:
        return data

    c0, c1 = binair_counter(data, idx)
    if c0 <= c1:
        new_data = filter_binaries_on_idx_value(data, idx, "0")
    else:
        new_data = filter_binaries_on_idx_value(data, idx, "1")

    return co_two(new_data, idx + 1)


def part_1(data):
    gamma = ""
    epsilon = ""
    for idx in range(len(data[0])):
        c0, c1 = binair_counter(data, idx)
        if c0 > c1:
            gamma += "1"
            epsilon += "0"
        else:
            gamma += "0"
            epsilon += "1"
    gamma = int(gamma, 2)
    epsilon = int(epsilon, 2)
    return gamma * epsilon


def part_2(data):
    ox = int(oxygen(data, 0)[0], 2)
    co = int(co_two(data, 0)[0], 2)
    return ox * co


if __name__ == '__main__':
    source = get_data("day-3.txt")
    print("Part 1:", part_1(source))  # 4103154
    print("part 2:", part_2(source))  # 4245351
