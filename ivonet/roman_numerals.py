#!/usr/bin/env python
#  -*- coding: utf-8 -*-


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


def int_to_roman(value: int) -> str:
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


def roman_to_int(value: str) -> int:
    """Convert a Roman numeral to an integer.
    """
    if not isinstance(value, type("")):
        raise TypeError("expected string, got %s" % type(value))
    value = value.upper()
    nums = {'M': 1000, 'D': 500, 'C': 100, 'L': 50, 'X': 10, 'V': 5, 'I': 1}
    sum_total = 0
    for i in range(len(value)):
        try:
            value = nums[value[i]]
            # If the next place holds a larger number, this value is negative
            if i + 1 < len(value) and nums[value[i + 1]] > value:
                sum_total -= value
            else:
                sum_total += value
        except KeyError:
            raise ValueError('input is not a valid Roman numeral: %s' % value)
    # easiest test for validity...
    if int_to_roman(sum_total) == value:
        return sum_total
    else:
        raise ValueError('input is not a valid Roman numeral: %s' % value)


def small_int_to_roman(integer: int) -> str:
    rlist = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"),
             (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    roman_result = ""
    for whole_number in rlist:
        while integer >= whole_number[0]:
            integer -= whole_number[0]
            roman_result += whole_number[1]
    return roman_result


def big_int_to_roman(integer: int) -> str:
    thousands, rest = divmod(integer, 1000)
    return "({}){}".format(small_int_to_roman(thousands), small_int_to_roman(rest))


def int_2_roman(integer: int) -> str:
    if integer >= 4000:
        return big_int_to_roman(integer)
    else:
        return small_int_to_roman(integer)


def small_romain_to_int(numeral: str) -> int:
    rlist = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"),
             (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    index = 0
    int_result = 0
    for integer, roman_numeral in rlist:
        while numeral[index: index + len(roman_numeral)] == roman_numeral:
            int_result += integer
            index += len(roman_numeral)
    return int_result


def romain_2_int(numeral: str) -> int:
    assert len(numeral) > 0, "Numerals should not be empty"
    int_parts = numeral[1:].split(')')  # Better done with regex
    if len(int_parts) == 1:
        return small_romain_to_int(numeral)
    elif len(int_parts) == 2:
        big = small_romain_to_int(int_parts[1])
        small = small_romain_to_int(int_parts[0])
        if big is None or small is None:
            raise ValueError("Could not convert")
        else:
            return big * 1000 + small
    else:
        raise ValueError("Could not convert")


if __name__ == '__main__':
    print(roman(2018))
    print(roman("MMXVIII"))
    print(int_2_roman(5555))
    print(ToRoman(2018))
