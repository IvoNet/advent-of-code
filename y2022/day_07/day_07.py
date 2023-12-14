#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2022 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
If a part of the code is not part of the post it is probably 
code I found reusable and I may have moved it to my 'ivonet' library.
you can find that here: https://github.com/IvoNet/advent-of-code/tree/master/ivonet
"""

import os
import sys
import unittest
from collections import defaultdict
from pathlib import Path

from ivonet import infinite
from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def end_slash(path):
    if path.endswith("/"):
        return path
    return path + "/"


def add_dir(current_dir: str, new_dir: str) -> str:
    """Create a new absolute path"""
    return end_slash(current_dir) + new_dir


def sub_dir(current_dir: str) -> str:
    """Remove the last directory from the path"""
    return "/".join(current_dir.split("/")[:-1])


def update_directory_sizes(directories: dict, current_dir: str, size: int) -> dict:
    """A size is added to all directories in the path"""
    dirs = directories.copy()
    paths = current_dir.split("/")
    if current_dir == "/":
        paths = [""]
    cd = ""
    for directory in paths:
        cd = add_dir(cd, directory)
        dirs[cd] += size
    return dirs


def parse_dos_commands(source):
    """Parses the commands and maintains a dict of fully qualified directories and their sizes"""
    directories = defaultdict(int)
    current_dir = ""
    for line in source:
        work = line.split(" ")
        if line.startswith("$"):
            if work[1] == "cd":
                if work[-1] == "/":
                    current_dir = "/"
                    continue
                if work[-1] == "..":
                    current_dir = sub_dir(current_dir)
                    continue
                current_dir = add_dir(current_dir, work[-1])
                continue
            if work[1] == "ls":
                continue
        if work[0] == "dir":
            directories[add_dir(current_dir, work[1])] += 0
            continue
        int_work = ints(work[0])
        if int_work:
            int_work = int_work[0]
            directories = update_directory_sizes(directories, current_dir, int_work)
            continue
    return directories


def part_1(source, max_size=100000):
    directories = parse_dos_commands(source)
    return sum(x for x in directories.values() if x <= max_size)


def part_2(source, system_size=70000000, size_needed_for_update=30000000):
    directories = parse_dos_commands(source)
    currently_free = system_size - directories["/"]
    smallest = infinite
    for value in directories.values():
        if currently_free + value > size_needed_for_update:
            if smallest > value:
                smallest = value
    return smallest


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k""")

    def test_example_data_part_1(self):
        self.assertEqual(95437, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(1232307, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(24933642, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(7268994, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
