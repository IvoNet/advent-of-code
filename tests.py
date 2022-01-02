#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 02/01/2022 17:47$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import os
import pkgutil
import unittest
from pathlib import Path

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


EXCLUDE = [
    ".pytest_cache",
    "__pycache__",
    ".ipynb_checkpoints",
    "venv",
    "out",
    "lib",
    ".idea",
    ".tmp",
]

__path__ = [x[0] for x in os.walk(os.path.dirname(__file__))]

for x in EXCLUDE:
    for f in __path__[:]:
        if x in f:
            __path__.remove(f)


def exclude():
    return [
        Path(__file__).name[:-3],
        "template",
        "aoc_input"
    ]


def load_tests(loader, suite, pattern):
    """https://stackoverflow.com/questions/29713541/recursive-unittest-discover"""
    total = 0
    for imp, modname, b in pkgutil.walk_packages(__path__):
        if modname in exclude():
            continue
        mod = imp.find_module(modname).load_module(modname)
        for test in loader.loadTestsFromModule(mod):
            _(f"Found Tests in {mod}: {test._tests}")
            suite.addTests(test)
            total += len(test._tests)
    print("=" * 80)
    print(f"Running {total} tests")
    print("=" * 80)
    return suite


if __name__ == '__main__':
    unittest.main(verbosity=3, failfast=False)
