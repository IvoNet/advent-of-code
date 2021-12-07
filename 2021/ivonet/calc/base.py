#!/usr/bin/env python
#  -*- coding: utf-8 -*-


def ternary(n):
    """
    Calculates ternary result from a decimal number.
    https://en.wikipedia.org/wiki/Ternary_numeral_system
    http://www.unitconversion.org/numbers/base-3-conversion.html
    http://www.unitconversion.org//unit_converter/numbers-ex.html

    deprecated use base_3
    """
    if n == 0:
        return '0'
    nums = []
    while n:
        n, r = divmod(n, 3)
        nums.append(str(r))
    return ''.join(reversed(nums))


def base_10_to_base_x(value, base=3):
    return str(int(str(value), base=base))


def base_3(value):
    """"Calculates base-3 / ternary from a decimal number"""
    return base_10_to_base_x(value, 3)


def base_x_to_10(value, base=3):
    string = str(value)[::-1]
    ret = 0
    for idx, x in enumerate(string):
        ret += (base ** idx) * int(x)
    return ret


def binary_8_bits(value) -> list:
    bin = []
    if type(value) == int:
        bin.append("{0:b}".format(value).zfill(8))
        return bin
    for x in value:
        bin.append("{0:b}".format(ord(x)).zfill(8))
    return bin


if __name__ == '__main__':
    print(binary_8_bits(2))
    print(binary_8_bits("FDWJDIIH"))
    for x in binary_8_bits("FDWJDIIH"):
        for y in x:
            print(y, end=" ")
        print()
