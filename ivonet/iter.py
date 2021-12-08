#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

from typing import List, Callable


def sort_dict_on_values(dct: dict) -> dict:
    """sort a dict in its values

    >>> sort_dict_on_values({1: 2, 3: 4, 4: 3, 2: 1, 0: 0})
    {0: 0, 2: 1, 1: 2, 4: 3, 3: 4}
    >>> sort_dict_on_values({'one':1,'three':3,'five':5,'two':2,'four':4})
    {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5}
    """
    return {k: v for k, v in sorted(dct.items(), key=lambda item: item[1])}


def consecutive_element_pairing(data: List,
                                consecutive_element: int = 3,
                                map_to_func: Callable = sum) -> List[int]:
    """
    Return a list with consecutively paired items given to a function that can handle an iterable
    See also: https://stackoverflow.com/questions/70186132/generic-function-for-consequtive-element-paring-by-n-given-to-a-function-with-zi

    see testcases for examples


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


def plist(lst: list):
    for x in lst:
        print(x)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
