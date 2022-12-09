#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

from collections import defaultdict
from enum import Enum
from itertools import product
from typing import NamedTuple, Callable

from ivonet.iter import flatten, max_idx


class Location(NamedTuple):
    row: int
    col: int

    def __add__(self, other):
        return Location(self.row + other.row, self.col + other.col)

    def __sub__(self, other):
        return Location(self.row - other.row, self.col - other.col)

    def __mul__(self, other):
        return Location(self.row * other.row, self.col * other.col)


DIRECTIONS = {
    "N": Location(-1, 0),
    "NE": Location(-1, 1),
    "E": Location(0, 1),
    "SE": Location(1, 1),
    "S": Location(1, 0),
    "SW": Location(1, -1),
    "W": Location(0, -1),
    "NW": Location(-1, -1),
}


def manhattan_distance(goal: Location) -> Callable[[Location], float]:
    """https://en.wikipedia.org/wiki/Taxicab_geometry"""

    def distance(ml: Location) -> float:
        xdist: int = abs(ml.col - goal.col)
        ydist: int = abs(ml.row - goal.row)
        return xdist + ydist

    return distance


def neighbors(grid: list[list[any]], coord: Location, diagonal=True) -> list[Location]:
    """Retrieve all the neighbors of a coordinate in a fixed 2d grid (boundary).

    :param diagonal: True if you also want the direction neighbors, False if not
    :param coord: Tuple with (height, width) coordinate (Y, X) or (row, col)!!
    :param grid: the boundary of the grid in layman's terms
    :return: the adjacent coordinates
    """
    height = len(grid) - 1
    width = len(grid[0]) - 1
    current: Location = coord
    adjacent = []
    nb: list[Location] = list(DIRECTIONS.values())
    if not diagonal:
        nb = [v for k, v in DIRECTIONS.items() if k in list("NESW")]
    for loc in nb:
        pos: Location = current + loc
        if pos.row < 0 or pos.row > height or pos.col < 0 or pos.col > width:
            # not within its boundaries
            continue
        adjacent.append(pos)
    return adjacent


def neighbor_values(grid: list[list[any]], coord: Location, diagonal=True) -> list:
    """Retrieve the neighbor values of a given 2D grid (list of lists).

    >>> neighbor_values([\
    [2, 1, 9, 9, 9, 4, 3, 2, 1, 0], \
    [3, 9, 8, 7, 8, 9, 4, 9, 2, 1], \
    [9, 8, 5, 6, 7, 8, 9, 8, 9, 2], \
    [8, 7, 6, 7, 8, 9, 6, 7, 8, 9], \
    [9, 8, 9, 9, 9, 6, 5, 6, 7, 8]], Location(2, 6))
    [4, 9, 8, 7, 6, 9, 8, 9]
    >>> neighbor_values([\
    [2, 1, 9, 9, 9, 4, 3, 2, 1, 0], \
    [3, 9, 8, 7, 8, 9, 4, 9, 2, 1], \
    [9, 8, 5, 6, 7, 8, 9, 8, 9, 2], \
    [8, 7, 6, 7, 8, 9, 6, 7, 8, 9], \
    [9, 8, 9, 9, 9, 6, 5, 6, 7, 8]], Location(0, 1), diagonal=False)
    [9, 9, 2]
    """
    nb = neighbors(grid, coord, diagonal=diagonal)
    return [grid[h][w] for h, w in nb]


def neighbors_defined_grid(coord: Location, grid=(100, 100), diagonal=True) -> list[Location]:
    """Same as neighbors (above) but now with a fictional grid"""
    height = grid[0] - 1
    width = grid[1] - 1
    current = coord
    adjacent = []
    nb: list[Location] = list(DIRECTIONS.values())
    if not diagonal:
        nb = [v for k, v in DIRECTIONS.items() if k in list("NESW")]
    for loc in nb:
        pos = current + loc
        if pos.col < 0 or pos.col > width or pos.row < 0 or pos.row > height:
            continue
        adjacent.append(pos)
    return adjacent


def diagonals(grid: list[list[any]], coord: Location, merged: bool = False) -> list:
    """Get all the direction 'lines' from a staring point to the boundary of the grid
    normally you would get a list in list with the direction coordinates per
    direction in a list. If flatten = True then it will be merged into a single list.

    >>> diagonals([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], Location(0,0), merged=True)
    [(1, 1), (2, 2), (3, 3), (4, 4)]
    >>> diagonals([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], Location(3,3))
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


def direction(grid: list[list[any]], coord: Location, to: tuple[int, int] = (-1, 1)):
    """Direction in a grid based on its starting point and direction.
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


def nw(grid: list[list[any]], coord: Location, value: bool = False):
    """North-West direction based on coord in the grid

    >>> list(nw([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], Location(4,4)))
    [(3, 3), (2, 2), (1, 1), (0, 0)]
    >>> list(nw([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], Location(3,2)))
    [(2, 1), (1, 0)]
    >>> list(nw([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], Location(3,2), value=True))
    [((2, 1), 1), ((1, 0), 0)]
    """
    for x in direction(grid, coord, to=(-1, -1)):
        if value:
            yield x, grid[x[0]][x[1]]
        else:
            yield x


