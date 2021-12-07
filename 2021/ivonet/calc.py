#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"


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


if __name__ == '__main__':
    import doctest

    doctest.testmod()
