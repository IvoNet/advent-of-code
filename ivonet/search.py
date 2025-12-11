# generic_search.py
# From Classic Computer Science Problems in Python Chapter 2
# Copyright 2018 David Kopec
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

from collections import deque
from typing import TypeVar, Iterable, Sequence, Generic, List, Callable, Any, Optional, Protocol

from ivonet.collection import PriorityQueue, Stack, Queue

T = TypeVar('T')
C = TypeVar("C", bound="Comparable")

DIRECTIONS = [
    (0, 1),  # right
    (0, -1),  # left
    (1, 0),  # down
    (-1, 0)  # up
]

def linear_contains(iterable: Iterable[T], key: T) -> bool:
    for item in iterable:
        if item == key:
            return True
    return False


class Comparable(Protocol):
    def __eq__(self, other: Any) -> bool:
        ...

    def __lt__(self: C, other: C) -> bool:
        ...

    def __gt__(self: C, other: C) -> bool:
        return (not self < other) and self != other

    def __le__(self: C, other: C) -> bool:
        return self < other or self == other

    def __ge__(self: C, other: C) -> bool:
        return not self < other


def binary_contains(sequence: Sequence[C], key: C) -> bool:
    low: int = 0
    high: int = len(sequence) - 1
    while low <= high:  # while there is still a search space
        mid: int = (low + high) // 2
        if sequence[mid] < key:
            low = mid + 1
        elif sequence[mid] > key:
            high = mid - 1
        else:
            return True
    return False


class Node(Generic[T]):
    def __init__(self, state: T, parent: Optional[Node], cost: float = 0.0, heuristic: float = 0.0) -> None:
        self.state: T = state
        self.parent: Optional[Node] = parent
        self.cost: float = cost
        self.heuristic: float = heuristic

    def __lt__(self, other: Node) -> bool:
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

    def __repr__(self) -> str:
        if self.parent:
            return f"state[{self.state}] - cost_calculator[{self.cost}] - parent[{self.parent.state}]"
        return f"state[{self.state}] - cost_calculator[{self.cost}] - parent[None]"


def _state_key(state: Any) -> Any:
    """Return a hashable key for a state, converting common unhashable types.

    - lists -> tuples (recursively)
    - tuples -> tuples (with recursive conversion of elements)
    - dicts -> tuple of sorted (key, value_key)
    - sets -> tuple of sorted element keys
    - otherwise: return the state itself if hashable, else repr(state)
    """
    try:
        hash(state)
        return state
    except TypeError:
        # handle common container types
        if isinstance(state, list):
            return tuple(_state_key(x) for x in state)
        if isinstance(state, tuple):
            return tuple(_state_key(x) for x in state)
        if isinstance(state, dict):
            # sort items to produce a deterministic key
            return tuple((k, _state_key(v)) for k, v in sorted(state.items()))
        if isinstance(state, set):
            return tuple(sorted(_state_key(x) for x in state))
        # last resort: use repr (deterministic for immutable contents)
        return repr(state)


def dfs(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], list[T]]) -> Optional[Node[T]]:
    """Depth first search
    """
    # frontier is where we've yet to go
    frontier: Stack[Node[T]] = Stack()
    frontier.push(Node(initial, None))
    # explored is where we've been (store keys)
    explored: set[Any] = {_state_key(initial)}

    # keep going while there is more to explore
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # if we found the goal, we're done
        if goal_test(current_state):
            return current_node
        # check where we can go next and haven't explored
        for child in successors(current_state):
            k = _state_key(child)
            if k in explored:  # skip children we already explored
                continue
            explored.add(k)
            frontier.push(Node(child, current_node))
    return None  # went through everything and never found goal


def node_to_path(node: Node[T]) -> List[T]:
    path: List[T] = [node.state]
    # work backwards from end to front
    while node.parent is not None:
        node = node.parent
        path.append(node.state)
    path.reverse()
    return path