def sw(grid: list[list[any]], coord: Location, value: bool = False):
    """South-West direction based on coord in the grid

    >>> list(sw([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], Location(0,4)))
    [(1, 3), (2, 2), (3, 1), (4, 0)]
    >>> list(sw([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], Location(4,0)))
    []
    >>> list(sw([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], Location(3,3), value=True))
    [((4, 2), 2)]
    """
    for x in direction(grid, coord, to=(1, -1)):
        if value:
            yield x, grid[x[0]][x[1]]
        else:
            yield x


def se(grid: list[list[any]], coord: Location, value: bool = False):
    """South-East direction based on coord in the grid

    >>> list(se([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], Location(0,0)))
    [(1, 1), (2, 2), (3, 3), (4, 4)]
    >>> next(se([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], Location(2,1)))
    (3, 2)
    >>> next(se([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], Location(2,1), value=True))
    ((3, 2), 2)
    """
    for x in direction(grid, coord, to=(1, 1)):
        if value:
            yield x, grid[x[0]][x[1]]
        else:
            yield x


def ne(grid: list[list[any]], coord: Location, value: bool = False):
    """Nort-East direction based on coord in the grid

    >>> list(ne([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], Location(4,0)))
    [(3, 1), (2, 2), (1, 3), (0, 4)]
    >>> list(ne([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], Location(1,2)))
    [(0, 3)]
    >>> list(ne([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], Location(1,2), value=True))
    [((0, 3), 3)]
    """
    for x in direction(grid, coord, to=(-1, 1)):
        if value:
            yield x, grid[x[0]][x[1]]
        else:
            yield x


def north(grid: list[list[any]], coord: Location, value: bool = False):
    """Nort direction based on coord in the grid

    >>> list(north([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], Location(3,3)))
    [(2, 3), (1, 3), (0, 3)]
    >>> list(north([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], Location(2,4)))
    [(1, 4), (0, 4)]
    >>> list(north([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], Location(2,4), value=True))
    [((1, 4), 4), ((0, 4), 4)]
    """
    for x in direction(grid, coord, to=(-1, 0)):
        if value:
            yield x, grid[x[0]][x[1]]
        else:
            yield x


def east(grid: list[list[any]], coord: Location, value: bool = False):
    """East direction based on coord in the grid

    >>> list(east([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], Location(3,2)))
    [(3, 3), (3, 4)]
    >>> list(east([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], Location(2,4)))
    []
    >>> next(east([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], Location(2,3), value=True))
    ((2, 4), 4)
    """
    for x in direction(grid, coord, to=(0, 1)):
        if value:
            yield x, grid[x[0]][x[1]]
        else:
            yield x


def south(grid: list[list[any]], coord: Location, value: bool = False):
    """
    Nort direction based on coord in the grid

    >>> list(south([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], Location(3,3)))
    [(4, 3)]
    >>> list(south([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], Location(2,0)))
    [(3, 0), (4, 0)]
    >>> list(south([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], Location(3,3), value=True))
    [((4, 3), 3)]
    """
    for x in direction(grid, coord, to=(1, 0)):
        if value:
            yield x, grid[x[0]][x[1]]
        else:
            yield x


def west(grid: list[list[any]], coord: Location, value: bool = False):
    """West direction based on coord in the grid

    >>> list(west([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], Location(3,3)))
    [(3, 2), (3, 1), (3, 0)]
    >>> list(west([[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4],], Location(2,4)))
    [(2, 3), (2, 2), (2, 1), (2, 0)]
    >>> list(west([list("abcde"), list("abcde"), list("abcde"), list("abcde"),], Location(2,2), value=True))
    [((2, 1), 'b'), ((2, 0), 'a')]
    """
    for x in direction(grid, coord, to=(0, -1)):
        if value:
            yield x, grid[x[0]][x[1]]
        else:
            yield x


def directions(grid: list[list[any]], coord: Location, value: bool = False) -> dict:
    """Create a coordinate generator for all the wind directions.
    The grid should be a 2d matrix (list of lists)
    """
    return {
        'n': north(grid, coord, value),
        'ne': ne(grid, coord, value),
        'e': east(grid, coord, value),
        'se': se(grid, coord, value),
        's': south(grid, coord, value),
        'sw': sw(grid, coord, value),
        'w': west(grid, coord, value),
        'nw': nw(grid, coord, value)
    }


class Matrix(defaultdict):

    def __init__(self) -> None:
        super().__init__(int)
        self.max_w = 0
        self.max_h = 0

    def __setitem__(self, k: tuple[int, int], v: int) -> None:
        w, h = k
        self.max_w = w if w > self.max_w else self.max_w
        self.max_h = h if h > self.max_h else self.max_h
        super().__setitem__(k, v)

    def width(self) -> int:
        """Find the max width of the given matrix
        The matrix is represented as a dict looking like this:
           dict[(x,y)] = value
        """
        return self.max_w + 1

    def height(self) -> int:
        """Find the max height of the given matrix
        The matrix is represented as a dict looking like this:
           dict[(x,y)] = value
        """
        return self.max_h + 1

    def fold_vertical(self, fold_index):
        return fold_vertical(self, fold_index)

    def fold_horizontal(self, fold_index):
        return fold_horizontal(self, fold_index)

    def total(self):
        total = 0
        for x in range(self.width()):
            for y in range(self.height()):
                total += self[(x, y)]
        return total

    def print(self, end="", sign_on="#", sign_off=" "):
        print("-" * 50)
        for y in range(self.height()):
            for x in range(self.width()):
                try:
                    print(sign_on if self[(x, y)] == 1 else sign_off, end=end)
                except KeyError:
                    print(f"key error x={x}, y={y}")
            print()
        print("-" * 50)


