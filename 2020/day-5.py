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

For example, consider just the first seven characters of FBFBBFFRLR:

Start by considering the whole range, rows 0 through 127.
F means to take the lower half, keeping rows 0 through 63.
B means to take the upper half, keeping rows 32 through 63.
F means to take the lower half, keeping rows 32 through 47.
B means to take the upper half, keeping rows 40 through 47.
B keeps rows 44 through 47.
F keeps rows 44 through 45.
The final F keeps the lower of the two, row 44.

The last three characters will be either L or R; these specify exactly one 
of the 8 columns of seats on the plane (numbered 0 through 7). The same 
process as above proceeds again, this time with only three steps. L means 
to keep the lower half, while R means to keep the upper half.

For example, consider just the last 3 characters of FBFBBFFRLR:

Start by considering the whole range, columns 0 through 7.
R means to take the upper half, keeping columns 4 through 7.
L means to take the lower half, keeping columns 4 through 5.
The final R keeps the upper of the two, column 5.

So, decoding FBFBBFFRLR reveals that it is the seat at row 44, column 5.

Every seat also has a unique seat ID: multiply the row by 8, then add the 
column. In this example, the seat has ID 44 * 8 + 5 = 357.
##############################################################################
# Part 2
##############################################################################

"""

from ivonet import get_data

ROWS = list(range(128))
COLLUMS = list(range(8))


def split_middle(rows):
    middle_index = len(rows) // 2
    left = rows[:middle_index]
    right = rows[middle_index:]
    return left, right


def part_1(data):
    seats = []
    highest_seat = 0
    # data = ["BFFFBBFRRR", "FFFBBBFRRR", "BBFFBBFRLL"]
    for seat in data:
        rows = ROWS.copy()
        for row in seat[:7]:
            front, back = split_middle(rows)
            if row == "F":
                rows = front
            else:
                rows = back
        row = rows[0]
        columns = COLLUMS.copy()
        for col in seat[7:]:
            lower, upper = split_middle(columns)
            if col == "L":
                columns = lower
            else:
                columns = upper
        col = columns[0]
        seat = int(row) * 8 + int(col)
        if seat > highest_seat:
            highest_seat = seat
        seats.append(seat)
    return seats, highest_seat


def part_2(data):
    seats = sorted(part_1(data)[0])
    start = seats[0]
    for seat in seats[1:]:
        if seat - start != 1:
            return start + 1
        start = seat
    raise ValueError("Should have found your seat by now")


if __name__ == '__main__':
    source = get_data("day-5.txt")
    print("Part 1:", part_1(source)[1])  # 955
    print("part 2:", part_2(source))  #
