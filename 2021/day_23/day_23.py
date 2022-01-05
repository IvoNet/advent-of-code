#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

Note that my submitted solution I did by hand and this version came a couple of weeks later :-)
Took me a very long time to figure this one out and e bit of light reading into search patterns

             1
  0123456789012
 0#############
 1#..X.X.X.X..#  <- hallway 11 long
 2###C#B#D#D###
 3  #B#C#A#A#
 4  #########
     ^ ^ ^ ^
col: A B C D  (side rooms)
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

Good idea but I had no idea on how to represent this grid and ask for successors
so after long thinking I came up with a one dimentional grid

"...........ABCDABCD"
This made calculating easier (not much)

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
from typing import Generator

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


def parse(source):
    """Parses the source into a single string with all # removed. That is the state/grid used"""
    return "".join(c for row in source for c in row.strip() if c not in "#")


def gen_left_right():
    """generates the possible left and right movements from a side room
    Note that the left is reversed. Took me forever to find this out!
    but while walking left you walk "the other way around" OMG!
    So what happends here:
    - the hallway has a range of 10 (inclusive) spots but the door locations are not available for standing on
    - from the first door location (2) going left would mean positions [0, 1] in the hallway available except walking that way
      the order should be [1, 0] and walking from the second doorway (pos 4) would have [3, 1, 0] as stop options and so on
    - going right from the first door would have [3, 5, 7, 9, 10] as viable stopping locations.
      these are already in the correct ordering
    """
    hallway = range(11)
    left = {}
    right = {}
    for k, v in HALL_DOOR.items():
        left[v] = [x for x in hallway[:v] if x not in HALL_DOOR.values()][::-1]  # reverse important for distance!
        right[v] = [x for x in hallway[v:] if x not in HALL_DOOR.values()]
    return left, right


def is_goal(solution: str) -> Callable[[T], bool]:
    """callback to check if the goal has been reached"""
    def reached(state) -> bool:
        return solution == state

    return reached


