#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 08/12/2021 15:04$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""


def read_data(infile: str) -> str:
    """Read the puzzle input without extra lines"""
    with open(infile, "r") as fi:
        return fi.read().strip()


def read_rows(infile: str) -> list:
    """Read the puzzle input without extra lines"""
    return read_data(infile).split("\n")
