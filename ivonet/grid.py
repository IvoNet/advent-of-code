#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 07/12/2021 22:38$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

from itertools import product

from ivonet.iter import flatten


def neighbors(grid: list[list[int]], coord: tuple, diagonal=True):
    """Retrieve all the neighbors of a coordinate in a fixed 2d grid (boundary).

    :param diagonal: True if you also want the direction neighbors, False if not
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


def diagonals(grid, coord, merged=False):
    """Get all the direction 'lines' from a staring point to the boundary of the grid
    normally you would get a list in list with the direction coordinates per
    direction in a list. If flatten = True then it will be merged into a single list.

    >>> diagonals([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], (0,0), merged=True)
    [(1, 1), (2, 2), (3, 3), (4, 4)]
    >>> diagonals([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], (3,3))
    [[(2, 2), (1, 1), (0, 0)], [(2, 4)], [(4, 2)], [(4, 4)]]
    """
    height = len(grid) - 1
    width = len(grid[0]) - 1
    down, right = coord
    diags = []
    for h, w in product([-1, 1], repeat=2):
        hh = down + h
        ww = right + w
        diagonal = []
        if hh < 0 or hh > height or ww < 0 or ww > width:
            # not within its boundaries
            continue
        while 0 <= hh <= height and 0 <= ww <= width:
            diagonal.append((hh, ww))
            hh += h
            ww += w
        diags.append(diagonal)
    if merged:
        return flatten(diags)
    return diags


def direction(grid, coord, to=(-1, 1)):
    """Direction in a grid based on its staring point and direction.
    """
    vertical, horizontal = to
    down, right = coord
    height = len(grid) - 1
    width = len(grid[0]) - 1
    hh = down + vertical
    ww = right + horizontal
    if hh < 0 or hh > height or ww < 0 or ww > width:
        # not within its boundaries
        return
    while 0 <= hh <= height and 0 <= ww <= width:
        yield hh, ww
        hh += vertical
        ww += horizontal


def nw(grid, coord, value=False):
    """North-West direction based on coord in the grid

    >>> list(nw([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], (0,0)))
    []
    >>> list(nw([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], (4,0)))
    [(3, 1), (2, 2), (1, 3), (0, 4)]
    >>> list(nw([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], (4,0), value=True))
    [((3, 1), 1), ((2, 2), 2), ((1, 3), 3), ((0, 4), 4)]
    """
    for x in direction(grid, coord, to=(-1, 1)):
        if value:
            yield x, grid[x[0]][x[1]]
        else:
            yield x


def sw(grid, coord, value=False):
    """South-West direction based on coord in the grid

    >>> list(sw([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], (0,0)))
    [(1, 1), (2, 2), (3, 3), (4, 4)]
    >>> list(sw([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], (4,0)))
    []
    >>> list(sw([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], (3,3), value=True))
    [((4, 4), 4)]
    """
    for x in direction(grid, coord, to=(1, 1)):
        if value:
            yield x, grid[x[0]][x[1]]
        else:
            yield x


def se(grid, coord, value=False):
    """South-East direction based on coord in the grid

    >>> list(se([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], (0,4)))
    [(1, 3), (2, 2), (3, 1), (4, 0)]
    >>> next(se([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], (2,1)))
    (3, 0)
    >>> next(se([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], (2,1), value=True))
    ((3, 0), 0)
    """
    for x in direction(grid, coord, to=(1, -1)):
        if value:
            yield x, grid[x[0]][x[1]]
        else:
            yield x


def ne(grid, coord, value=False):
    """Nort-East direction based on coord in the grid

    >>> list(ne([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], (4,4)))
    [(3, 3), (2, 2), (1, 1), (0, 0)]
    >>> list(ne([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], (1,2)))
    [(0, 1)]
    >>> list(ne([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], (1,2), value=True))
    [((0, 1), 1)]
    """
    for x in direction(grid, coord, to=(-1, -1)):
        if value:
            yield x, grid[x[0]][x[1]]
        else:
            yield x


def north(grid, coord, value=False):
    """Nort direction based on coord in the grid

    >>> list(north([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], (3,3)))
    [(2, 3), (1, 3), (0, 3)]
    >>> list(north([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], (2,4)))
    [(1, 4), (0, 4)]
    >>> list(north([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], (2,4), value=True))
    [((1, 4), 4), ((0, 4), 4)]
    """
    for x in direction(grid, coord, to=(-1, 0)):
        if value:
            yield x, grid[x[0]][x[1]]
        else:
            yield x


def east(grid, coord, value=False):
    """East direction based on coord in the grid

    >>> list(east([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], (3,2)))
    [(3, 3), (3, 4)]
    >>> list(east([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], (2,4)))
    []
    >>> next(east([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], (2,3), value=True))
    ((2, 4), 4)
    """
    for x in direction(grid, coord, to=(0, 1)):
        if value:
            yield x, grid[x[0]][x[1]]
        else:
            yield x


def south(grid, coord, value=False):
    """
    Nort direction based on coord in the grid

    >>> list(south([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], (3,3)))
    [(4, 3)]
    >>> list(south([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], (2,0)))
    [(3, 0), (4, 0)]
    >>> list(south([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], (3,3), value=True))
    [((4, 3), 3)]
    """
    for x in direction(grid, coord, to=(1, 0)):
        if value:
            yield x, grid[x[0]][x[1]]
        else:
            yield x


def west(grid, coord, value=False):
    """West direction based on coord in the grid

    >>> list(west([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], (3,3)))
    [(3, 2), (3, 1), (3, 0)]
    >>> list(west([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], (2,4)))
    [(2, 3), (2, 2), (2, 1), (2, 0)]
    >>> list(west(["abcde", "abcde", "abcde", "abcde",], (2,2), value=True))
    [((2, 1), 'b'), ((2, 0), 'a')]
    """
    for x in direction(grid, coord, to=(0, -1)):
        if value:
            yield x, grid[x[0]][x[1]]
        else:
            yield x


if __name__ == '__main__':
    import doctest

    doctest.testmod()
