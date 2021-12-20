#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
--- Day 15: Chiton ---
You've almost reached the exit of the cave, but the walls are getting 
closer together. Your submarine can barely still fit, though; the
 main problem is that the walls of the cave are covered in chitons, 
 and it would be best not to bump any of them.

The cavern is large, but has a very low ceiling, restricting your 
motion to two dimensions. The shape of the cavern resembles a square; 
a quick scan of chiton density produces a map of risk level throughout 
the cave (your puzzle input). For example:

1 1 6 3 7 5 1 7 4 2
1 3 8 1 3 7 3 6 7 2
2 1 3 6 5 1 1 3 2 8
3 6 9 4 9 3 1 5 6 9
7 4 6 3 4 1 7 1 1 1
1 3 1 9 1 2 8 1 3 7
1 3 5 9 9 1 2 4 2 1
3 1 2 5 4 2 1 6 3 9
1 2 9 3 1 3 8 5 2 1
2 3 1 1 9 4 4 5 8 1


You start in the top left position, your destination is the bottom 
right position, and you cannot move diagonally. The number at each 
position is its risk level; to determine the total risk of an entire 
path, add up the risk levels of each position you enter (that is, don't 
count the risk level of your starting position unless you enter it; 
leaving it adds no risk to your total).

Your goal is to find a path with the lowest total risk. 
In this example, a path with the lowest total risk is highlighted here:

1x1 6 3 7 5 1 7 4 2
1x3 8 1 3 7 3 6 7 2
2x1x3x6x5x1x1x3 2 8
3 6 9 4 9 3 1x5x6 9
7 4 6 3 4 1 7 1x1 1
1 3 1 9 1 2 8 1x3x7
1 3 5 9 9 1 2 4 2x1
3 1 2 5 4 2 1 6 3x9
1 2 9 3 1 3 8 5 2x1x
2 3 1 1 9 4 4 5 8 1x

The total risk of this path is 40 (the starting position is 
never entered, so its risk is not counted).

What is the lowest total risk of any path from the top left to 
the bottom right?


--- Part Two ---

Now that you know how to find low-risk paths in the cave, you can try 
to find your way out.

The entire cave is actually five times larger in both dimensions than you 
thought; the area you originally scanned is just one tile in a 5x5 tile area 
that forms the full map. Your original map tile repeats to the right and 
downward; each time the tile repeats to the right or downward, all of its 
risk levels are 1 higher than the tile immediately up or left of it. However, 
risk levels above 9 wrap back around to 1. So, if your original map had some 
position with a risk level of 8, then that same position on each of the 25 
total tiles would be as follows:

8 9 1 2 3
9 1 2 3 4
1 2 3 4 5
2 3 4 5 6
3 4 5 6 7

Each single digit above corresponds to the example position with a value 
of 8 on the top-left tile. Because the full map is actually five times 
larger in both dimensions, that position appears a total of 25 times, 
once in each duplicated tile, with the values shown above.

Here is the full five-times-as-large version of the first example above, 
with the original map in the top left corner highlighted:

1163751742 2274862853338597396444961841755517295286
1381373672 2492484783351359589446246169155735727126
2136511328 3247622439435873354154698446526571955763
3694931569 4715142671582625378269373648937148475914
7463417111 8574528222968563933317967414442817852555
1319128137 2421239248353234135946434524615754563572
1359912421 2461123532357223464346833457545794456865
3125421639 4236532741534764385264587549637569865174
1293138521 2314249632342535174345364628545647573965
2311944581 3422155692453326671356443778246755488935

2274862853 3385973964449618417555172952866628316397
2492484783 3513595894462461691557357271266846838237
3247622439 4358733541546984465265719557637682166874
4715142671 5826253782693736489371484759148259586125
8574528222 9685639333179674144428178525553928963666
2421239248 3532341359464345246157545635726865674683
2461123532 3572234643468334575457944568656815567976
4236532741 5347643852645875496375698651748671976285
2314249632 3425351743453646285456475739656758684176
3422155692 4533266713564437782467554889357866599146
3385973964 4496184175551729528666283163977739427418
3513595894 4624616915573572712668468382377957949348
4358733541 5469844652657195576376821668748793277985
5826253782 6937364893714847591482595861259361697236
9685639333 1796741444281785255539289636664139174777
3532341359 4643452461575456357268656746837976785794
3572234643 4683345754579445686568155679767926678187
5347643852 6458754963756986517486719762859782187396
3425351743 4536462854564757396567586841767869795287
4533266713 5644377824675548893578665991468977611257
4496184175 5517295286662831639777394274188841538529
4624616915 5735727126684683823779579493488168151459
5469844652 6571955763768216687487932779859814388196
6937364893 7148475914825958612593616972361472718347
1796741444 2817852555392896366641391747775241285888
4643452461 5754563572686567468379767857948187896815
4683345754 5794456865681556797679266781878137789298
6458754963 7569865174867197628597821873961893298417
4536462854 5647573965675868417678697952878971816398
5644377824 6755488935786659914689776112579188722368
5517295286 6628316397773942741888415385299952649631
5735727126 6846838237795794934881681514599279262561
6571955763 7682166874879327798598143881961925499217
7148475914 8259586125936169723614727183472583829458
2817852555 3928963666413917477752412858886352396999
5754563572 6865674683797678579481878968159298917926
5794456865 6815567976792667818781377892989248891319
7569865174 8671976285978218739618932984172914319528
5647573965 6758684176786979528789718163989182927419
6755488935 7866599146897761125791887223681299833479

