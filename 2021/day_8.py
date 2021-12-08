#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """"""

import unittest

from ivonet import get_data, plist, sort_str

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
    0: "abcefg",
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


               a = top = [0, 2, 3, 5, 6, 7, 8, 9]
        b = tle = [0, 4, 5, 6, 8, 9]
        c = tri = [0, 1, 2, 3, 4, 7, 8, 9]
        d = mdl = [2, 3, 4, 5, 6, 8, 9]
        e = ble = [0, 2, 6, 8]
        f = bri = [0, 1, 3, 4, 5, 6, 7, 8, 9]
        g = btm = [0, 2, 3, 5, 6, 8, 9]
        # 7 - 1 = top

    """

    def __init__(self, data) -> None:
        self.numbers = {}
        self.strs = {}
        self.line = data
        pat, out = data.split(" | ")
        self.pat = [sort_str(x) for x in pat.split()]
        self.out = [sort_str(x) for x in out.split()]
        self.pat_popper = self.pat.copy()
        for x in self.pat:
            self.number_it(x)
        for x in self.out:
            self.number_it(x)
        self.analysis()

    def set_num(self, num: int, s: str):
        self.numbers[num] = s
        self.strs[s] = num
        self.pat_popper.remove(s)

    def number_it(self, s: str):
        num = UNIQUE_NUMBERS_LEN.get(len(s), None)
        if num:
            self.set_num(num, s)

    def str_minus_str(self, s1, s2):
        a = s1
        b = s2
        return "".join([x for x in a if x not in b])

    def str_minus_len(self, s1, s2):
        return len(self.str_minus_str(s1, s2))

    def analysis(self):
        """
        5:
       - 2 - 1 = adeg
         2 - 7 = deg
         2 - 4 = adeg
         8 - 4 = aeg
       - 3 - 7 = dg (uniek)
         3 - 1 = adg
         3 - 4 = ag
         8 - 3 = be
       - 5 - 1 = abdg
         5 - 7 = bdg
         5 - 4 = ag  !! eerst drie identificeren dan 5 met 4
         5 - 9 = --
       6:
       - 0 - 1 = abeg
         0 - 7 =
       - 6 - 1 = abdeg
         6 - 7 = bdeg
         6 - 4 = aeg
         6 - 3 = be !! 3 again
       - 9 - 3 = b !! 3 again
        """
        # original segment distribution
        top = [x for x in self.numbers[7] if x not in self.numbers[1]][0]
        # three is len 5 and has all of 7 in it as the only other 5 len
        for x in self.pat_popper[:]:
            if len(x) == 5:  # [2, 3 ,5]
                print(self.str_minus_str(x, self.numbers[7]))
                if len(self.str_minus_str(x, self.numbers[7])) == 2:
                    self.set_num(3, x)
                    break
        for x in self.pat_popper[:]:  # finding 6 and 9 or 0
            if len(x) == 6:
                if len(self.str_minus_str(x, self.numbers[3])) == 1:
                    self.set_num(9, x)
                    break
        for x in self.pat_popper[:]:  # finding 6 and 9 or 0
            if len(x) == 6 and x != self.numbers[9] and x != self.numbers[3]:
                s1 = self.str_minus_str(x, self.numbers[9])
                s2 = self.str_minus_str(self.numbers[8], self.numbers[9])
                print(s1, s2)
                if s1 == s2:
                    self.set_num(0, x)

        self.check_output()

    def check_output(self):
        print(self.numbers)
        print(self.strs)
        print(self.pat_popper)
        nr = ""
        for x in self.out:
            try:
                nr += str(self.numbers[x])
            except KeyError:
                print("Not complete yet")
                return None
        print(nr)
        return int(nr)

    def __str__(self) -> str:
        return f"{self.pat} | {self.out}"

    def __repr__(self) -> str:
        return self.__str__()


def part_2(data):
    """
       acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
       8                   3     7                 4           1

       - 0 (6) alles van 8 behalve d
       - 1 (2)
       - 2 (5) 1 verschil met 3 (e vs f)
       - 2 - 7 = deg
       - 3 (5)
       - 3 - 7 = dg
       - 4 (4)
       - 5 (5) alles van 6 behalve e
       - 5     alles van 9 behalve c
       - 5 - 7 = bdg
       - 6 (6) bevat volledig 5 plus e
       - 6     alles van 8 behalve c
       - 6     verschil met 9 is c en e
       - 7 (3)
       - 7     - 1 = a (top)
       - 7     past volledig in 0, 3, 8, 9
       - 8 (7) past alles in maar mist
       - 8 - 0 = d
       - 8 - 1 = abdeg
       - 8 - 2 = bf
       - 8 - 3 = be
       - 8 - 4 = aeg
       - 8 - 5 = ce
       - 8 - 6 = c
       - 8 - 7 = bdeg
       - 8 - 9 = e
       - 9 (6) alles van 8 behalve e

       - len 2 = [1]
       - len 3 = [7]
       - len 4 = [4]
       - len 5 = [2, 3, 5]
       - len 6 = [6, 9]
       - len 7 = [8]

       - wat identificeert 2,3,5 en 6,9
         - lengte




    """
    for x in ORIG_NUMBERS:
        print(f"{x} - len[{len(ORIG_NUMBERS[x])}] - {ORIG_NUMBERS[x]}")

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
