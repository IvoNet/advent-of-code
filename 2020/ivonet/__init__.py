#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:43$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

from typing import List, Callable


def get_data(infile: str) -> List:
    """Read the puzzle input without extra lines"""
    with open(infile, "r") as fi:
        return fi.read().strip().split("\n")


def consecutive_element_pairing(data: List[int],
                                consecutive_element: int = 3,
                                map_to_func: Callable = sum) -> List[int]:
    """
    Return a list with consecutively paired items given to a function that can handle an iterable
    See also: https://stackoverflow.com/questions/70186132/generic-function-for-consequtive-element-paring-by-n-given-to-a-function-with-zi
    :param data: the list of integers to process
    :param consecutive_element: how many to group consecutively
    :param map_to_func: the function to give the groups to
    :return: the new list of consecutive grouped functioned items
    """
    if len(data) < consecutive_element:
        return []
    return list(
        map(map_to_func,
            zip(*(data[i:len(data) - (consecutive_element - i) + 1] for i in range(consecutive_element)))))
