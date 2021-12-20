#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

from ivonet.files import read_rows


def part_1(data):
    valid_count = 0
    for password in data:
        a, b, c = password.split(" ")
        l_min, l_max = list(map(int, a.split("-")))
        letter = b.split(":")[0]
        pwd = c.strip()
        if l_min <= pwd.count(letter) <= l_max:
            valid_count += 1
    return valid_count


def part_2(data):
    valid_count = 0
    for password in data:
        a, b, c = password.split(" ")
        l_min, l_max = list(map(int, a.split("-")))
        letter = b.split(":")[0]
        pwd = c.strip()
        if l_min > len(pwd):
            continue
        if l_max > len(pwd) and pwd[l_min - 1] == letter:
            valid_count += 1
            continue
        if pwd[l_min - 1] == letter and pwd[l_max - 1] == letter:
            continue
        if pwd[l_min - 1] == letter or pwd[l_max - 1] == letter:
            valid_count += 1
    return valid_count


if __name__ == '__main__':
    source = read_rows("day_2.input")
    print(part_1(source))  # 469
    print(part_2(source))  # 267
