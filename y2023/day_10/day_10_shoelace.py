import os
import unittest
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints
from ivonet.polygon import shoelace_theorem, picks_theorem

directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def to_direction(c: str) -> tuple[int, int]:
    return {
        '|': (0, 2),
        '-': (1, 3),
        'L': (0, 1),
        'J': (0, 3),
        '7': (2, 3),
        'F': (1, 2)
    }.get(c, (-1, -1))


def other_direction(c: str, d: int) -> int:
    f, s = to_direction(c)
    return s if f == d else f if s == d else -1


def start_pos(grid: list[str]) -> tuple[int, int]:
    for i, row in enumerate(grid):
        if 'S' in row:
            return i, row.index('S')
    raise ValueError("No start position found")


def move_cell(dir: int, pos: tuple[int, int]) -> tuple[int, int]:
    dx, dy = directions[dir]
    x, y = pos
    return x + dx, y + dy


def opposite_direction(dir: int) -> int:
    return dir ^ 2


def get_path_recursive(fi: str,
                       grid: list[str],
                       start: tuple[int, int],
                       target: tuple[int, int], dir: int) -> list[
    tuple[int, int]]:
    """
    Not used anymore but left here for reference
    """
    sx, sy = start
    tx, ty = target
    if not (0 <= sx < len(grid)) or not (0 <= sy < len(grid[0])):
        return []
    if sx == tx and sy == ty and dir != -1:
        return [(sx, sy)]
    ch = grid[sx][sy]
    od = to_direction(fi)[0] if dir == -1 else other_direction(ch, opposite_direction(dir))
    recr = get_path(fi, grid, move_cell(od, start), target, od)
    return [] if od == -1 or not recr else [(sx, sy)] + recr


def get_path(fi: str,
             grid: list[str],
             start: tuple[int, int],
             target: tuple[int, int],
             direction: int) -> list[tuple[int, int]]:
    stack = [(start, direction)]
    path = []
    while stack:
        (sx, sy), direction = stack.pop()
        if not (0 <= sx < len(grid)) or not (0 <= sy < len(grid[0])):
            continue
        if (sx, sy) == target and direction != -1:
            path.append((sx, sy))
            break
        ch = grid[sx][sy]
        od = to_direction(fi)[0] if direction == -1 else other_direction(ch, opposite_direction(direction))
        if od != -1:
            next_pos = move_cell(od, (sx, sy))
            stack.append((next_pos, od))
        path.append((sx, sy))
    return path if path and path[-1] == target else []


def get_loop(grid: list[str]) -> list[tuple[int, int]]:
    sx, sy = start_pos(grid)
    for c in "|-LJ7F":
        path = get_path(c, grid, (sx, sy), (sx, sy), -1)
        if path:
            print(f"len(path) = {len(path)}")
            print(f"Found path: {sorted(path)}")
            return path
    raise ValueError("No loop found")


def shoelace(path: list[tuple[int, int]]) -> int:
    return sum((y1 + y2) * (x2 - x1) for ((x1, y1), (x2, y2)) in zip(path, path[1:])) // 2


def part_1(grid: list[str]) -> int:
    return len(get_loop(grid)) // 2


def part_2(grid: list[str]) -> int:
    path = get_loop(grid)
    area = abs(shoelace_theorem(path))
    print(f"Area: {area}")
    return picks_theorem(area, len(path))


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ""")
        self.test_source2 = read_rows(""".....
.S-7.
.|.|.
.L-J.
.....""")
        self.test_source3 = read_rows("""...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........""")
        self.test_source4 = read_rows("""..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........""")
        self.test_source5 = read_rows(""".F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...""")
        self.test_source6 = read_rows("""FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L""")

    def test_example_data_part_1(self):
        self.assertEqual(8, part_1(self.test_source))

    def test_example_data_part_1_2(self):
        self.assertEqual(4, part_1(self.test_source2))

    def test_part_1(self):
        self.assertEqual(6757, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(4, part_2(self.test_source3))

    def test_example_data_part_2_4(self):
        self.assertEqual(4, part_2(self.test_source4))

    def test_example_data_part_2_5(self):
        self.assertEqual(8, part_2(self.test_source5))

    def test_part_2(self):
        self.assertEqual(523, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
