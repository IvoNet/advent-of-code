#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__doc__ = """
# https://raw.githubusercontent.com/mcpower/adventofcode/15ae109bc882ca688665f86e4ca2ba1770495bb4/utils.py
"""

# region Imports
import itertools
import math
import sys
import typing

# endregion

sys.setrecursionlimit(100000)


# Copy a function if you need to modify it.

# region Strings, lists, dicts


def make_grid(*dimensions: list[int], fill=None):
    "Returns a grid such that 'dimensions' is juuust out of bounds."
    if len(dimensions) == 1:
        return [fill for _ in range(dimensions[0])]
    next_down = make_grid(*dimensions[1:], fill=fill)
    return [list(next_down) for _ in range(dimensions[0])]


# endregion

# region Algorithms
class RepeatingSequence:
    def __init__(self, generator, to_hashable=lambda x: x):
        """
        generator should yield the things in the sequence.
        to_hashable should be used if things aren't nicely hashable.
        """
        self.index_to_result = []
        self.hashable_to_index = dict()
        for i, result in enumerate(generator):
            self.index_to_result.append(result)
            hashable = to_hashable(result)
            if hashable in self.hashable_to_index:
                break
            else:
                self.hashable_to_index[hashable] = i
        else:
            raise Exception("generator terminated without repeat")
        self.cycle_begin = self.hashable_to_index[hashable]
        self.cycle_end = i
        self.cycle_length = self.cycle_end - self.cycle_begin

        self.first_repeated_result = self.index_to_result[self.cycle_begin]
        self.second_repeated_result = self.index_to_result[self.cycle_end]

    def cycle_number(self, index):
        """
        Returns which 0-indexed cycle index appears in.
        cycle_number(cycle_begin) is the first index to return 0,
        cycle_number(cycle_end)   is the first index to return 1,
        and so on.
        """
        if index < self.cycle_begin:
            print("WARNING: Index is before cycle!!")
            return 0
        return (index - self.cycle_begin) // self.cycle_length

    def __getitem__(self, index):
        """
        Gets an item in the sequence.
        If index >= cycle_length, returns the items from the first occurrence
        of the cycle.
        Use first_repeated_result and second_repeated_result if needed.
        """
        if index < 0:
            raise Exception("index can't be negative")
        if index < self.cycle_begin:
            return self.index_to_result[index]
        cycle_offset = (index - self.cycle_begin) % self.cycle_length
        return self.index_to_result[self.cycle_begin + cycle_offset]


def bisect(f, lo=0, hi=None, eps=1e-9):
    """
    Returns a value x such that f(x) is true.
    Based on the values of f at lo and hi.
    Assert that f(lo) != f(hi).
    """
    lo_bool = f(lo)
    if hi is None:
        offset = 1
        while f(lo + offset) == lo_bool:
            offset *= 2
        hi = lo + offset
    else:
        assert f(hi) != lo_bool
    while hi - lo > eps:
        mid = (hi + lo) / 2
        if f(mid) == lo_bool:
            lo = mid
        else:
            hi = mid
    if lo_bool:
        return lo
    else:
        return hi


def binary_search(f, lo=0, hi=None):
    """
    Returns a value x such that f(x) is true.
    Based on the values of f at lo and hi.
    Assert that f(lo) != f(hi).
    """
    lo_bool = f(lo)
    if hi is None:
        offset = 1
        while f(lo + offset) == lo_bool:
            offset *= 2
        hi = lo + offset
    else:
        assert f(hi) != lo_bool
    best_so_far = lo if lo_bool else hi
    while lo <= hi:
        mid = (hi + lo) // 2
        result = f(mid)
        if result:
            best_so_far = mid
        if result == lo_bool:
            lo = mid + 1
        else:
            hi = mid - 1
    return best_so_far


# Distances
BLANK = object()


def hamming_distance(a, b) -> int:
    """
    https://www.tutorialspoint.com/what-is-hamming-distance
    """
    return sum(i is BLANK or j is BLANK or i != j for i, j in itertools.zip_longest(a, b, fillvalue=BLANK))


def edit_distance(a, b) -> int:
    n = len(a)
    m = len(b)
    dp = [[None] * (m + 1) for _ in range(n + 1)]
    dp[n][m] = 0

    def aux(i, j):
        assert 0 <= i <= n and 0 <= j <= m
        if dp[i][j] is not None:
            return dp[i][j]
        if i == n:
            dp[i][j] = 1 + aux(i, j + 1)
        elif j == m:
            dp[i][j] = 1 + aux(i + 1, j)
        else:
            dp[i][j] = min((a[i] != b[j]) + aux(i + 1, j + 1), 1 + aux(i + 1, j), 1 + aux(i, j + 1))
        return dp[i][j]

    return aux(0, 0)


# endregion

# region Data Structures
T = typing.TypeVar("T")


class Linked(typing.Generic[T], typing.Iterable[T]):
    """
    Represents a node in a doubly linked lists.

    Can also be interpreted as a list itself.
    Consider this to be first in the list.
    """

    # item: T
    # forward: "Linked[T]"
    # backward: "Linked[T]"
    def __init__(self, item: T) -> None:
        self.item = item
        self.forward = self
        self.backward = self

    @property
    def val(self):
        return self.item

    @property
    def after(self):
        return self.forward

    @property
    def before(self):
        return self.backward

    def _join(self, other: "Linked[T]") -> None:
        self.forward = other
        other.backward = self

    def concat(self, other: "Linked[T]") -> None:
        """
        Concatenates other AFTER THE END OF THE LIST,
        i.e. before this current node.
        """
        first_self = self
        last_self = self.backward

        first_other = other
        last_other = other.backward
        # self ++ other
        # consider last_self and first_other
        last_self._join(first_other)
        last_other._join(first_self)

    def concat_immediate(self, other: "Linked[T]") -> None:
        """
        Concatenates other IN THE "SECOND" INDEX OF THE LIST
        i.e. after this current node.
        """
        self.forward.concat(other)

    def append(self, val: T) -> None:
        """
        Appends an item AFTER THE END OF THE LIST,
        i.e. before this current node.
        """
        self.concat(Linked(val))

    def append_immediate(self, val: T) -> None:
        """
        Appends an item IN THE "SECOND" INDEX OF THE LIST
        i.e. after this current node.
        """
        self.concat_immediate(Linked(val))

    def delete(self) -> None:
        """
        Deletes this node.
        After this is called, you should never use this node.
        """
        forward = self.forward
        backward = self.backward
        forward.backward = backward
        backward.forward = forward

    def delete_other(self, n: int) -> None:
        """
        Deletes a node n nodes forward, or backwards if n is negative.
        """
        to_delete = self.move(n)
        if to_delete is self:
            raise Exception("can't delete self")
        to_delete.delete()
        del to_delete

    def move(self, n: int) -> "Linked[T]":
        """
        Move n nodes forward, or backwards if n is negative.
        """
        out = self
        if n >= 0:
            for _ in range(n):
                out = out.forward
        else:
            for _ in range(-n):
                out = out.backward
        return out

    def iterate_nodes_inf(self) -> typing.Iterator["Linked[T]"]:
        cur = self
        while True:
            yield cur
            cur = cur.forward

    def iterate_nodes(self, count=1) -> typing.Iterator["Linked[T]"]:
        for node in self.iterate_nodes_inf():
            if node is self:
                count -= 1
                if count < 0:
                    break
            yield node

    def iterate_inf(self) -> typing.Iterator[T]:
        return map(lambda node: node.item, self.iterate_nodes_inf())

    def iterate(self, count=1) -> typing.Iterator[T]:
        return map(lambda node: node.item, self.iterate_nodes(count))

    def to_list(self):
        return list(self.iterate())

    def check_correctness(self) -> None:
        assert self.forward.backward is self
        assert self.backward.forward is self

    def check_correctness_deep(self) -> None:
        for node in self.iterate_nodes():
            node.check_correctness()

    def __iter__(self) -> typing.Iterator[T]:
        return self.iterate()

    def __repr__(self) -> str:
        return "Linked({})".format(self.to_list())

    @classmethod
    def from_list(cls, l: typing.Iterable[T]) -> "Linked[T]":
        it = iter(l)
        out = cls(next(it))
        for i in it:
            out.concat(cls(i))
        return out


class UnionFind:
    # n: int
    # parents: List[Optional[int]]
    # ranks: List[int]
    # num_sets: int

    def __init__(self, n: int) -> None:
        self.n = n
        self.parents = [None] * n
        self.ranks = [1] * n
        self.num_sets = n

    def find(self, i: int) -> int:
        p = self.parents[i]
        if p is None:
            return i
        p = self.find(p)
        self.parents[i] = p
        return p

    def in_same_set(self, i: int, j: int) -> bool:
        return self.find(i) == self.find(j)

    def merge(self, i: int, j: int) -> None:
        i = self.find(i)
        j = self.find(j)

        if i == j:
            return

        i_rank = self.ranks[i]
        j_rank = self.ranks[j]

        if i_rank < j_rank:
            self.parents[i] = j
        elif i_rank > j_rank:
            self.parents[j] = i
        else:
            self.parents[j] = i
            self.ranks[i] += 1
        self.num_sets -= 1


# endregion

# region List/Vector operations
GRID_DELTA = [[-1, 0], [1, 0], [0, -1], [0, 1]]
OCT_DELTA = [[1, 1], [-1, -1], [1, -1], [-1, 1]] + GRID_DELTA


def get_neighbours(grid, row, col, deltas, fill=None):
    n, m = len(grid), len(grid[0])
    out = []
    for i, j in deltas:
        p_row, p_col = row + i, col + j
        if 0 <= p_row < n and 0 <= p_col < m:
            out.append(grid[p_row][p_col])
        elif fill is not None:
            out.append(fill)
    return out


def lget(l, i):
    if len(l) == 2:
        return l[i[0]][i[1]]
    for index in i:
        l = l[index]
    return l


def lset(l, i, v):
    if len(l) == 2:
        l[i[0]][i[1]] = v
        return
    for index in i[:-1]:
        l = l[index]
    l[i[-1]] = v


def points_sub_min(points):
    m = [min(p[i] for p in points) for i in range(len(points[0]))]
    return [psub(p, m) for p in points]


def points_to_grid(points, sub_min=True, flip=True):
    if sub_min:
        points = points_sub_min(points)
    if not flip:
        points = [(y, x) for x, y in points]
    grid = make_grid(max(map(snd, points)) + 1, max(map(fst, points)) + 1, '.')
    for x, y in points:
        grid[y][x] = '#'
    return grid


def print_grid(grid, sep=""):
    for line in grid:
        print(*line, sep=sep)


def fst(x):
    return x[0]


def snd(x):
    return x[1]


def padd(x, y):
    if len(x) == 2:
        return [x[0] + y[0], x[1] + y[1]]
    return [a + b for a, b in zip(x, y)]


def pneg(v):
    if len(v) == 2:
        return [-v[0], -v[1]]
    return [-i for i in v]


def psub(x, y):
    if len(x) == 2:
        return [x[0] - y[0], x[1] - y[1]]
    return [a - b for a, b in zip(x, y)]


def pmul(m: int, v):
    if len(v) == 2:
        return [m * v[0], m * v[1]]
    return [m * i for i in v]


def pdot(x, y):
    if len(x) == 2:
        return x[0] * y[0] + x[1] * y[1]
    return sum(a * b for a, b in zip(x, y))


def pdist1(x, y=None):
    if y is not None:
        x = psub(x, y)
    if len(x) == 2:
        return abs(x[0]) + abs(x[1])
    return sum(map(abs, x))


def pdist2sq(x, y=None):
    if y is not None:
        x = psub(x, y)
    if len(x) == 2:
        return (x[0] * x[0]) + (x[1] * x[1])
    return sum(i * i for i in x)


def pdist2(v):
    return math.sqrt(pdist2sq(v))


# endregion

# region Matrices
def matmat(a, b):
    n, k1 = len(a), len(a[0])
    k2, m = len(b), len(b[0])
    assert k1 == k2
    out = [[None] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            out[i][j] = sum(a[i][k] * b[k][j] for k in range(k1))
    return out


def matvec(a, v):
    return [j for i in matmat(a, [[x] for x in v]) for j in i]


def matexp(a, k):
    n = len(a)
    out = [[int(i == j) for j in range(n)] for i in range(n)]
    while k > 0:
        if k % 2 == 1:
            out = matmat(a, out)
        a = matmat(a, a)
        k //= 2
    return out

# endregion
