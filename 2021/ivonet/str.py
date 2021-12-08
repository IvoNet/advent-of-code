#!/usr/bin/env python
#  -*- coding: utf-8 -*-


def sort_str(txt, reverse=False) -> str:
    return "".join(sorted(txt, reverse=reverse))


def is_sorted(txt, reverse=False) -> bool:
    return txt == sort_str(txt, reverse=reverse)


def letters(txt, index=0):
    """return the indexed letter of words"""
    words = txt.split(" ")
    return ''.join([x[index] for x in words])


def str_minus_str(s1: str, s2: str):
    """s1 minus s2 only leaving in the list all the letters not in s2

    eg.
    >>> str_minus_str("acdge", "dex")
    'acg'
    >>> str_minus_str("acdge", "abdeerwerede")
    'cg'
    >>> str_minus_str("a", "ab")
    ''
    >>> str_minus_str("ab", "a")
    'b'
    """
    return "".join([x for x in s1 if x not in s2])


def str_minus_len(s1, s2):
    """calc length of str_min_str(s1, s2)

    >>> str_minus_len("acdge", "dex")
    3
    >>> str_minus_len("acdge", "abdeerwerede")
    2
    >>> str_minus_len("a", "ab")
    0
    >>> str_minus_len("ab", "a")
    1
    """
    return len(str_minus_str(s1, s2))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
