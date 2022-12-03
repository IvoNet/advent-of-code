#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import re
from collections import defaultdict
from typing import Generator, Sized, Callable, Iterable


def rangei(start, end, step=1):
    """Inclusive, range from start to end: rangei(a, b) = range(a, b+1).
    """
    return range(start, end + 1, step)


def lmap(fn, *iterables):
    """list of map to func on iterables

    >>> lmap(int, {1:'a', 3:'b'})
    [1, 3]
    >>> lmap(int, "12345")
    [1, 2, 3, 4, 5]
    >>> lmap(lambda x: x*x, lmap(int, "123456789"))
    [1, 4, 9, 16, 25, 36, 49, 64, 81]
    """
    return list(map(fn, *iterables))


def tmap(fn, *iterables):
    """Do a map, and make the results into a tuple."""
    return tuple(map(fn, *iterables))


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


def max_2d(matrix: list[list[int]]):
    """Find the max in a 2D matrix of ints

    >>> max_2d([[1,2],[1,3],[42,1,42,3,4,5]])
    42
    """
    return max(map(max, matrix))


def quantify(iterable: Iterable, pred: Callable = bool):
    """Count how many items in iterable have pred(item) true.
    >>> quantify([4,3,2,True,7,8,False], lambda x: x is True)
    1
    >>> quantify([4,3,2,True,7,8,False])
    6
    >>> quantify([4,3,2,True,7,8,False, 3], pred=lambda x: x == 3)
    2
    """
    return sum(map(pred, iterable))


def flatten(lst: Iterable[Iterable]):
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


def max_idx(inputlist: list[list[int]], idx=0):
    return max([sublist[idx] for sublist in inputlist])


def keyvalues(d: dict) -> list[tuple]:
    """Convert a dict into a list of [(key, value),...]

    >>> keyvalues({1:'a', 3:'b'})
    [(1, 'a'), (3, 'b')]
    """
    return list(d.items())


def chunkify(iterable, length=2):
    """Chunkify a string into a list of chunk length sizes

    >>> chunkify("abcdefghijklmnopqrstuvwxyz", 5)
    ['abcde', 'fghij', 'klmno', 'pqrst', 'uvwxy', 'z']
    >>> chunkify("(){}[]<>")
    ['()', '{}', '[]', '<>']
    >>> chunkify(list("(){}[]<>"))
    [['(', ')'], ['{', '}'], ['[', ']'], ['<', '>']]
    """
    return [iterable[i:i + length] for i in range(0, len(iterable), length)]


def dictify(iterable):
    """Create a dict form an iterable.

    >>> dictify("(){}[]<>")
    {'(': ')', '{': '}', '[': ']', '<': '>'}
    >>> dictify("(){}[]<")
    Traceback (most recent call last):
    AssertionError: iterable should have a multiplication of len 2 but has len 7.
    """
    assert iterable, "Iterable should have value."
    assert len(iterable) % 2 == 0, f"iterable should have a multiplication of len 2 but has len {len(iterable)}."
    ret = {}
    for k, v in chunkify(iterable, length=2):
        ret[k] = v
    return ret


def groupify(iterable, group_size: int = 2) -> list[list]:
    """Groupify a string into a list of chunk length sizes

    >>> groupify("abcdefghijklmnopqrstuvwxyz", 5)
    ['abcde', 'fghij', 'klmno', 'pqrst', 'uvwxy', 'z']
    >>> groupify("(){}[]<>")
    ['()', '{}', '[]', '<>']
    >>> groupify(list("(){}[]<>"))
    [['(', ')'], ['{', '}'], ['[', ']'], ['<', '>']]
    """
    #
    return [iterable[i:i + group_size] for i in range(0, len(iterable), group_size)]


def groupify_as_lists(iterable, group_size: int = 2) -> list[list]:
    """Groupify a string into a list of chunk length sizes

    >>> groupify_as_lists("abcdefghijklmnopqrstuvwxyz", 5)
    [('a', 'b', 'c', 'd', 'e'), ('f', 'g', 'h', 'i', 'j'), ('k', 'l', 'm', 'n', 'o'), ('p', 'q', 'r', 's', 't'), ('u', 'v', 'w', 'x', 'y')]
    >>> groupify_as_lists("(){}[]<>")
    [('(', ')'), ('{', '}'), ('[', ']'), ('<', '>')]
    >>> groupify_as_lists(list("(){}[]<>"))
    [('(', ')'), ('{', '}'), ('[', ']'), ('<', '>')]
    """
    return list(zip(*(iter(iterable),) * group_size))


def multimap(items):
    """Given (key, val) pairs, return {key: [val, ....], ...}.
    >>> multimap([("a", "b"),("a", "c"),("a", "d"),("b", "a"),("b", "c"),])
    defaultdict(<class 'list'>, {'a': ['b', 'c', 'd'], 'b': ['a', 'c']})
    """
    result = defaultdict(list)
    for (key, val) in items:
        result[key].append(val)
    return result


