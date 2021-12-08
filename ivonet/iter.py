#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import re


def lmap(func, *iterables):
    """list of map to func on iterables

    >>> lmap(int, {1:'a', 3:'b'})
    [1, 3]
    >>> lmap(int, "12345")
    [1, 2, 3, 4, 5]
    >>> lmap(lambda x: x*x, lmap(int, "123456789"))
    [1, 4, 9, 16, 25, 36, 49, 64, 81]
    """
    return list(map(func, *iterables))


def min_max(lst: list):
    """Get the min and the max of a list

    >>> min_max([9,5,6,7,8,1,2,3,1])
    (1, 9)
    """
    return min(lst), max(lst)


def max_minus_min(lst: list):
    """return the max - min of a list

    >>> max_minus_min([1,10,6])
    9
    """
    return max(lst) - min(lst)


def list_diff(lst: list[int]):
    """Calculate the diff of consecutive elements of a list of int

    >>> list_diff([1,2,3,4,5,6])
    [1, 1, 1, 1, 1]
    >>> list_diff([1,0,2,9,3,8,4,7,5,6])
    [-1, 2, 7, -6, 5, -4, 3, -2, 1]
    """
    return [b - a for a, b in zip(lst, lst[1:])]


def flatten(lst: list[list]):
    """Flatten a list of lists

    >>> flatten([[0,3],[6,6,6,6],[9,1],[0]])
    [0, 3, 6, 6, 6, 6, 9, 1, 0]
    """
    return [i for x in lst for i in x]


def ints(s: str) -> list[int]:
    return lmap(int, re.findall(r"-?\d+", s))


def positive_ints(s: str) -> list[int]:
    return lmap(int, re.findall(r"\d+", s))


def floats(s: str) -> list[float]:
    return lmap(float, re.findall(r"-?\d+(?:\.\d+)?", s))


def positive_floats(s: str) -> list[float]:
    """Parse positive floats out of a string"""
    return lmap(float, re.findall(r"\d+(?:\.\d+)?", s))


def words(s: str) -> list[str]:
    """Bad implementation of finding words in a string"""
    return re.findall(r"[a-zA-Z]+", s)


def keyvalues(d: dict) -> list[tuple]:
    """Convert a dict into a list of [(key, value),...]

    >>> keyvalues({1:'a', 3:'b'})
    [(1, 'a'), (3, 'b')]
    """
    return list(d.items())


def sort_dict_on_values(dct: dict) -> dict:
    """sort a dict in its values

    >>> sort_dict_on_values({1: 2, 3: 4, 4: 3, 2: 1, 0: 0})
    {0: 0, 2: 1, 1: 2, 4: 3, 3: 4}
    >>> sort_dict_on_values({'one':1,'three':3,'five':5,'two':2,'four':4})
    {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5}
    """
    return {k: v for k, v in sorted(dct.items(), key=lambda item: item[1])}


def consecutive_element_pairing(data: list,
                                consecutive_element: int = 3,
                                map_to_func: callable = sum) -> list[int]:
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
