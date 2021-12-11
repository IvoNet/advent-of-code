#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 07/12/2021 22:38$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

from itertools import product


def neighbors(grid: list[list[int]], coord: tuple, diagonal=True):
    """Retrieve all the neighbors of a coordinate in a fixed 2d grid (boundary).

    :param diagonal: True if you also want the diagonal neighbors, False if not
    :param coord: Tuple with x, y coordinate
    :param grid: the boundary of the grid in layman's terms
    :return: the adjacent coordinates
    """
    height = len(grid) - 1
    width = len(grid[0]) - 1
    down, right = coord
    adjacent = []
    nb = [x for x in product([-1, 0, 1], repeat=2) if x != (0, 0)]
    if not diagonal:
        nb = [x for x in nb if x not in product([-1, 1], repeat=2)]
    for h, w in nb:
        hh = down + h
        ww = right + w
        if hh < 0 or hh > height or ww < 0 or ww > width:
            # not within its boundaries
            continue
        adjacent.append((hh, ww))
    return adjacent


def neighbor_values(grid, coord, diagonal=True):
    """Retrieve the neighbor values of a given 2D grid (list of lists).

    >>> neighbor_values([\
    [2, 1, 9, 9, 9, 4, 3, 2, 1, 0], \
    [3, 9, 8, 7, 8, 9, 4, 9, 2, 1], \
    [9, 8, 5, 6, 7, 8, 9, 8, 9, 2], \
    [8, 7, 6, 7, 8, 9, 6, 7, 8, 9], \
    [9, 8, 9, 9, 9, 6, 5, 6, 7, 8]], (2, 6))
    [9, 4, 9, 8, 8, 9, 6, 7]
    >>> neighbor_values([\
    [2, 1, 9, 9, 9, 4, 3, 2, 1, 0], \
    [3, 9, 8, 7, 8, 9, 4, 9, 2, 1], \
    [9, 8, 5, 6, 7, 8, 9, 8, 9, 2], \
    [8, 7, 6, 7, 8, 9, 6, 7, 8, 9], \
    [9, 8, 9, 9, 9, 6, 5, 6, 7, 8]], (0, 1), diagonal=False)
    [2, 9, 9]
    """
    nb = neighbors(grid, coord, diagonal=diagonal)
    return [grid[h][w] for h, w in nb]


def diagonals(grid, coord):



if __name__ == '__main__':
    import doctest

    doctest.testmod()
