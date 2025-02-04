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


def gcd(a, b):
    """
    Calculate the greatest common divisor (GCD) of two numbers using
    the Euclidean algorithm.
    https://en.wikipedia.org/wiki/Euclidean_algorithm
    :param a: The first number.
    :param b: The second number.
    :return: The GCD of a and b.
    """
    while b != 0:
        a, b = b, a % b
    return a


def lcm(a, b):
    """
    Calculate the least common multiple (LCM) of two numbers.
    :param a: The first number.
    :param b: The second number.
    :return: The LCM of a and b.
    """
    return abs(a * b) // gcd(a, b)


def lcm_list(numbers: list[int]):
    """
     Calculate the least common multiple (LCM) of a list of numbers.
     :param numbers: The list of numbers.
     :return: The LCM of the numbers in the list.
     """
    if not numbers:
        return 0
    if len(numbers) == 1:
        return numbers[0]
    result = numbers[0]
    for number in numbers[1:]:
        result = lcm(result, number)
    return result


def prod(*iterable) -> float:
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
    >>> prod((1, 83, 101, 103, 107, 113))
    10439961859
    >>> prod({1, 2, 3, 4})
    24
    >>> prod({'a': 7, "b": 6})
    42
    >>> prod(len(x) for x in ['aaaaa', 'aa', 'asdf'])
    40
    """
    it = iterable
    if len(it) == 1:
        if type(it[0]) in [list, set, tuple] or isinstance(it[0], types.GeneratorType):
            it = it[0]
        elif type(it[0]) == dict:
            it = list(it[0].values())
    return reduce(lambda a, b: a * b, it, 1)


def fibonacci(n: int) -> int:
    """Calculated value of the fibonacci sequence

    Difficult to understand but very fast in execution

    >>> fibonacci(5)
    5
    """
    return int(((1 + sqrt(5)) ** n - (1 - sqrt(5)) ** n) / (2 ** n * sqrt(5)))


def fib(n: int) -> int:
    """Iterative approach to the fibonacci sequence

    :param n: number of fib iterations
    :return: fib int

    >>> fib(5)
    5
    """
    if n == 0:
        return 0
    last = 0
    following = 1
    for _ in range(1, n):
        last, following = following, last + following
    return following


def step_sequence_calc(end: int, start: int = 1) -> int:
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


def base_10_to_base_x(value, base=3):
    return str(int(str(value), base=base))


def base_3(value: int):
    """"Calculates base-3 / ternary from a decimal number"""
    return base_10_to_base_x(value, 3)


def base_x_to_10(value: str, base: int = 3) -> int:
    string = str(value)[::-1]
    ret = 0
    for idx, x in enumerate(string):
        ret += (base ** idx) * int(x)
    return ret


def binary(value, bit_len=8) -> list:
    bits = []
    if type(value) == int:
        bits.append("{0:b}".format(value).zfill(bit_len))
        return bits
    for x in value:
        bits.append("{0:b}".format(ord(x)).zfill(bit_len))
    return bits


if __name__ == '__main__':
    import doctest

    doctest.testmod()
