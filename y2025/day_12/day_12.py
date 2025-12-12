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

DEBUG = False


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
        # grid represented as list of integers (bitmask per row)
        self.grid: list[int] = [0 for _ in range(self.height)]

    def _shape_transformations(self, shape: Shape):
        """Return unique transformations of a shape as dicts with:
        - cells: list of (x,y)
        - width, height
        - row_masks: list[int] (mask per row with bit 0 as leftmost)
        """
        seen = set()
        transformations = []
        # generate rotations and flips
        s = shape
        for _ in range(4):
            for variant in (s, s.flip_horizontally(), s.flip_vertically()):
                # build canonical string representation
                rows = [''.join('#' if c else '.' for c in row) for row in variant.grid]
                key = '\n'.join(rows)
                if key in seen:
                    continue
                seen.add(key)
                cells = []
                for y, row in enumerate(variant.grid):
                    for x, v in enumerate(row):
                        if v:
                            cells.append((x, y))
                width = max(x for x, _ in cells) + 1
                height = max(y for _, y in cells) + 1
                # build row masks
                row_masks = [0 for _ in range(height)]
                for x, y in cells:
                    row_masks[y] |= 1 << x
                transformations.append({
                    'cells': cells,
                    'width': width,
                    'height': height,
                    'row_masks': row_masks,
                    'area': len(cells),
                    'repr': key,
                })
            s = s.rotate()
        return transformations

    def fits_shapes(self, shapes: list[Shape]) -> bool:
        """Try to fit the required shapes into this region.

        Uses a backtracking solver with precomputed placements and MRV heuristic.
        """
        counts = list(self.indexes)
        total_pieces = sum(counts)
        verbose = total_pieces <= 10 and DEBUG
        # Compute transformations and placements
        shape_transforms = {}
        for shape in shapes:
            shape_transforms[int(shape.name)] = self._shape_transformations(shape)
        # Quick area check
        total_area = sum((shape_transforms[i][0]['area'] if shape_transforms.get(i) else 0) * counts[i] for i in range(len(counts)))
        if verbose:
            print(f"Region {self.name} {self.width}x{self.height} counts={counts} total_area={total_area}")
        if total_area > self.width * self.height:
            if verbose:
                print(' quick area reject')
            return False

        # Precompute all possible placements for each shape index
        placements = {i: [] for i in range(len(counts))}
        full_mask = (1 << self.width) - 1
        for i in range(len(counts)):
            transforms = shape_transforms.get(i, [])
            for t in transforms:
                for oy in range(0, self.height - t['height'] + 1):
                    for ox in range(0, self.width - t['width'] + 1):
                        # build placement row masks
                        row_masks = [0] * self.height
                        for row_idx in range(t['height']):
                            row_masks[oy + row_idx] = t['row_masks'][row_idx] << ox
                        placements[i].append(tuple(row_masks))
            if verbose:
                print(f' shape {i} placements={len(placements[i])}')
            if not placements[i] and counts[i] > 0:
                # shape cannot be placed at all but required
                if verbose:
                    print(f' shape {i} cannot be placed but required')
                return False

        remaining = {i: counts[i] for i in range(len(counts))}

        # MRV: choose shape index with remaining>0 and fewest placements
        def choose_shape():
            best = None
            best_count = None
            for i in range(len(counts)):
                r = remaining[i]
                if r <= 0:
                    continue
                pcount = len(placements[i])
                if best is None or pcount < best_count:
                    best = i
                    best_count = pcount
            return best

        sys.setrecursionlimit(10000)

        def backtrack(grid_rows: list[int]) -> bool:
            if all(v == 0 for v in remaining.values()):
                if verbose:
                    print(' success: all placed')
                return True
            # simple pruning
            free = 0
            for r in grid_rows:
                free += bin(full_mask ^ r).count('1')
            rem_area = sum(remaining[i] * (shape_transforms[i][0]['area'] if shape_transforms.get(i) else 0) for i in range(len(counts)))
            if rem_area > free:
                if verbose:
                    print(' prune by area', rem_area, free)
                return False
            i = choose_shape()
            if i is None:
                return False
            if verbose:
                print(f'trying shape {i} remaining {remaining[i]} placements {len(placements[i])}')
            # Try placements
            for p in placements[i]:
                collision = False
                for row_idx in range(self.height):
                    if grid_rows[row_idx] & p[row_idx]:
                        collision = True
                        break
                if collision:
                    continue
                # place
                for row_idx in range(self.height):
                    grid_rows[row_idx] |= p[row_idx]
                remaining[i] -= 1
                if backtrack(grid_rows):
                    return True
                remaining[i] += 1
                for row_idx in range(self.height):
                    grid_rows[row_idx] ^= p[row_idx]
            if verbose:
                print(f' backtrack fail for shape {i} at this branch')
            return False

        grid_rows = [0] * self.height
        res = backtrack(grid_rows)
        if verbose:
            print('final result', res)
        # if this solver found a solution, return True, otherwise continue to other strategies
        if res:
            return True

        # For small number of pieces use expanded-piece MRV backtracking (more reliable)
        if total_pieces <= 10:
            # build placements per shape as before
            piece_list = []
            for i in range(len(counts)):
                for _ in range(counts[i]):
                    piece_list.append(i)
            # precompute placements per shape
            placements_per_shape = placements

            # backtrack choosing the piece (index in piece_list) with fewest valid placements
            def backtrack_pieces(grid_rows: list[int], remaining_counts: dict[int,int]) -> bool:
                if all(v == 0 for v in remaining_counts.values()):
                    if verbose:
                        print(' success: all placed (pieces)')
                    return True
                # compute valid placements count per shape
                best_shape = None
                best_options = None
                valid_options_cache = {}
                for shape_idx, cnt in remaining_counts.items():
                    if cnt <= 0:
                        continue
                    valid = []
                    for p in placements_per_shape[shape_idx]:
                        ok = True
                        for r in range(self.height):
                            if grid_rows[r] & p[r]:
                                ok = False
                                break
                        if ok:
                            valid.append(p)
                    valid_options_cache[shape_idx] = valid
                    if best_options is None or len(valid) < len(best_options):
                        best_options = valid
                        best_shape = shape_idx
                if best_shape is None or not best_options:
                    return False
                if verbose:
                    print(f' choose shape {best_shape} with {len(best_options)} options remaining_counts={remaining_counts}')
                for p in best_options:
                    # place
                    for r in range(self.height):
                        grid_rows[r] |= p[r]
                    remaining_counts[best_shape] -= 1
                    if backtrack_pieces(grid_rows, remaining_counts):
                        return True
                    remaining_counts[best_shape] += 1
                    for r in range(self.height):
                        grid_rows[r] ^= p[r]
                return False

            grid_rows = [0] * self.height
            if backtrack_pieces(grid_rows, dict(remaining)):
                return True
            # fallthrough to general solver if small-case backtrack fails
            if verbose:
                print(' small-piece solver failed, falling back to general')

        # If small instance, build exact cover matrix and solve with Algorithm X
        total_placements = sum(len(placements[i]) * (counts[i] if counts[i] > 0 else 0) for i in range(len(counts)))
        if total_pieces <= 12 and total_placements < 10000:
            # Columns: grid cells indexed 0..(w*h-1), and piece instance columns ('p',i,j)
            cols = []
            cell_cols = list(range(self.width * self.height))
            cols.extend(cell_cols)
            piece_cols = []
            for i in range(len(counts)):
                for j in range(counts[i]):
                    piece_cols.append(('p', i, j))
            cols.extend(piece_cols)
            # Map column to set of rows that cover it
            col_rows = {c: set() for c in cols}
            # Rows: id -> set(columns)
            rows = {}
            row_id = 0
            for i in range(len(counts)):
                for inst in range(counts[i]):
                    for p in placements[i]:
                        covered = set()
                        # cells
                        ok = True
                        for y in range(self.height):
                            mask = p[y]
                            if mask:
                                # for each bit in mask add corresponding cell col
                                for x in range(self.width):
                                    if (mask >> x) & 1:
                                        covered.add(y * self.width + x)
                        if not covered:
                            continue
                        # add piece instance column
                        covered.add(('p', i, inst))
                        rows[row_id] = covered
                        for c in covered:
                            col_rows[c].add(row_id)
                        row_id += 1
            if verbose:
                print('Exact cover columns', len(cols), 'rows', len(rows))
            # Algorithm X
            def solve(selected_rows: list[int], col_rows_map: dict, rows_map: dict) -> bool:
                if not col_rows_map:
                    return True
                # choose column with fewest options
                c = min(col_rows_map.keys(), key=lambda c: len(col_rows_map[c]))
                options = list(col_rows_map[c])
                if not options:
                    return False
                for r in options:
                    selected_rows.append(r)
                    removed = {}
                    # cover columns in this row
                    for col in rows_map[r]:
                        # for each row that has this col, remove that row from other cols
                        for rr in list(col_rows_map.get(col, [])):
                            for col2 in rows_map[rr]:
                                if col2 == col:
                                    continue
                                if col2 in col_rows_map and rr in col_rows_map[col2]:
                                    col_rows_map[col2].remove(rr)
                                    removed.setdefault(col2, []).append(rr)
                        # remove the column entirely
                        if col in col_rows_map:
                            removed.setdefault(col, []).append(col_rows_map[col])
                            del col_rows_map[col]
                    if solve(selected_rows, col_rows_map, rows_map):
                        return True
                    # undo
                    selected_rows.pop()
                    # restore
                    for col2, rows_removed in removed.items():
                        if col2 in cols:
                            # col was removed entirely
                            if isinstance(rows_removed, set):
                                col_rows_map[col2] = set(rows_removed)
                        else:
                            col_rows_map[col2].update(rows_removed)
                return False
            # Copy maps
            col_rows_copy = {k: set(v) for k, v in col_rows.items()}
            rows_copy = {k: set(v) for k, v in rows.items()}
            try:
                ok = solve([], col_rows_copy, rows_copy)
                if verbose:
                    print('exact cover result', ok)
                if ok:
                    return True
            except RecursionError:
                if verbose:
                    print('exact cover recursion error')
            # fall through to general solver
            if verbose:
                print(' exact cover failed, continue to general backtracker')

        # As final attempt for small instances, use explicit boolean grid DFS
        if total_pieces <= 14:
            # build list of transformations with cells list in (x,y)
            trans_per_shape = {i: shape_transforms.get(i, []) for i in range(len(counts))}
            # expand pieces as list of shape indices
            pieces = []
            for i in range(len(counts)):
                pieces.extend([i] * counts[i])
            # order pieces by area descending to help pruning
            piece_order = sorted(range(len(pieces)), key=lambda idx: - (trans_per_shape[pieces[idx]][0]['area'] if trans_per_shape[pieces[idx]] else 0))
            # start grid
            grid = [[False] * self.width for _ in range(self.height)]

            def find_first_empty():
                for y in range(self.height):
                    for x in range(self.width):
                        if not grid[y][x]:
                            return x, y
                return None

            def can_place(t, ox, oy):
                for (tx, ty) in t['cells']:
                    x = ox + tx
                    y = oy + ty
                    if x < 0 or y < 0 or x >= self.width or y >= self.height:
                        return False
                    if grid[y][x]:
                        return False
                return True

            def place(t, ox, oy, val: bool):
                for (tx, ty) in t['cells']:
                    grid[oy + ty][ox + tx] = val

            # recursive by remaining counts
            def dfs(remaining_counts):
                # find first empty cell
                fe = find_first_empty()
                if fe is None:
                    return all(v == 0 for v in remaining_counts.values())
                x_empty, y_empty = fe
                # try each shape type that has remaining
                for i in sorted([k for k, v in remaining_counts.items() if v > 0], key=lambda k: - (trans_per_shape[k][0]['area'] if trans_per_shape.get(k) else 0)):
                    for t in trans_per_shape.get(i, []):
                        # try all placements that could cover x_empty,y_empty by aligning each cell of t
                        for tx, ty in t['cells']:
                            ox = x_empty - tx
                            oy = y_empty - ty
                            if can_place(t, ox, oy):
                                place(t, ox, oy, True)
                                remaining_counts[i] -= 1
                                if dfs(remaining_counts):
                                    return True
                                remaining_counts[i] += 1
                                place(t, ox, oy, False)
                return False

            if dfs(dict(remaining)):
                return True
            # else continue to other solvers

        return False


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
    # Nothing to do for part 2
    return None


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(2, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(448, part_1(self.source))

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
