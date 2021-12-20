#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
You barely reach the safety of the cave when the whale smashes into the cave mouth, 
collapsing it. Sensors indicate another exit to this cave at a much greater depth, 
so you have no choice but to press on.

As your submarine slowly makes its way through the cave system, you notice that the 
four-digit seven-segment displays in your submarine are malfunctioning; they must 
have been damaged during the escape. 
You'll be in a lot of trouble without them, so you'd better figure out what's wrong.

Each digit of a seven-segment display is rendered by turning on or off any of 
seven segments named a through g:

  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg
 
So, to render a 1, only segments c and f would be turned on; the rest would be off. 
To render a 7, only segments a, c, and f would be turned on.

The problem is that the signals which control the segments have been mixed up on each 
display. The submarine is still trying to display numbers by producing output on signal 
wires a through g, but those wires are connected to segments randomly. Worse, the 
wire/segment connections are mixed up separately for each four-digit display! 
(All of the digits within a display use the same connections, though.)

So, you might know that only signal wires b and g are turned on, but that doesn't 
mean segments b and g are turned on: the only digit that uses two segments is 1, so 
it must mean segments c and f are meant to be on. With just that information, you still 
can't tell which wire (b/g) goes to which segment (c/f). For that, you'll need to 
collect more information.

For each display, you watch the changing signals for a while, make a note of all ten 
unique signal patterns you see, and then write down a single four digit output 
value (your puzzle input). Using the signal patterns, you should be able to work 
out which pattern corresponds to which digit.

For example, here is what you might see in a single entry in your notes:

acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab |
cdfeb fcadb cdfeb cdbaf
(The entry is wrapped here to two lines so it fits; in your notes, 
it will all be on a single line.)

Each entry consists of ten unique signal patterns, a | delimiter, and finally the 
four digit output value. Within an entry, the same wire/segment connections are used 
(but you don't know what the connections actually are). The unique signal patterns 
correspond to the ten different ways the submarine tries to render a digit using the 
current wire/segment connections. Because 7 is the only digit that uses three 
segments, dab in the above example means that to render a 7, signal lines d, a, and b are on. 
Because 4 is the only digit that uses four segments, eafb means that to render a 4, 
signal lines e, a, f, and b are on.

Using this information, you should be able to work out which combination of signal 
wires corresponds to each of the ten digits. Then, you can decode the four digit output 
value. Unfortunately, in the above example, all of the digits in the output 
value (cdfeb fcadb cdfeb cdbaf) use five segments and are more difficult to deduce.

For now, focus on the easy digits. Consider this larger example:

be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce

Because the digits 1, 4, 7, and 8 each use a unique number of segments, you should be 
able to tell which combinations of signals correspond to those digits. Counting only 
digits in the output values (the part after | on each line), in the above example, 
there are 26 instances of digits that use a unique number of segments (highlighted above).

In the output values, how many times do digits 1, 4, 7, or 8 appear?

Your puzzle answer was 449.

--- Part Two ---
Through a little deduction, you should now be able to determine the remaining digits. 
Consider again the first example above:

acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
After some careful analysis, the mapping between signal wires and segments only make sense in the following configuration:

 dddd
e    a
e    a
 ffff
g    b
g    b
 cccc
 
So, the unique signal patterns would correspond to the following digits:

acedgfb: 8
cdfbe: 5
gcdfa: 2
fbcad: 3
dab: 7
cefabd: 9
cdfgeb: 6
eafb: 4
cagedb: 0
ab: 1

Then, the four digits of the output value can be decoded:

cdfeb: 5
fcadb: 3
cdfeb: 5
cdbaf: 3

Therefore, the output value for this entry is 5353.

Following this same process for each entry in the second, larger example above, 
the output value of each entry can be determined:

fdgacbe cefdb cefbgd gcbe: 8394
fcgedb cgb dgebacf gc: 9781
cg cg fdcagb cbg: 1197
efabcd cedba gadfec cb: 9361
gecf egdcabf bgf bfgea: 4873
gebdcfa ecba ca fadegcb: 8418
cefg dcbef fcge gbcadfe: 4548
ed bcgafe cdgba cbgef: 1625
gbdfcae bgc cg cgb: 8717
fgae cfgab fg bagce: 4315

Adding all of the output values in this larger example produces 61229.

For each entry, determine all of the wire/segment connections and decode the four-digit 
output values. What do you get if you add up all of the output values?
"""

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
