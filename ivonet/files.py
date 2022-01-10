#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 08/12/2021 15:04$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import sys
import urllib.request
from io import StringIO

from ivonet.iter import lmap


def open_anything(source: any):
    """URI, filename, or string --> stream

    This function lets you define parsers that take any input source
    (URL, pathname to local or network file, or actual data as a string)
    and deal with it in a uniform manner.  Returned object is guaranteed
    to have all the basic stdio read methods (read, readline, readlines).
    Just .close() the object when you're done with it.
    """

    if hasattr(source, "read"):
        return source

    if source == "-":
        return sys.stdin

    # try to open with urllib (if source is http, ftp, or file URL)

    try:
        return urllib.request.urlopen(source)
    except (IOError, OSError, ValueError):
        pass

    # try to open with native open function (if source is pathname)
    try:
        return open(source, 'r')
    except (IOError, OSError):
        pass

    # treat source as string
    return StringIO(str(source))


def read_data(infile: str) -> str:
    """Read the puzzle input without extra lines"""
    with open_anything(infile) as fi:
        return fi.read().strip()


def read_rows(infile: str) -> list[str]:
    """Read the puzzle input without extra lines"""
    return read_data(infile).strip().split("\n")


def read_ints(infile: str, delimiter: str = "\n") -> list[int]:
    """Read the infile and parse it into a list of ints based on the delimiter"""
    return list(map(int, read_data(infile).strip().split(delimiter)))


def read_int_matrix(infile: str) -> list[list[int]]:
    """Read an infile of the following format into a matrix of ints (list of lists)
    e.g.
    219
    398
    985

    It can handle file reference and string input

    >>> read_int_matrix('''219
    ... 398
    ... 985
    ... 876''')
     [[2, 1, 9], [3, 9, 8], [9, 8, 5], [8, 7, 6]]
    """
    return [lmap(int, list(x)) for x in read_rows(infile)]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