def manhatten_distances(goal) -> callable:
    """Distance in this puzzle is not as straight forward as it in an normal grid.
    I still call it a manhatten distance as I am still calculating in "straight lines"
    but a I created a formula for it
    ############# (inclusive)      ############# distance betwee @ and * is like distance between
    #...........# 0..10            #@..&.....!.# pos 0 and pos 11 and that is 3
    ###B#C#B#D### 11..14     ==>   ###*#%#B#D### and between @ and $
      #A#D#C#A#   15..18             #A#D#C#$#   pos 0 and pos 18 -> dist 10 (largest distance)
      #########                      #########   (*,%) -> (11,12) -> does not happen as we always walk from a
                                                                     hallway to a room!
    - (&,%) -> (3,12) -> distance 2
    - (&,$) -> (3,18) -> distance 7
    - (!,*) -> (9,11) -> distance 8
    - (A,!) -> (15,9) -> distance 9
    - the postions do not matter for the distance left/right or right/left distance is the same
    - I made a dictionary with all the possible distances between two points and that in actual fact
      twice as the position does not matter
    - all the possibilities can be found by finding the product of all the possible distances.
      these are the hallway and siderooms.
    - a distance is always positive so first find the distance to the corresponding sideroom from the left
    So how to calculate this:
    - starting out with the product of all hallway positions with the siderooms
      so product of (hallway, sideroom) combinations
    - first find the door belonging to the sideroom we want to calculate
      e.g. (!,*) -> (9,11) -> distance 8
      * 11 belongs to sideroom A and it has door 2.
      * distance between hallway items is the absolute value of door minus the hallway value abs(2 - 9) = 7
      * now we need to know how much extra we need to add to this distance.
        there are 4 rooms with a depth. so either 1 or 2 extra steps
        e.g. sideroom A has positions 11 and 15 in the one dimentional state. 11 needs to add 1 extra step and 15 two
             sideroom B has positions 12 and 16 in the one dimentional state. 12 needs to add 1 extra step and 16 two
             sideroom C has positions 13 and 17 in the one dimentional state. 13 needs to add 1 extra step and 17 two
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
    _, reverse_side_room_target = gen_side_room_target(goal)
    distances = {}
    for left, right in product(HALLWAY, range(11, len(goal))):
        distances[(left, right)] = abs(HALL_DOOR[reverse_side_room_target[right]] - left) + (right - 7) // 4
        distances[(right, left)] = distances[(left, right)]

    def distance(positions):
        return distances[positions]

    return distance


def gen_side_room_target(goal):
    """In a one dimentional grid I need to calculate the locations of where A,B,C,D must go
    so I find the index of these in the goal (finished) state and save them as a dictionary.

    Later I found out that I also needed to be able to lookup the reverse like having an index and
    finding out which item should go there. As all the locations and stuff are unique
    I did a reverse dict kinda exercise.
    """
    side_room_target = {
        "A": [i for i, el in enumerate(goal) if el == "A"],
        "B": [i for i, el in enumerate(goal) if el == "B"],
        "C": [i for i, el in enumerate(goal) if el == "C"],
        "D": [i for i, el in enumerate(goal) if el == "D"],
    }
    reverse_side_room_target = {v: k for k, v in side_room_target.items() for v in v}
    return side_room_target, reverse_side_room_target


def hallway_blocked(loc, state) -> bool:
    """See if the hallway is blocked for the amphipod at loc in state to the
    sideroom it belongs to.
    If blocked we kan not walk...
    This function is only called where state[loc] actually holds a amphipod.
    """
    door_loc = HALL_DOOR[state[loc]]
    step = 1 if loc < door_loc else -1
    for v in range(loc + step, door_loc + step, step):
        if state[v] != ".":
            return True
    return False


def can_enter_room(goal):
    """Callback function to see if an amphipod at loc in state can enter its sideroom"""
    side_room_target, _ = gen_side_room_target(goal)

    def can_enter(loc, state) -> int | bool:
        """See if amphipod at state[loc] can enter it target sideroom
        - assume we can not and it has to be proven we can
        - find the target sideroom
        - see if there is empty space in the sideroom and if all the states are of their own type
        - now check if the hallway is free and go...
        - fail if any of the rulez are not met.
        """
        ret = False
        amphibod = state[loc]
        target = side_room_target[amphibod]
        for i in target:
            if state[i] == ".":
                ret = i
            elif state[i] != state[loc]:
                return False
        if not hallway_blocked(loc, state):
            return ret
        return False

    return can_enter


def can_leave_room(goal):
    """Callback function to check if an amphipod can leave its sideroom"""
    side_room_target, _ = gen_side_room_target(goal)

    def can_leave(room, state) -> int | bool:
        """Check if an amphipod in from a given sideroom can leave
        So:
        - if a sideroom has already been solved it can never leave again
        - check for all locations in the room from top to bottom if it contains
          an amphipod and if so it can leave
        - fail if any of these conditions are not met.
        """
        if all(state[i] == room for i in side_room_target[room] if state[i] != "."):
            return False
        for i in side_room_target[room]:
            if state[i] != ".":
                return i
        return False

    return can_leave


def hallway_positions(goal):
    """callback function to give all open hallway positions"""
    left, right = gen_left_right()
    side_room_target, reverse_side_room_target = gen_side_room_target(goal)

    def options(loc, state):
        """Generate all hallway positions a given amphipod at state[loc] can move to
        - we find all positions to the left and right of our door
        - we can only walk from our sideroom to any location in the hallway if the space is empty
        - generate locations lef and right as long as these conditions are met.
        """
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
    """Swap the left and right positions in the state
    When we descide to move we actially swap two positions we have found to be acceptable
    - this is always an empty spot with an amphipod.
    """
    ret = list(state)
    ret[left], ret[right] = ret[right], ret[left]
    return "".join(ret)


def successors(goal) -> Callable[[T], tuple[int, int]]:
    """Calback function that generates all possible moves from a given state.
    """
    can_enter = can_enter_room(goal)
    can_leave = can_leave_room(goal)
    hallway_options = hallway_positions(goal)

    def options(state: T) -> Generator:
        """Generate combinations of swappable spaces
        So:
        - first check the hallway for amphipods and if they can enter their sideroom
        - then check rooms if they can leave to the hallway and if so
          find all hallway locations it can leave to
        - do this as long as there is something to yield
        """
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
    """Callback function to get the cost of an amphipod"""
    return COST[state[loc]]


def astar(initial: T,
          goal_test: Callable[[T], bool],
          successors: Callable[[T], List[T]],
          heuristic: Callable[[T], float],
          cost: Callable[[T], int]) -> Optional[Node[T]]:
    """The A* (astar)
    is a dfs but you can provide a cost callback function that can direct your search
    in this adjusted version of the astar the heuristic (distance) function is used in the cost calulation and not
    seperately as a priority thing.
    """
    # frontier is where we've yet to go
    frontier: PriorityQueue[Node[T]] = PriorityQueue()
    frontier.push(Node(initial, None))
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
