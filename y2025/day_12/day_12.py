#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2023 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
If a part of the code is not part of the post it is probably 
code I found reusable and I may have moved it to my 'ivonet' library.
you can find that here: https://github.com/IvoNet/advent-of-code/tree/master/ivonet
"""

import collections
import sys
import unittest
from pathlib import Path

import pyperclip
from ivonet.decorators import debug
from ivonet.decorators import timer
from ivonet.files import read_rows
from ivonet.iter import ints

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


class Shape:
    def __init__(self, name: int) -> None:
        self.name = name
        self.grid = []

    def add_row(self, row: str) -> None:
        self.grid.append([True if c == '#' else False for c in row])

    def rotate(self) -> Shape:
        """ Rotate 90 degrees clockwise """
        new_shape = Shape(self.name)
        new_shape.grid = [list(reversed(col)) for col in zip(*self.grid)]
        return new_shape

    def flip_horizontally(self) -> Shape:
        """ Flip horizontally """
        new_shape = Shape(self.name)
        new_shape.grid = [list(reversed(row)) for row in self.grid]
        return new_shape

    def flip_vertically(self) -> Shape:
        """ Flip vertically """
        new_shape = Shape(self.name)
        new_shape.grid = list(reversed(self.grid))
        return new_shape

    def all_transformations(self) -> list[Shape]:
        """ Generate all unique transformations of the shape """
        transformations = set()
        current_shape = self
        for _ in range(4):
            transformations.add(current_shape)
            transformations.add(current_shape.flip_horizontally())
            transformations.add(current_shape.flip_vertically())
            current_shape = current_shape.rotate()
        return list(transformations)

    def __repr__(self):
        return "Shape({})".format(self.name)

    def __str__(self):
        rows = []
        for row in self.grid:
            rows.append(''.join('#' if cell else '.' for cell in row))
        return '\n'.join(rows)


class Region:
    def __init__(self, name: str, indexes: list[int]) -> None:
        self.name = name
        self.indexes = indexes
        size = ints(name)
        self.width = size[0]
        self.height = size[1]
        self.grid: list[list[str]] = []
        self.reset()

    def reset(self) -> None:
        self.grid = [["." for _ in range(self.width)] for _ in range(self.height)]

    def fits_shapes(self, shapes: list[Shape]) -> bool:
        """
        Try to fit all shapes in the region.
        Shapes can be rotated and flipped before placing.
        Start with a reset region and try all the combinations of all shapes to see if they fit.
        We need to find all positions where we can place a shape, then try to place the next shape in the remaining space.
        This is a backtracking problem.
        :param shapes:
        :return: True if all shapes fit in the region, False otherwise.
        """
        self.reset()
        for shape in shapes:
            if not self.add_shape(shape):
                return False
        return True

    def add_shape(self, shape: Shape) -> bool:
        """
        Try to add the shape to the region.
        note that a shape can be rotated and flipped before placing. All the states can be generated using shape.all_transformations()
        try to fit the shape in all possible positions.
        """
        for transformed_shape in shape.all_transformations():
            for row in range(self.height - len(transformed_shape.grid) + 1):
                for col in range(self.width - len(transformed_shape.grid[0]) + 1):
                    if self.can_place_shape(transformed_shape, row, col):
                        self.place_shape(transformed_shape, row, col)
                        return True
        return False


    def can_place_shape(self, shape: Shape, row: int, col: int) -> bool:
        for i in range(len(shape.grid)):
            for j in range(len(shape.grid[0])):
                if shape.grid[i][j] != "." and self.grid[row + i][col + j] != ".":
                    return False
        return True

    def place_shape(self, shape: Shape, row: int, col: int) -> None:
        for i in range(len(shape.grid)):
            for j in range(len(shape.grid[0])):
                if shape.grid[i][j]:
                    self.grid[row + i][col + j] = shape.name
        p(f"Placed shape {shape.name} at ({row}, {col}) in region {self.name}")
        p(self)


    def __repr__(self):
        return f"Region({self.name}, indexes={self.indexes})"

    def __str__(self):
        rows = []
        for row in self.grid:
            rows.append(''.join(str(x) for x in row))
        return '\n'.join(rows)


def parse(source: list[str]):
    in_shapes = True
    shapes: dict[str, Shape] = {}
    regions: list[Region] = []
    name = ""
    for line in source:
        if line.strip() == "":
            in_shapes = False
            continue
        if line.find(":") > 0:
            if len(ints(line)) == 1:
                in_shapes = True
                name = ints(line.strip())[0]
                shapes[name] = Shape(name)
            else:
                in_shapes = False
                values = line.split(":")
                name = values[0].strip()
                indexes = ints(values[1])
                regions.append(Region(name, indexes))
            continue
        if in_shapes:
            shapes[name].add_row(line.strip())
            continue
    return shapes, regions


@debug
@timer
def part_1(source) -> int | None:
    answer = 0
    shapes, regions = parse(source)
    for region in regions:
        if region.fits_shapes(list(shapes.values())):
            answer += 1
    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:
    answer = 0
    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(2, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(None, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(None, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = Path(__file__).resolve().parent
        day = f"{ints(Path(__file__).stem)[0]:02}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
