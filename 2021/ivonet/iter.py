#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import unittest
from typing import List, Callable


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


def printlist(lst: list):
    for x in lst:
        print(x)


class UnitTests(unittest.TestCase):
    def test_consecutive_element_paring(self):
        self.assertEqual(consecutive_element_pairing([1, 2, 3, 4, 5, 6], consecutive_element=7, map_to_func=list), [])
        self.assertEqual(consecutive_element_pairing([1, 2, 3, 4, 5, 6], consecutive_element=3, map_to_func=list),
                         [[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]])
        # first pair to the list ^^^ then sum the the separate sub lists and make that into a list
        self.assertEqual(consecutive_element_pairing([1, 2, 3, 4, 5, 6], consecutive_element=3, map_to_func=sum),
                         [6, 9, 12, 15])
        self.assertEqual(
            consecutive_element_pairing([1, 2, 3, 4, 5, 6], consecutive_element=3,
                                        map_to_func=lambda z: "".join([str(x) for x in z])),
            ['123', '234', '345', '456'])


if __name__ == '__main__':
    unittest.main()
