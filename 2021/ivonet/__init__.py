#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:43$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

__all__ = [
    "calc",
    "iter_tools",
]


def read_data(infile: str) -> str:
    """Read the puzzle input without extra lines"""
    with open(infile, "r") as fi:
        return fi.read().strip()


def get_data(infile: str) -> list:
    """Read the puzzle input without extra lines"""
    with open(infile, "r") as fi:
        return fi.read().strip().split("\n")


def plist(lst: list):
    for x in lst:
        print(x)


def sort_str(s: str):
    return "".join(sorted(s))
