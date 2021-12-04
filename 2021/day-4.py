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

from ivonet import read_data


def prettyprint(puzzle):
    puzzle = puzzle.split(" ")
    for x in range(0, len(puzzle), 5):
        for y in puzzle[x:x + 5]:
            print(f"{y:>4} ", end="")
        print()
    print()
    for x in range(0, len(puzzle), 5):
        for y in puzzle[x:x + 5]:
            if "*" in y:
                print("X", end="")
            else:
                print("#", end="")
        print()
    print()


def parse_data(data):
    d = data.split("\n\n")
    draws = d[0].split(",")
    puzzles = [x.replace("\n", " ").replace("  ", " ").replace("  ", " ").replace("  ", " ").strip() for x in d[1:]]
    return draws, puzzles


def check_horizontal(puzzle):
    puzzle = puzzle.strip().split(" ")
    win = False
    for x in range(0, len(puzzle) + 1, 5):
        if " ".join(puzzle[x:x + 5]).count("*") == 5:
            win = True
    return win


def check_vertical(puzzle):
    puzzle = puzzle.strip().split(" ")
    for x in range(5):
        count = 0
        for y in range(5):
            if "*" in puzzle[x + (y * 5)]:
                count += 1
        if count == 5:
            return True
    return False


def part_1(data):
    draws, puzzles = parse_data(data)
    for draw in draws:
        new_state = []
        for puzzle in puzzles:
            if f" {draw} " in puzzle:
                print(draw)
                puzzle = puzzle.replace(f" {draw} ", f" {draw}* ")
            new_state.append(puzzle)
            print(draw)
            prettyprint(puzzle)
            win = check_horizontal(puzzle) or check_vertical(puzzle)
            if win:
                unmarked = [int(x) for x in puzzle.split(" ") if "*" not in x]
                unmarked = sum(unmarked)
                print(draw, unmarked, puzzle)
                return unmarked * int(draw)
        puzzles = new_state


def part_2(data):
    pass


if __name__ == '__main__':
    source = read_data("day-4.txt")
    source = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""
    print("Part 1:", part_1(source))  #
    print("part 2:", part_2(source))  #
