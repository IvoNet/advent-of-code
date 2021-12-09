#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 08/12/2021 15:17$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import types
from functools import reduce
from math import sqrt

import numpy as np


def prod(*iterable):
    """Like sum() but then for the product of an iterable
    If a dict is provided the product of the values is calculated.

    It can handle a generator, list, single parameters that can
    be counted as iterable.
    See the examples below:
    >>> prod(1,2,3)
    6
    >>> prod('a',10)
    'aaaaaaaaaa'
    >>> prod([1, 2, 3, 4])
    24
    >>> prod({1, 2, 3, 4})
    24
    >>> prod({'a': 7, "b": 6})
    42
    >>> prod(len(x) for x in ['aaaaa', 'aa', 'asdf'])
    40
    """
    it = iterable
    if len(it) == 1:

        if type(it[0]) == list or type(it[0]) == set or isinstance(it[0], types.GeneratorType):
            it = it[0]
        elif type(it[0]) == dict:
            it = it[0].values()
    return reduce(lambda a, b: a * b, it, 1)


def fibonacci(n):
    """Calculated value of the fibonacci sequence

    Difficult to understand but very fast in execution
    """
    return int(((1 + sqrt(5)) ** n - (1 - sqrt(5)) ** n) / (2 ** n * sqrt(5)))


def step_sequence_calc(end, start=1):
    """Optimized formula for 1+2+3+4+5...

   S= 10 + 9 +  8 +  7 +  6 +  5 +  4 +  3 +  2 +  1
   S=  1 + 2 +  3 +  4 +  5 +  6 +  7 +  8 +  9 + 10
    ------------------------------------------------- +
      11 + 11 + 11 + 11 + 11 + 11 + 11 + 11 + 11 + 11

   so 2S = 10 * 11 = 110
       S = 110 / 2 = 55


    >>> step_sequence_calc(3)
    6
    >>> step_sequence_calc(10)
    55
    >>> step_sequence_calc(6, 3)
    18
    """

    return int((end - start + 1) * (end + start) / 2)


def normalize_overlap_matrix(mtrx):
    """
    Normalizes a numpy matrix used for overlap matrices,
    by dividing every element A_ij by sqrt(A_ii)*sqrt(A_jj)
    """
    assert isinstance(mtrx, np.ndarray), 'Input shall be a numpy array'
    assert np.isreal(mtrx).all(), 'Numpy array shall contain real numbers'
    assert mtrx.shape[0] == mtrx.shape[1], 'Overlap matrix shall be square'
    assert (np.diag(mtrx) != 0).all(), 'Overlap matrix shall not have 0 on its diagonal'

    b = np.sqrt(np.diag(mtrx))
    result = ((mtrx / b).T / b).T

    return result


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
    bits = []
    if type(value) == int:
        bits.append("{0:b}".format(value).zfill(8))
        return bits
    for x in value:
        bits.append("{0:b}".format(ord(x)).zfill(8))
    return bits


def tests():
    print(binary_8_bits(2))
    print(binary_8_bits("FDWJDIIH"))
    for x in binary_8_bits("FDWJDIIH"):
        for y in x:
            print(y, end=" ")
        print()


if __name__ == '__main__':
    import doctest

    doctest.testmod()
