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

import re

from ivonet import read_data

PASSPORT_CODES = [
    "byr",
    "iyr",
    "eyr",
    "hgt",
    "hcl",
    "ecl",
    "pid",
    "cid",
]
MANDATORY_PASSPORT_CODES = [
    "byr",
    "iyr",
    "eyr",
    "hgt",
    "hcl",
    "ecl",
    "pid",
    # "cid",
]


def part_1(data):
    passports = data.split("\n\n")
    valid_passports = 0
    parsed_paspoorts = []
    for psp in passports:
        psp = psp.replace("\n", " ").strip().split(" ")
        pp = {}
        for k in psp:
            key, value = k.split(":")
            pp[key] = value
        valid = True
        for code in MANDATORY_PASSPORT_CODES:
            if code not in pp:
                valid = False
                break
        if valid:
            parsed_paspoorts.append(pp)
            valid_passports += 1
    return parsed_paspoorts, valid_passports


def part_2(data):
    passports = part_1(data)[0]
    valid_passports = 0
    parsed_valid_passports = []
    for pp in passports:
        valid = True
        key = "byr"
        if int(pp[key]) < 1920 or int(pp[key]) > 2002:
            # print(key, pp)
            valid = False

        key = "iyr"
        if int(pp[key]) < 2010 or int(pp[key]) > 2020:
            # print(key, pp)
            valid = False

        key = "eyr"
        value = int(pp[key])
        if value < 2020 or value > 2030:
            # print(key, pp)
            valid = False

        key = "hgt"
        if pp[key].endswith("in"):
            if int(pp[key].replace("in", "")) < 59 or int(pp[key].replace("in", "")) > 79:
                # print("hgt 1", pp)
                valid = False
        elif pp[key].endswith("cm"):
            if int(pp[key].replace("cm", "")) < 150 or int(pp[key].replace("cm", "")) > 193:
                # print("hgt 2", pp)
                valid = False
        else:
            # print("hgt 3", pp)
            valid = False

        key = "hcl"
        if not re.match("^#[0-9a-f]{6}$", pp[key]):
            # print(key, pp)
            valid = False

        key = "ecl"
        if not pp[key] in "amb blu brn gry grn hzl oth".split(" "):
            # print(key, pp)
            valid = False

        key = "pid"
        if not re.match("^[0-9]{9}$", pp[key]):
            # print(key, pp)
            valid = False

        if valid:
            valid_passports += 1
            # print("valid", pp)
            parsed_valid_passports.append(pp)
    return valid_passports


if __name__ == '__main__':
    source = read_data("day_4.txt")
    #     print(part_2("""eyr:1972 cid:100
    # hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926
    #
    # iyr:2019
    # hcl:#602927 eyr:1967 hgt:170cm
    # ecl:grn pid:012533040 byr:1946
    #
    # hcl:dab227 iyr:2012
    # ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277
    #
    # hgt:59cm ecl:zzz
    # eyr:2038 hcl:74454a iyr:2023
    # pid:3556412378 byr:2007"""))
    print("Part 1:", part_1(source)[1])  # 213
    print("Part 2:", part_2(source))  # 147