def create_grid(width, height, initial="0"):
    """Initializes a list in list of the given width (cols) and height (rows)
    initialized with the `initial` value
    """
    return [[initial] * width] * height


def fold_horizontal(matrix: defaultdict, fold_index):
    """Fold a 2d matrix represented as a dictionary with coordinats as key
    and int as value
    1 = on
    0 = off

    01001
    10000                         11111
    10001                         10001
    00000 <- fold line results in 11111
    11110
    10001
    10111

    You loose the folding line in this setup

    Note that the under side of the fold should never exceed more
    than half the height of the matrix. No checks on this at this time

    :param matrix: list of lists
    :param fold_index: the height on which to fold and the new max height
    :return: new matrix
    """
    m = Matrix()
    for x, y in matrix:
        if matrix[(x, y)] == 1:
            if y < fold_index:
                m[(x, y)] = 1
            elif y > fold_index:
                yy = fold_index - (y - fold_index)
                m[(x, yy)] = 1
    return m


def fold_vertical(matrix: defaultdict, fold_index):
    """Fold a 2d matrix represented as a dictionary with coordinats as key
    and int as value
    1 = on
    0 = off

    01001           results in 011
    10000                      100
    10001                      101
       ^
       fold index
    You loose the folding line in this setup.

    Note that the right side of the fold should never exceed more
    than half the width of the matrix. No checks on this at this time

    :param matrix: dict of tuple, int as key, value
    :param fold_index: the width on which to fold and the new max width
    :return: new matrix
    """
    m = Matrix()
    for x, y in matrix:
        if matrix[(x, y)] == 1:
            if x < fold_index:
                m[(x, y)] = 1
            elif x > fold_index:
                xx = fold_index - (x - fold_index)
                m[(xx, y)] = 1
    return m


def max_width(matrix: defaultdict) -> int:
    """Find the max width of the given matrix
    The matrix is represented as a dict looking like this:
       dict[(x,y)] = value
    """
    return max_idx(list(matrix.keys()), 0) + 1


def max_height(matrix: defaultdict) -> int:
    """Find the max height of the given matrix
    The matrix is represented as a dict looking like this:
       dict[(x,y)] = value
    """
    return max_idx(list(matrix.keys()), 1) + 1


def walk_direction(grid, loc: Location, direction_: str, value=False):  # Note untested yet!
    """
    Walks in a the_way_to_go until it hits a wall or the edge of the grid.
    :param grid: the grid to walk on
    :param loc: the location to start walking from
    :param direction_: the direction to walk in
    :param value: if True return the value at the location too
    :return: an Iterator of locations
    """
    r, c = loc
    if direction_ == "N":
        for i in range(r - 1, -1, -1):
            if value:
                yield i, c, grid[i][c]
            else:
                yield i, c
    elif direction_ == "S":
        for i in range(r + 1, len(grid)):
            if value:
                yield i, c, grid[i][c]
            else:
                yield i, c
    elif direction_ == "E":
        for i in range(c + 1, len(grid[r])):
            if value:
                yield r, i, grid[r][i]
            else:
                yield r, i
    elif direction_ == "W":
        for i in range(c - 1, -1, -1):
            if value:
                yield r, i, grid[r][i]
            else:
                yield r, i
    elif direction_ == "NE":
        for i in range(1, len(grid[r])):
            if r - i < 0 or c + i >= len(grid[r]):
                break
            if value:
                yield r - i, c + i, grid[r - i][c + i]
            else:
                yield r - i, c + i
    elif direction_ == "NW":
        for i in range(1, len(grid[r])):
            if r - i < 0 or c - i < 0:
                break
            if value:
                yield r - i, c - i, grid[r - i][c - i]
            else:
                yield r - i, c - i
    elif direction_ == "SE":
        for i in range(1, len(grid[r])):
            if r + i >= len(grid) or c + i >= len(grid[r]):
                break
            if value:
                yield r + i, c + i, grid[r + i][c + i]
            else:
                yield r + i, c
    elif direction_ == "SW":
        for i in range(1, len(grid[r])):
            if r + i >= len(grid) or c - i < 0:
                break
            if value:
                yield r + i, c - i, grid[r + i][c - i]
            else:
                yield r + i, c - i


class Cell(str, Enum):
    EMPTY = "."
    BLOCKED = "#"
    PATH = "*"
    START = "S"
    GOAL = "G"

    def __repr__(self) -> str:
        return self.value

    def __str__(self) -> str:
        return repr(self)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
