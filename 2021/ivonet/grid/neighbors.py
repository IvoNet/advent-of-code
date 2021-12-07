#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 07/12/2021 22:38$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

from itertools import product


def neighbors(coord: tuple, grid=(10, 10)):
    """Retrieve all the neighbors of a coordinate in a fixed 2d grid (boundary).

    :param coord: Tuple with x, y coordinate
    :param grid: the boundary of the grid in layman's terms
    :return: the adjacent coordinates
    """
    width = grid[0] - 1
    height = grid[1] - 1
    retx, rety = coord
    adjacent = []
    for x, y in [x for x in product([-1, 0, 1], repeat=2) if x != (0, 0)]:
        xx = retx + x
        yy = rety + y
        if xx < 0 or xx > width or yy < 0 or yy > height:
            # not in boundaries
            continue
        adjacent.append((xx, yy))
    return adjacent
