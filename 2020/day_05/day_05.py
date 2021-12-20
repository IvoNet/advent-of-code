#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

from ivonet.files import read_rows

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
    source = read_rows("day_5.input")
    print("Part 1:", part_1(source)[1])  # 955
    print("part 2:", part_2(source))  #
