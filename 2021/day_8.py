#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """"""

import unittest

from ivonet import get_data, plist

UNIQUE_NUMBERS = {
    1: 2,
    4: 4,
    7: 3,
    8: 7,
}
UNIQUE_NUMBERS_LEN = {
    2: 1,
    4: 4,
    3: 7,
    7: 8,
}

ORIG_NUMBERS = {
    0: "abcef",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg",
}


def part_1(data):
    output = [x.split(" | ")[1].split() for x in data]
    print(output)
    counter = 0
    for x in output:
        for y in x:
            print(y)
            if len(y) in [2, 4, 3, 7]:
                counter += 1
    return counter


class Display(object):
    """
           0: abcefg
       - 6 long
       - misses only d from 8
       - only 0 and 9 have 6 digits

       1: cf
       - unique length 2
       - right side

       2: acdeg
       - 2 is 5 long
       - 2 does not have pattern of 1 (1=cf, 2=acdeg)
       - 2 does have the top part of 1 (c)
       - 2 has has a and c in common with 7 (top, right top)

       3: acdfg
       - 3 is 5 long
       - 3 had full pattern of 1 and 7
       - 3 has right line (df) in common with 4

       4: bcdf
       - unique length 4
       - directly identifiable

       5: abdfg
       - len 5
       - has only lower right half of 1 in its pattern (f)
       - has top and right bottom of 7 in its pattern
       - has bdf of 4 in its pattern

       6: abdefg
       - len 6
       - f of 1 (lower right)
       - af of 7 (top and lower right)
       - bdf of 4

       7: acf
       - unique len 3
       - directly identifiable

       8: abcdefg
       - unique len 7
       - directly identifiable


       - 1,4,7,8 directly identifiable
       - 2 if len = 5 and...
       - 3 if len = 4 and contains all of 1 and 7
    """

    def __init__(self, data) -> None:
        self.numbers = {}
        self.line = data
        pat, out = data.split(" | ")
        pat = pat.split()
        out = out.split()
        self.pat = []
        self.out = []
        for x in pat:
            num = self.number_it(x)
            self.pat.append([x, num])
        for x in out:
            num = self.number_it(x)
            self.out.append([x, num])

    def number_it(self, s: str):
        num = UNIQUE_NUMBERS_LEN.get(len(s), None)
        if num:
            self.numbers[num] = s
            return num
        if len(s) == 5:
            if sum(1 for l in self.numbers.get(1, "z") if l in s) == 2:
                if sum(1 for l in self.numbers.get(7, "z") if l in s) == 3:
                    # s = 3
                    self.numbers[3] = s

        return num

    def __str__(self) -> str:
        return f"{self.pat} | {self.out}"

    def __repr__(self) -> str:
        return self.__str__()


def part_2(data):
    """
       acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
       8                   3     7                 4           1

    """
    source = [Display(x) for x in data]
    plist(source)


class UnitTests(unittest.TestCase):
    source = get_data("day_8.txt")
    test_source_small = ["acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"]
    test_source = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce""".split("\n")

    def test_example_data_part_1(self):
        self.assertEqual(26, part_1(self.test_source))

    def test_example_data_part_2_small(self):
        self.assertEqual(5353, part_2(self.test_source_small))

    def test_example_data_part_2(self):
        self.assertEqual(61229, part_2(self.test_source))

    def test_part_1(self):
        self.assertEqual(449, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