def bfs(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], list[T]]) -> Optional[Node[T]]:
    """Breath first search

    See for a nice implementation with extra's see:
    - Year 2016 day 11
    - Year 2022 day 12
    - Year 2023 day 10
    - year 2024 day 18 - Twist with a new blockage every step
    - year 2025 day 10 - part 1 twist with not being a grid
    """
    # frontier is where we've yet to go
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(initial, None))
    # explored is where we've been (store keys)
    explored: set[Any] = {_state_key(initial)}

    # keep going while there is more to explore
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # if we found the goal, we're done
        if goal_test(current_state):
            return current_node
        # check where we can go next and haven't explored
        for child in successors(current_state):
            k = _state_key(child)
            if k in explored:  # skip children we already explored
                continue
            explored.add(k)
            frontier.push(Node(child, current_node))
    return None  # went through everything and never found goal


def bfs_shortest(start, end, grid):
    """fastest path from start to end
    :returns: distance, path
    """
    q = deque([(start, 0, [start])])
    seen = {start}
    while q:
        (r, c), dist, path = q.popleft()
        if (r, c) == end:
            return dist, path
        for dr, dc in DIRECTIONS:
            rr, cc = r + dr, c + dc
            if 0 <= rr < len(grid) and 0 <= cc < len(grid[0]) and grid[rr][cc] != "#" and (rr, cc) not in seen:
                seen.add((rr, cc))
                q.append(((rr, cc), dist + 1, path + [(rr, cc)]))
    return None, []


def bfs_shortest_with_distance(start, end, grid):
    """fastest path from start to end
    :returns: distance, [(path, dist)]
    """
    q = deque([(start, 0, [(start, 0)])])
    seen = {start}
    while q:
        (r, c), dist, path = q.popleft()
        if (r, c) == end:
            return dist, path
        for dr, dc in DIRECTIONS:
            rr, cc = r + dr, c + dc
            if 0 <= rr < len(grid) and 0 <= cc < len(grid[0]) and grid[rr][cc] != "#" and (rr, cc) not in seen:
                seen.add((rr, cc))
                q.append(((rr, cc), dist + 1, path + [((rr, cc), dist + 1)]))
    return None, []

def astar(initial: T,
          goal_test: Callable[[T], bool],
          successors: Callable[[T], list[T]],
          heuristic: Callable[[T], float],
          cost: Callable[[T], int]) -> Optional[Node[T]]:
    """The A* (astar)

    The A* (A-star) algorithm is a popular pathfinding and graph traversal algorithm used to find the
    shortest path between a start node and a goal node. It combines the strengths of Dijkstra's algorithm
    and Greedy Best-First-Search by using both the actual cost from the start node and a heuristic
    `estimate of the cost to reach the goal.

    is a dfs but you can provide a cost callback function that can direct your search
    - see 2021/Day15 of the Advent of Code for an implementation example
    - see 2022/Day17 for an implementation with a twist (max steps in a direction and how many steps before turning)
    """
    # frontier is where we've yet to go
    frontier: PriorityQueue[Node[T]] = PriorityQueue()
    frontier.push(Node(initial, None, 0.0, heuristic(initial)))
    # explored is where we've been (store keys -> cost)
    explored: dict[Any, float] = {_state_key(initial): 0.0}

    # keep going while there is more to explore
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # if we found the goal, we're done
        if goal_test(current_state):
            return current_node
        # check where we can go next and haven't explored
        for nb in successors(current_state):
            new_cost: float = current_node.cost + cost(nb)
            k = _state_key(nb)

            if k not in explored or explored[k] > new_cost:
                explored[k] = new_cost
                frontier.push(Node(nb, current_node, new_cost, heuristic(nb)))
    return None  # went through everything and never found goal

def all_the_paths_from_start_end(start, end, grid) -> list[list[tuple[int, int]]]:
    """all paths from start to end
    :returns: list of paths
    """
    paths = []
    q = deque([(start, [start])])
    seen = {start}
    while q:
        (r, c), path = q.popleft()
        if (r, c) == end:
            paths.append(path)
            continue
        for dr, dc in DIRECTIONS:
            rr, cc = r + dr, c + dc
            if 0 <= rr < len(grid) and 0 <= cc < len(grid[0]) and grid[rr][cc] != "#" and (rr, cc) not in seen:
                seen.add((rr, cc))
                q.append(((rr, cc), path + [(rr, cc)]))
    return paths

if __name__ == "__main__":
    print(linear_contains([1, 5, 15, 15, 15, 15, 20], 5))  # True
    print(binary_contains(["a", "d", "e", "f", "z"], "f"))  # True
    print(binary_contains(["john", "mark", "ronald", "sarah"], "sheila"))  # False
