#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import unittest

from ivonet.files import read_rows
from ivonet.iter import sort_dict_on_values
from ivonet.str import sort_str, str_minus_len

UNIQUE_NUMBERS_LEN = {
    2: 1,
    4: 4,
    3: 7,
    7: 8,
}


def part_1(data):
    return sum(sum(1 for y in x if len(y) in [2, 4, 3, 7]) for x in [x.split(" | ")[1].split() for x in data])


class Display(object):
    def __init__(self, data) -> None:
        self.orig = data
        self.numbers = {}
        self.str_numbers = {}
        pat, out = data.split(" | ")
        self.pat = [sort_str(x) for x in pat.split()]
        self.out = [sort_str(x) for x in out.split()]
        self.slink_list = self.pat.copy()

        self.__analysis()

    def __set_num(self, num: int, s: str):
        self.numbers[num] = s
        self.str_numbers[s] = num
        self.slink_list.remove(s)

    def __get_sizes(self, size: int):
        return [x for x in self.slink_list if len(x) == size]

    def __find_1_4_7_8(self):
        """These numbers have unique length so are easy to identify"""
        for s in self.pat:
            num = UNIQUE_NUMBERS_LEN.get(len(s), None)
            if num:
                self.__set_num(num, s)

    def __find_3(self):
        """"""
        for x in self.__get_sizes(5):
            if str_minus_len(x, self.numbers[7]) == 2:
                self.__set_num(3, x)
                break

    def __find_9(self):
        for x in self.__get_sizes(6):
            if str_minus_len(x, self.numbers[3]) == 1:
                self.__set_num(9, x)
                break

    def __find_5_and_2(self):
        for x in self.__get_sizes(5):
            if str_minus_len(x, self.numbers[9]) == 0:
                self.__set_num(5, x)
            else:
                self.__set_num(2, x)

    def __find_6_and_0(self):
        for x in self.__get_sizes(6):
            if str_minus_len(x, self.numbers[5]) == 1:
                self.__set_num(6, x)
            else:
                self.__set_num(0, x)  # ==2

    def __analysis(self):
        """
        - all found numbers are removed from the list to parse
        - when saying 5 - 1 it means the string representation of the two subtracted e.g. dab(7) - ab(1) = d -> len 1
        - the ordering of the method calls is important!
        - [1, 4, 7, 8] are known by size so easy
        - in five range:
          - 3 -> if len 3 - 7 == 2 -> unique when subtracting 7 of the others in the range
        - in six range:
          - 9 -> if len 9 - 3(str) == 1 -> unique when subtracting 3 from others in the range
        - in five range again:
          - 5 -> if len str(5) - 9(str) == 0
          - 2 -> if len str(5) - 9(str) == 1
        - in six range:
          - 6 -> if len str(6) - 5 == 1
          - 0 -> if len str(6) - 5 == 2 (or the else of 6)
        """
        self.__find_1_4_7_8()
        self.__find_3()
        self.__find_9()
        self.__find_5_and_2()
        self.__find_6_and_0()

    def result(self):
        nr = ""
        for x in self.out:
            try:
                nr += str(self.str_numbers[x])
            except KeyError:
                print("Not complete yet")
                return None
        return int(nr)

    def print(self):
        self.str_numbers = sort_dict_on_values(self.str_numbers)
        ret = f"{self.orig} -> {self.result()}\n"
        for key in self.str_numbers:
            ret += f"{key:<7} = {self.str_numbers[key]}\n"
        return ret

    def __str__(self) -> str:
        return self.print()

    def __repr__(self) -> str:
        return f"{self.pat} - {self.result()}"


def part_2(data):
    source = [Display(x) for x in data]
    for x in source:
        print(x)

    return sum(x.result() for x in source)


class UnitTests(unittest.TestCase):
    source = read_rows("day_8.input")
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
        self.assertEqual(968175, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