Equipped with the full map, you can now find a path from the top left corner 
to the bottom right corner with the lowest total risk

The total risk of this path is 315 (the starting position is still 
never entered, so its risk is not counted).

Using the full map, what is the lowest total risk of any path 
from the top left to the bottom right?
"""

import sys
import unittest
from collections import Callable
from pathlib import Path
from typing import Dict, NamedTuple
from typing import TypeVar

from ivonet.files import read_int_matrix
from ivonet.grid import neighbors_defined_grid
from ivonet.iter import ints
from ivonet.search import astar

sys.dont_write_bytecode = True

T = TypeVar('T')


class MazeLocation(NamedTuple):
    row: int
    col: int


def manhattan_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation) -> float:
        xdist: int = abs(ml.col - goal.col)
        ydist: int = abs(ml.row - goal.row)
        return xdist + ydist

    return distance


def is_goal(goal: MazeLocation) -> Callable[[MazeLocation], bool]:
    def reached(current: MazeLocation) -> bool:
        return current == goal

    return reached


def adjoining(height, width) -> Callable[[MazeLocation], list[MazeLocation]]:
    def adjacent(ml: MazeLocation) -> list[MazeLocation]:
        nb = [MazeLocation(r, c) for r, c in
              neighbors_defined_grid((ml.row, ml.col), grid=(width, height), diagonal=False)]
        return nb

    return adjacent


def cost_calculator(risks: Dict[MazeLocation, int]) -> Callable[[MazeLocation], int]:
    def get_cost(ml: MazeLocation) -> int:
        return risks[ml]

    return get_cost


def make_risk_map(grid: list[list[int]]) -> Dict[MazeLocation, int]:
    risks: Dict[MazeLocation, int] = {}
    for r, row in enumerate(grid):
        for c, risk in enumerate(row):
            risks[MazeLocation(r, c)] = risk
    return risks


def make_extended_risk_map(risks: Dict[MazeLocation, int], width, height) -> Dict[MazeLocation, int]:
    expanded_risks: Dict[MazeLocation, int] = {}
    for k, v in risks.items():
        for r in range(5):
            for c in range(5):
                increase = r + c
                value = 1 + (v + increase - 1) % 9
                expanded_risks[MazeLocation(k.row + r * height, k.col + c * width)] = value
    return expanded_risks


def part_1(source):
    rows = len(source)
    cols = len(source[0])
    start = MazeLocation(0, 0)
    goal = MazeLocation(rows - 1, cols - 1)
    risks = make_risk_map(source)
    solution = astar(start,  # start at the start
                     is_goal(goal),  # callback function to see if the end goal has been reached
                     adjoining(rows, cols),  # callback to get all the relevant neighbors of a MazeLocation
                     manhattan_distance(goal),  # No diagonals allowed so the Manhattan distance calculator callback
                     cost_calculator(risks))  # the cost of going a direction based on the Chiton risk per MazeLocation
    if solution:
        # print(solution)
        # print(node_to_path(solution))
        return solution.cost
    raise ValueError("Part 1: No solution found.")


def part_2(source):
    rows = len(source)
    cols = len(source[0])
    start = MazeLocation(0, 0)
    new_height = rows * 5
    new_width = cols * 5
    goal = MazeLocation(new_height - 1, new_width - 1)
    risks = make_extended_risk_map(make_risk_map(source), rows, cols)
    solution = astar(start,
                     is_goal(goal),
                     adjoining(new_height, new_width),
                     manhattan_distance(goal),
                     cost_calculator(risks))
    if solution:
        # print(solution)
        # print(node_to_path(solution))
        return solution.cost
    raise ValueError("Part 2: No solution found.")


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = ints(Path(__file__).name)[0]
        self.source = read_int_matrix(f"day_{day}.input")
        self.test_source = read_int_matrix("""1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581""")

    def test_example_data_part_1(self):
        self.assertEqual(40, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(458, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(315, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(2800, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
