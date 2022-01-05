#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
             1
  0123456789012
 0#############
 1#..X.X.X.X..#  <- hallway 11 long
 2###C#B#D#D###
 3  #B#C#A#A#
 4  #########
     ^ ^ ^ ^
col: A B C D
Rules:
- # is a wall
- . is empty space
    - Eleven open spaces
- X is empty space where you can not stop
- A's need to go into the A lane
- B's / C's / D's need to go ....
- Lanes -> No Stop
    A -> 2
    B -> 4
    C -> 6
    D -> 8
- Cost 1 move:
   A -> 1
   B -> 10
   C -> 100
   D -> 1000

Grid -> Astar?
#############
#..X.X.X.X..#
###C#B#D#D###
###B#C#A#A###
#############
Going for a* function...
Astar needs:
- initial state
- callable to test if goal has been reached
- callable to get the list of successors
- callable to get the heuristic (distance to the goal)
- callable for the cost calculation
"""

import sys
import unittest
from enum import IntEnum
from itertools import product
from pathlib import Path

from ivonet.collection import PriorityQueue
from ivonet.files import read_rows
from ivonet.iter import ints
from ivonet.search import astar, Node, node_to_path

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


HALL_DOOR = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8,
}

COST = {"A": 1,
        "B": 10,
        "C": 100,
        "D": 1000
        }

HALLWAY = [0, 1, 3, 5, 7, 9, 10]
ROOMS = "ABCD"


class Amphipod(IntEnum):
    A = 1
    B = 10
    C = 100
    D = 1000


COLS = {
    Amphipod.A: 2,
    Amphipod.B: 4,
    Amphipod.C: 6,
    Amphipod.D: 8,
}


def gen_left_right():
    """generates the possible left and right movements from a side room"""
    hallway = range(11)
    left = {}
    right = {}
    for k, v in HALL_DOOR.items():
        left[v] = [x for x in hallway[:v] if x not in HALL_DOOR.values()][::-1]  # reverse important for distance!
        right[v] = [x for x in hallway[v:] if x not in HALL_DOOR.values()]
    return left, right


def parse(source):
    return "".join(c for row in source for c in row.strip() if c not in "#")


def is_goal(solution: str) -> Callable[[T], bool]:
    def reached(state) -> bool:
        return solution == state

    return reached


def manhatten_distances(goal) -> callable:
    """Distance in this puzzle is not as straight forward as it seems
    a linear translation needs to be made

    TODO explain :-)
    """
    _, reverse_side_room_target = gen_side_room_target(goal)
    distances = {}
    for left, right in product(HALLWAY, range(11, len(goal))):
        distances[(left, right)] = abs(HALL_DOOR[reverse_side_room_target[right]] - left) + (right - 7) // 4
        distances[(right, left)] = distances[(left, right)]

    def distance(positions):
        if not isinstance(positions, tuple):  # for initial heuristic
            return 0  # TODO Tune this
        return distances[positions]

    return distance


def gen_side_room_target(goal):
    side_room_target = {
        "A": [i for i, el in enumerate(goal) if el == "A"],
        "B": [i for i, el in enumerate(goal) if el == "B"],
        "C": [i for i, el in enumerate(goal) if el == "C"],
        "D": [i for i, el in enumerate(goal) if el == "D"],
    }
    reverse_side_room_target = {v: k for k, v in side_room_target.items() for v in v}
    return side_room_target, reverse_side_room_target


def blocked(loc, state):
    door_loc = HALL_DOOR[state[loc]]
    step = 1 if loc < door_loc else -1
    for v in range(loc + step, door_loc + step, step):
        if state[v] != ".":
            return True
    return False


def can_enter_room(goal):
    side_room_target, _ = gen_side_room_target(goal)

    def can_enter(loc, state) -> int | bool:
        ret = False
        amphibod = state[loc]
        target = side_room_target[amphibod]
        for i in target:
            if state[i] == ".":
                ret = i
            elif state[i] != state[loc]:
                return False
        if not blocked(loc, state):
            return ret
        return False

    return can_enter


def can_leave_room(goal):
    side_room_target, _ = gen_side_room_target(goal)

    def can_leave(room, state) -> int | bool:
        if all(state[i] == room for i in side_room_target[room] if state[i] != "."):
            return False
        for i in side_room_target[room]:
            if state[i] != ".":
                return i
        return False

    return can_leave


def hallway_positions(goal):
    left, right = gen_left_right()
    side_room_target, reverse_side_room_target = gen_side_room_target(goal)

    def options(loc, state):
        door = HALL_DOOR[reverse_side_room_target[loc]]
        for r_loc in left[door]:
            if state[r_loc] != ".":
                break
            yield r_loc
        for r_loc in right[door]:
            if state[r_loc] != ".":
                break
            yield r_loc

    return options


def swap(left, right, state):
    ret = list(state)
    ret[left], ret[right] = ret[right], ret[left]
    return "".join(ret)


def successors(goal) -> Callable[[T], tuple[int, int]]:
    """Possible move rulez:
    - empty never moves (can be swapped)
    - need to check if a Amphipod can enter or leave a room
    """
    can_enter = can_enter_room(goal)
    can_leave = can_leave_room(goal)
    hallway_options = hallway_positions(goal)

    def options(state: T) -> tuple[int, int]:
        for left in HALLWAY:
            if state[left] == '.':
                continue
            right = can_enter(left, state)
            if not right:
                continue
            yield left, right
        for room in ROOMS:
            left = can_leave(room, state)
            if not left:
                continue
            for right in hallway_options(left, state):
                yield left, right

    return options


def cost_calc(loc, state) -> int:
    return COST[state[loc]]


def astar(initial: T,
          goal_test: Callable[[T], bool],
          successors: Callable[[T], List[T]],
          heuristic: Callable[[T], float],
          cost: Callable[[T], int]) -> Optional[Node[T]]:
    """The A* (astar)
    is a dfs but you can provide a cost callback function that can direct your search
    """
    # frontier is where we've yet to go
    frontier: PriorityQueue[Node[T]] = PriorityQueue()
    frontier.push(Node(initial, None, 0.0, 0))
    # explored is where we've been
    explored: Dict[T, float] = {initial: 0.0}

    # keep going while there is more to explore
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # if we found the goal, we're done
        if goal_test(current_state):
            return current_node
        # check where we can go next and haven't explored
        for left, right in successors(current_state):
            new_cost: float = current_node.cost + heuristic((left, right)) * cost(left, current_state)
            new_state = swap(left, right, current_state)
            if new_state not in explored or explored[new_state] > new_cost:
                explored[new_state] = new_cost
                frontier.push(Node(new_state, current_node, new_cost))
    return None  # went through everything and never found goal


def state_print(state):
    print(
        "#############\n#{}{}{}{}{}{}{}{}{}{}{}#\n###{}#{}#{}#{}###\n  #{}#{}#{}#{}#\n  #########".format(*list(state)))


def state_print_2(state):
    print(
        "#############\n#{}{}{}{}{}{}{}{}{}{}{}#\n###{}#{}#{}#{}###\n  #{}#{}#{}#{}#\n  #{}#{}#{}#{}#  \n  #{}#{}#{}#{}#\n  #########".format(
            *list(state)))


def part_1(source):
    """a* needs:
    - initial state
    - callable to test if goal has been reached
    - callable to get the list of successors
    - callable to get the heuristic (distance to the goal)
    - callable for the cost calculation
    Thinking in one dimention is way easier so doing that
    """

    goal = "...........ABCDABCD"
    solution = astar(parse(source),
                     is_goal(goal),
                     successors(goal),
                     manhatten_distances(goal),
                     cost_calc)
    if DEBUG:
        pad = node_to_path(solution)
        for p in pad:
            state_print(p)
    return solution.cost


def part_2(source):
    goal = "...........ABCDABCDABCDABCD"
    solution = astar(parse(source),
                     is_goal(goal),
                     successors(goal),
                     manhatten_distances(goal),
                     cost_calc)
    if DEBUG:
        pad = node_to_path(solution)
        for p in pad:
            state_print_2(p)
    return solution.cost


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}.input")))
        self.source2 = read_rows(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}_2.input")))
        self.test_source = read_rows("""#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########""")
        self.test_source2 = read_rows("""#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########""")

    def test_example_data_part_1(self):
        self.assertEqual(12521, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(10321, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(44169, part_2(self.test_source2))

    def test_part_2(self):
        self.assertEqual(46451, part_2(self.source2))


if __name__ == '__main__':
    unittest.main()
