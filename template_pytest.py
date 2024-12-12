#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2023 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
If a part of the code is not part of the post it is probably 
code I found reusable and I may have moved it to my 'ivonet' library.
you can find that here: https://github.com/IvoNet/advent-of-code/tree/master/ivonet
"""

import collections
import os
from pathlib import Path

from ivonet.decorators import timer

collections.Callable = collections.abc.Callable

import sys
import pytest
from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


@timer
def part_1(source):
    return None


@timer
def part_2(source):
    return None


def test_puzzle(test_source, source):
    assert part_1(test_source) == None
    assert part_1(source) == None
    assert part_2(test_source) == None
    assert part_2(source) == None


@pytest.fixture
def day():
    return str(ints(Path(__file__).name)[0])


@pytest.fixture
def source(day):
    return read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")


@pytest.fixture
def test_source(day):
    return read_rows(f"{os.path.dirname(__file__)}/test_{day.zfill(2)}.input")
