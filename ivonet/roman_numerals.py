#!/usr/bin/env python
#  -*- coding: utf-8 -*-


from collections import OrderedDict


def write_roman(num):
    """A implementation for converting to roman
    @deprecated
    """
    roman = OrderedDict()
    roman[1000] = "M"
    roman[900] = "CM"
    roman[500] = "D"
    roman[400] = "CD"
    roman[100] = "C"
    roman[90] = "XC"
    roman[50] = "L"
    roman[40] = "XL"
    roman[10] = "X"
    roman[9] = "IX"
    roman[5] = "V"
    roman[4] = "IV"
    roman[1] = "I"

    def roman_num(num):
        for r in roman.keys():
            x, y = divmod(num, r)
            yield roman[r] * x
            num -= (r * x)
            if num > 0:
                roman_num(num)
            else:
                break

    return "".join([a for a in roman_num(num)])


class ToRoman(int):
    def __new__(cls, number):
        if number > 3999:
            raise ValueError('Values over 3999 are not allowed: {}'.format(number))
        if number < 0:
            raise ValueError('Negative values are not allowed: {}'.format(number))
        return super().__new__(cls, number)

    def __init__(self, number):
        super().__init__()
        to_roman = {1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V',
                    6: 'VI', 7: 'VII', 8: 'VIII', 9: 'IX', 10: 'X', 20: 'XX',
                    30: 'XXX', 40: 'XL', 50: 'L', 60: 'LX', 70: 'LXX', 80: 'LXXX',
                    90: 'XC', 100: 'C', 200: 'CC', 300: 'CCC', 400: 'CD', 500: 'D',
                    600: 'DC', 700: 'DCC', 800: 'DCCC', 900: 'CM', 1000: 'M',
                    2000: 'MM', 3000: 'MMM'}
        self.roman = ''.join([to_roman.get(num) for num in self][::-1])

    def __iter__(self):
        number = self.__str__()
        count = 1
        for digit in number[::-1]:
            if digit != '0':
                yield int(digit) * count
            count *= 10


class ToArabic(str):
    def __init__(self, roman):
        super().__init__()
        roman = self.check_valid(roman)
        keys = ['IV', 'IX', 'XL', 'XC', 'CD', 'CM', 'I', 'V', 'X', 'L', 'C', 'D', 'M']
        to_arabic = {'IV': '4', 'IX': '9', 'XL': '40', 'XC': '90', 'CD': '400', 'CM': '900',
                     'I': '1', 'V': '5', 'X': '10', 'L': '50', 'C': '100', 'D': '500', 'M': '1000'}
        for key in keys:
            if key in roman:
                roman = roman.replace(key, ' {}'.format(to_arabic.get(key)))
        self.arabic = sum(int(num) for num in roman.split())

    def check_valid(self, roman):
        roman = roman.upper()
        invalid = ['IIII', 'VV', 'XXXX', 'LL', 'CCCC', 'DD', 'MMMM']
        if any(sub in roman for sub in invalid):
            raise ValueError('Numerus invalidus est: {}'.format(roman))
        return roman


def roman(number):
    """
    convenience method converting either to or from roman numerals.
    if input is an int -> roman
    else -> int
    """
    if isinstance(number, int):
        return ToRoman(number).roman
    return ToArabic(number).arabic


def int_to_roman(value):
    """
    Convert an integer to a Roman numeral.
    """

    if not isinstance(value, type(1)):
        raise TypeError("expected integer, got %s" % type(value))
    if not 0 < value < 4000:
        raise ValueError("Argument must be between 1 and 3999")
    ints = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    nums = ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
    result = []
    for i in range(len(ints)):
        count = int(value / ints[i])
        result.append(nums[i] * count)
        value -= ints[i] * count
    return ''.join(result)


def roman_to_int(value):
    """
    Convert a Roman numeral to an integer.
    """
    if not isinstance(value, type("")):
        raise TypeError("expected string, got %s" % type(value))
    value = value.upper()
    nums = {'M': 1000, 'D': 500, 'C': 100, 'L': 50, 'X': 10, 'V': 5, 'I': 1}
    sum = 0
    for i in range(len(value)):
        try:
            value = nums[value[i]]
            # If the next place holds a larger number, this value is negative
            if i + 1 < len(value) and nums[value[i + 1]] > value:
                sum -= value
            else:
                sum += value
        except KeyError:
            raise ValueError('input is not a valid Roman numeral: %s' % value)
    # easiest test for validity...
    if int_to_roman(sum) == value:
        return sum
    else:
        raise ValueError('input is not a valid Roman numeral: %s' % value)


def small_int_to_roman(integer):
    rlist = romanList = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"),
                         (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    romanResult = ""
    for wholeNumber in rlist:
        while integer >= wholeNumber[0]:
            integer -= wholeNumber[0]
            romanResult += wholeNumber[1]
    return romanResult


def big_int_to_roman(integer):
    thousands, rest = divmod(integer, 1000)
    return "({}){}".format(small_int_to_roman(thousands), small_int_to_roman(rest))


def int_2_roman(integer):
    if integer >= 4000:
        return big_int_to_roman(integer)
    else:
        return small_int_to_roman(integer)


def small_romain_to_int(numeral):
    rlist = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"),
             (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    index = 0
    intResult = 0
    for integer, romanNumeral in rlist:
        while numeral[index: index + len(romanNumeral)] == romanNumeral:
            intResult += integer
            index += len(romanNumeral)
    return intResult


def romain_2_int(numeral):
    if len(numeral) == 0:
        return None
    int_parts = numeral[1:].split(')')  # Better done with regex
    if len(int_parts) == 1:
        return small_romain_to_int(numeral)
    elif len(int_parts) == 2:
        big = small_romain_to_int(int_parts[1])
        small = small_romain_to_int(int_parts[0])
        if big is None or small is None:
            return None
        else:
            return big * 1000 + small
    else:
        return None


if __name__ == '__main__':
    print(write_roman(2018))
    print(roman(2018))
    print(roman("MMXVIII"))
    print(int_2_roman(5555))
    print(ToRoman(2018))
    # wb = Woordenboek()  # and wb.is_word(int_2_roman(x).replace(")", "").replace("(", ""))
    # [print(int_2_roman(x)) for x in range(3999, 5500)]
    # [print(int_2_roman(x)) for x in range(1, 1000000) if len(int_2_roman(x).replace(")", "").replace("(", "")) == 5]
