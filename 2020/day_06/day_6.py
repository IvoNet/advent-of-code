#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
##############################################################################
# Part 1
##############################################################################

##############################################################################
# Part 2
##############################################################################

"""

from ivonet.files import read_data


class Group(object):

    def __init__(self, data: str) -> None:
        self.data = data
        self.group_answers = data.strip().split("\n")
        self.member_count = len(self.group_answers)
        self.combined_answers = set(list("".join(self.group_answers)))
        self.count = len(self.combined_answers)
        self.intersection = set(self.group_answers[0]).intersection(*self.group_answers)
        self.intersection_count = len(self.intersection)


def part_1_2(data):
    groups = data.split("\n\n")
    converted_groups = list(map(Group, groups))
    count = sum(i.count for i in converted_groups)
    intersection_count = sum(i.intersection_count for i in converted_groups)
    return count, intersection_count


if __name__ == '__main__':
    source = read_data("day_6.txt")
    print(part_1_2(source)[0])
    print(part_1_2(source)[1])
