#!/usr/bin/env python3
#  -*- coding: utf-8 -*-


UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


def directions(r, c):
    """Generator that yields the coordinates of the four possible neighbors of the provided coordinate"""
    for dr, dc in [UP, DOWN, LEFT, RIGHT]:
        yield r + dr, c + dc


def turn_left(direction):
    if direction == UP:
        return LEFT
    elif direction == LEFT:
        return DOWN
    elif direction == DOWN:
        return RIGHT
    elif direction == RIGHT:
        return UP
    else:
        raise ValueError(f"Invalid direction {direction}")


def turn_right(direction):
    if direction == UP:
        return RIGHT
    elif direction == RIGHT:
        return DOWN
    elif direction == DOWN:
        return LEFT
    elif direction == LEFT:
        return UP
    else:
        raise ValueError(f"Invalid direction {direction}")


def reverse(direction):
    if direction == UP:
        return DOWN
    elif direction == RIGHT:
        return LEFT
    elif direction == DOWN:
        return UP
    elif direction == LEFT:
        return RIGHT
    else:
        raise ValueError(f"Invalid direction {direction}")


def char_to_direction(char):
    if char == "^":
        return UP
    elif char == ">":
        return RIGHT
    elif char == "<":
        return LEFT
    elif char == "v":
        return DOWN
    else:
        raise ValueError(f"Invalid character {char}")
