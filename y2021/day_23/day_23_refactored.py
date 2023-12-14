#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

Note that my submitted solution I did by hand and this version came a couple of weeks later :-)
Took me a very long time to figure this one out and e bit of light reading into search patterns

Grid -> Astar?
#############
#..X.X.X.X..#
###C#B#D#D###
###B#C#A#A###
#############

Good idea but I had no idea on how to represent this grid and ask for successors
so after long thinking I came up with a one dimentional grid

"...........ABCDABCD"
This made calculating easier (not much :-))

Going for a* function...
Astar needs:
- initial state
- callable to test if goal has been reached
- callable to get the list of successors
- callable to get the heuristic (distance to the goal) but not separate as it has a direct 
  effect on the cost and sometimes you must walk more than one step
- callable for the cost calculation
"""

import sys
import unittest
from itertools import product
from pathlib import Path
from typing import Generator, Optional

from ivonet.collection import PriorityQueue
from ivonet.files import read_rows
from ivonet.iter import ints
from ivonet.search import Node, node_to_path

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def parse(source):
    """Parses the source into a single string with all # removed. That is the state/grid used"""
    return "".join(c for row in source for c in row.strip() if c not in "#")


class AmphibodPuzzle:

    def __init__(self, initial, goal) -> None:
        self.goal = goal
        self.initial = initial
        self.hall_door = {
            "A": 2,
            "B": 4,
            "C": 6,
            "D": 8,
        }
        self.cost = {"A": 1,
                     "B": 10,
                     "C": 100,
                     "D": 1000
                     }
        self.hallway = [0, 1, 3, 5, 7, 9, 10]
        self.rooms = "ABCD"
        self.left, self.right = self.__gen_left_right_movement_options_from_side_rooms()
        self.side_room_target, self.reverse_side_room_target = self.__gen_side_room_target()
        self.distances = self.__gen_manhatten_distances()

    def __gen_left_right_movement_options_from_side_rooms(self):
        """generates the possible left and right movements from a side room
        Note that the left is reversed. Took me forever to find this out!
        but while walking left you walk "the other way around" OMG!
        So what happens here:
        - the hallway has a range of 10 (inclusive) spots but the door locations are not available for standing on
        - from the first door location (2) going left would mean positions [0, 1] in the hallway available except
          walking that way
          the order should be [1, 0] and walking from the second doorway (pos 4) would have [3, 1, 0] as stop options
          and so on
        - going right from the first door would have [3, 5, 7, 9, 10] as viable stopping locations.
          these are already in the correct ordering
        - I tried doing this with the hallway as defined but with a range of 11 and than filtering out the side-room
          doors proved easier
        """
        hallway = range(11)
        left = {}
        right = {}
        for k, v in self.hall_door.items():
            left[v] = [x for x in hallway[:v] if x not in self.hall_door.values()][::-1]
            right[v] = [x for x in hallway[v:] if x not in self.hall_door.values()]
        return left, right

    def __gen_side_room_target(self):
        """In a one dimensional grid I need to calculate the locations of where A,B,C,D must go
        so I find the index of these in the goal (finished) state and save them as a dictionary.

        Later I found out that I also needed to be able to lookup the reverse like having an index and
        finding out which item should go there. As all the locations and stuff are unique
        I did a reverse dict kinda exercise.
        """
        side_room_target = {
            "A": [i for i, el in enumerate(self.goal) if el == "A"],
            "B": [i for i, el in enumerate(self.goal) if el == "B"],
            "C": [i for i, el in enumerate(self.goal) if el == "C"],
            "D": [i for i, el in enumerate(self.goal) if el == "D"],
        }
        reverse_side_room_target = {v: k for k, v in side_room_target.items() for v in v}
        return side_room_target, reverse_side_room_target

    def __gen_manhatten_distances(self):
        """Distance in this puzzle is not as straight forward as it in an normal grid.
        I still call it a manhatten distance as I am still calculating in "straight lines"
        but a I created a formula for it
        ############# (inclusive)      ############# distance between @ and * is like distance between
        #...........# 0..10            #@..&.....!.# pos 0 and pos 11 and that is 3
        ###B#C#B#D### 11..14     ==>   ###*#%#B#D### and between @ and $
          #A#D#C#A#   15..18             #A#D#C#$#   pos 0 and pos 18 -> dist 10 (largest distance)
          #########                      #########   (*,%) -> (11,12) -> does not happen as we always walk from a
                                                                         hallway to a room!
        - (&,%) -> (3,12) -> distance 2
        - (&,$) -> (3,18) -> distance 7
        - (!,*) -> (9,11) -> distance 8
        - (A,!) -> (15,9) -> distance 9
        - the positions do not matter for the distance left/right or right/left distance is the same
        - I made a dictionary with all the possible distances between two points and that in actual fact
          twice as the position does not matter
        - all the possibilities can be found by finding the product of all the possible distances.
          these are between the hallway and side-rooms.
          We never walk from a room to a room. There is always a hallway passage
        - a distance is always positive
        So how to calculate this:
        - starting out with the product of all hallway positions with the side-rooms
          so product of (hallway, side-room) combinations
        - first find the door belonging to the side-room we want to calculate
          e.g. (!,*) -> (9,11) -> distance 8
          * 11 belongs to side-room A and it has door 2.
          * distance between hallway items is the absolute value of door minus the hallway value abs(2 - 9) = 7
          * now we need to know how much extra we need to add to this distance.
            there are 4 rooms with a depth. so either 1 or 2 extra steps (3 or 4 in part 2, but formula holds steady)
            e.g. side-room A has pos 11 and 15 in the one dimensional state. 11 needs to add 1 extra step and 15 two
                 side-room B has pos 12 and 16 in the one dimensional state. 12 needs to add 1 extra step and 16 two
                 side-room C has pos 13 and 17 in the one dimensional state. 13 needs to add 1 extra step and 17 two
                 ...
            A            B            C
            11 - 7 = 4   12 - 7 = 5   13 - 7 = 6      -> // 4 = 1
            15 - 7 = 8   16 - 7 = 9   17 - 7 = 10     -> // 4 = 2
            How to make these into 1 and two steps.
            hard div of 4 !
         - so final formula to calculate the distance is:
           abs(HALL_DOOR[reverse_side_room_target[right]] - left) + (right - 7) // 4
           (took me forever to figure this out!)
        """
        distances = {}
        for left, right in product(self.hallway, range(11, len(self.goal))):
            distances[(left, right)] = abs(self.hall_door[self.reverse_side_room_target[right]] - left) + (
                    right - 7) // 4
            distances[(right, left)] = distances[(left, right)]
        return distances

    def hallway_blocked(self, loc, state) -> bool:
        """See if the hallway is blocked for the amphipod at state[loc] to the
        side-room it belongs to.
        If blocked we kan not walk...
        This function is only called where state[loc] actually holds a amphipod.
        """
        door_loc = self.hall_door[state[loc]]
        step = 1 if loc < door_loc else -1
        for v in range(loc + step, door_loc + step, step):
            if state[v] != ".":
                return True
        return False

    def can_enter_room(self, loc, state) -> int | bool:
        """See if amphipod at state[loc] can enter it target side-room
        - assume we can not and it has to be proven we can
        - find the target side-room
        - see if all room space is empty or the one filled is of correct type
        - if not of correct type entering is not allowed
        - now check if the hallway is free and go...
        - fail if any of the rules are not met.
        """
        ret = False
        amphibod = state[loc]
        target = self.side_room_target[amphibod]
        for i in target:
            if state[i] == ".":
                ret = i
            elif state[i] != amphibod:
                return False
        if not self.hallway_blocked(loc, state):
            return ret
        return False

    def can_leave_room(self, room, state) -> int | bool:
        """Check if an amphipod from a given side-room can leave
        So:
        - if a side-room has already been solved it can never leave again
        - check for all locations in the room from top to bottom if it contains
          an amphipod and if so it can leave
        - fail if any of these conditions are not met.
        """
        if all(state[i] == room for i in self.side_room_target[room] if state[i] != "."):
            return False
        for i in self.side_room_target[room]:
            if state[i] != ".":
                return i
        return False

    def hallway_positions(self, loc, state):
        """Generate all hallway positions a given amphipod at state[loc] can move to
        - we find all positions to the left and right of our side-room door
        - we can only walk from our side-room to any location in the hallway if the space is empty
        - generate locations left and right as long as these conditions are met.
        """
        door = self.hall_door[self.reverse_side_room_target[loc]]
        for r_loc in self.left[door]:
            if state[r_loc] != ".":
                break
            yield r_loc
        for r_loc in self.right[door]:
            if state[r_loc] != ".":
                break
            yield r_loc

    @staticmethod
    def swap(left, right, state) -> str:
        """Swap the left and right positions in the state
        When we decide to move we actually swap two positions we have found to be acceptable
        - this is always an empty spot with an amphipod.
        """
        ret = list(state)
        ret[left], ret[right] = ret[right], ret[left]
        return "".join(ret)

    def successors(self, state: str) -> Generator:
        """Generate combinations of swappable spaces
        So:
        - first check the hallway for amphipods and if they can enter their side-room
        - then check rooms if they can leave to the hallway and if so
          find all hallway locations it can leave to
        - do this as long as there is something to yield
        """
        for left in self.hallway:
            if state[left] == '.':
                continue
            right = self.can_enter_room(left, state)
            if not right:
                continue
            yield left, right
        for room in self.rooms:
            left = self.can_leave_room(room, state)
            if not left:
                continue
            for right in self.hallway_positions(left, state):
                yield left, right

    def solve(self) -> Optional[Node[str]]:
        """The A* (astar) function
        is a dfs but you can provide a cost callback function that can direct your search
        """
        frontier: PriorityQueue[Node[str]] = PriorityQueue()
        frontier.push(Node(self.initial, None))
        explored: dict[str, float] = {self.initial: 0.0}
        while not frontier.empty:
            current_node: Node[str] = frontier.pop()
            current_state: str = current_node.state
            if self.goal == current_state:
                return current_node
            for left, right in self.successors(current_state):
                new_cost: float = current_node.cost + self.distances[(left, right)] * self.cost[current_state[left]]
                new_state = self.swap(left, right, current_state)
                if new_state not in explored or explored[new_state] > new_cost:
                    explored[new_state] = new_cost
                    frontier.push(Node(new_state, current_node, new_cost))
        return None


def state_print(state):
    if len(state) > 20:
        print(
            """#############
#{}{}{}{}{}{}{}{}{}{}{}#
###{}#{}#{}#{}###
  #{}#{}#{}#{}#
  #{}#{}#{}#{}#  
  #{}#{}#{}#{}#
  #########""".format(*list(state)))
    else:
        print(
            """#############
#{}{}{}{}{}{}{}{}{}{}{}#
###{}#{}#{}#{}###
  #{}#{}#{}#{}#
  #########""".format(*list(state)))


def part_1(source, goal="...........ABCDABCD"):
    puzzle = AmphibodPuzzle(parse(source), goal)
    solution = puzzle.solve()
    if DEBUG:
        pad = node_to_path(solution)
        for p in pad:
            state_print(p)
    return solution.cost


def part_2(source):
    return part_1(source, goal="...........ABCDABCDABCDABCD")


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}_a.input")))
        self.source2 = read_rows(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}_b.input")))
        self.test_source = read_rows(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}_test_a.input")))
        self.test_source2 = read_rows(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}_test_b.input")))

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
