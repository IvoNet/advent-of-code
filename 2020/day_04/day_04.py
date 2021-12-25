#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import re
import unittest
from pathlib import Path

from ivonet.files import read_data
from ivonet.iter import ints

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


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"day_{day.zfill(2)}.input")

    def test_part_1(self):
        self.assertEqual(213, part_1(self.source)[1])

    def test_part_2(self):
        self.assertEqual(147, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