def list_middle(inlist: list[int]) -> any:
    """Return the middle int value of the sorted list

    >>> list_middle([1, 3, 2])
    2
    >>> list_middle([1, 3, 2, 9])
    Traceback (most recent call last):
    AssertionError: The list should contain an uneven amount of items
    """
    assert len(inlist) % 2 == 1, "The list should contain an uneven amount of items"
    return sorted(inlist)[len(inlist) // 2]


def sort_dict_on_values(dct: dict, reverse: bool = False, key=lambda x: x[1]) -> dict:
    """Sort a dict in its values but stay the same dict

    >>> sort_dict_on_values({1: 2, 3: 4, 4: 3, 2: 1, 0: 0})
    {0: 0, 2: 1, 1: 2, 4: 3, 3: 4}
    >>> sort_dict_on_values({'one':1,'three':3,'five':5,'two':2,'four':4})
    {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5}
    """
    return {k: v for k, v in sorted(dct.items(), key=key, reverse=reverse)}


def make_hashable(iterable):
    """Make the iterable hashable.
    Useful when using it as a key.
    """
    if isinstance(iterable, list):
        return tuple(map(make_hashable, iterable))
    if isinstance(iterable, dict):
        iterable = set(iterable.items())
    if isinstance(iterable, set):
        return frozenset(map(make_hashable, iterable))
    return iterable


def invert_dict(dct: dict, single=True, verbose=True):
    """Values become the keys and keys the values.
    They will be made hashable if they are not yet so.

    >>> invert_dict({1: 2, 9: 0})
    {2: 1, 0: 9}
    >>> invert_dict({1: 2, 9: 0, 3: 2})
    [invert_dict] WARNING WARNING: duplicate key 2
    {2: 3, 0: 9}
    >>> invert_dict({1: 2, 9: 0, 3: 2}, verbose=False)
    {2: 3, 0: 9}
    >>> invert_dict({1: 2, 9: [0, 3, 4], 3: 2, 'a': {4: 2, 2: 4}}, single=False, verbose=False)
    {2: [1, 3], (0, 3, 4): [9], frozenset({(2, 4), (4, 2)}): ['a']}
    >>> invert_dict({1: 2, 9: [0, 3, 4], 3: 2, 'a': {4: 2, 2: 4}})
    [invert_dict] WARNING WARNING: duplicate key 2
    {2: 3, (0, 3, 4): 9, frozenset({(2, 4), (4, 2)}): 'a'}
    """
    out = {}
    for k, v in dct.items():
        v = make_hashable(v)
        if v in out and verbose:
            print("[invert_dict] WARNING WARNING: duplicate key", v)
        if single:
            out[v] = k
        else:
            out.setdefault(v, []).append(k)
    return out


def consecutive_element_pairing(data: Sized,
                                elements: int = 3,
                                map_to_func: callable = list) -> list[any]:
    """
    Return a list with consecutively paired items given to a function that can handle an iterable
    See also: https://stackoverflow.com/questions/70186132/generic-function-for-consequtive-element-paring-by-n-given-to-a-function-with-zi

    see testcases for examples


    :param data: the list of integers to process
    :param elements: how many to group consecutively
    :param map_to_func: the function to give the groups to
    :return: the new list of consecutive grouped functioned items
    """
    if len(data) < elements:
        return []
    return list(map(map_to_func, zip(*(data[i:len(data) - (elements - i) + 1] for i in range(elements)))))


def combinations(a, n):
    if n == 1:
        for x in a:
            yield [x]
    else:
        for i in range(len(a)):
            for x in combinations(a[:i] + a[i + 1:], n - 1):
                yield [a[i]] + x


def permutations(a):
    return combinations(a, len(a))


def rotate(li: list, by):
    """Rotates a list by however much you want.
    rotates means wraparound
    """
    return li[-by % len(li):] + li[:-by % len(li)]


def four_way_split(n: int, first: int = 1, inclusive: bool = False) -> Generator:
    """Yields a new 4 way split of the number provided as n"""
    addition = 0
    if inclusive:
        addition = 1
    for i in range(first, n + addition):
        for j in range(i, n + addition):
            for k in range(j, n + addition):
                for l in range(k, n + addition):
                    if i + j + k + l == n:
                        if i == j == k == l:
                            yield i, j, k, l
                            continue
                        for a, b, c, d in permutations((i, j, k, l)):
                            yield a, b, c, d


def zip_list(iterable):
    """Zip with list output instead of tuple"""
    return list(map(list, zip(*iterable)))


def pretty(iterable, sort_keys=True, indent=2):
    """Pretty print an iterable
    >>> pretty([1,2,3])
    [
      1,
      2,
      3
    ]
    >>> pretty({3:'a', 1:'b'})
    {
      "1": "b",
      "3": "a"
    }
    >>> pretty({3:'a', 1:'b'}, sort_keys=False)
    {
      "3": "a",
      "1": "b"
    }
    >>> pretty({3:'a', 1: [1,2,]}, indent=4)
    {
        "1": [
            1,
            2
        ],
        "3": "a"
    }
    """
    import json
    print(json.dumps(iterable, sort_keys=sort_keys, indent=indent, default=str))


def print_2d(matrix, width=1):
    for h in matrix:
        for w in h:
            print(f"{w:<{width}}", end="")
        print()
    print()


if __name__ == '__main__':
    import doctest

    doctest.testmod()
