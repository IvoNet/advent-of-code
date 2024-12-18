#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from collections import deque
from typing import Callable, Optional

from ivonet.collection import Queue


def bfs(start: tuple[int, int],
        is_goal: Callable[[tuple[int, int]], bool],
        successors: Callable[[tuple[int, int]], list[tuple[int, int]]]) -> Optional[tuple[int, int]]:
    """Breath first search """
    frontier = Queue()
    frontier.push((start, 0))
    explored: set[tuple[int, int]] = {start}

    while not frontier.empty:
        current_state, distance = frontier.pop()
        if is_goal(current_state):
            return current_state, distance
        for child in successors(current_state):
            if child in explored:
                continue
            explored.add(child)
            frontier.push((child, distance + 1))
    return None


def bfs_2(start, end, grid, wall="#"):
    def successors(state):
        ret = []
        r, c = state
        for dir in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            rr, cc = r + dir[0], c + dir[1]
            if 0 <= rr < 10 and 0 <= cc < 10 and grid[rr][cc] != wall:
                ret.append((rr, cc))
        return ret

    def is_goal(state):
        return state == end

    """Breath first search """
    frontier = deque([start, 0])
    seen: set()

    while not frontier.empty:
        current_state, distance = frontier.pop()
        if is_goal(current_state):
            return current_state, distance
        for child in successors(current_state):
            if child in seen:
                continue
            seen.add(child)
            frontier.push((child, distance + 1))
    return None


def bfs_3(start, end, grid, wall="#"):
    queue = deque([start, 0])  # start, distance
    seen = set()

    while queue:
        current_state, distance = queue.pop()
        if current_state == end:  # change this to your goal state
            return current_state, distance
        if current_state in seen:
            continue
        seen.add(current_state)
        r, c = current_state
        for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            child = (rr, cc) = r + dr, c + dc
            if 0 <= rr < 10 and 0 <= cc < 10 and grid[rr][cc] != wall:
                seen.add(child)
                queue.append((child, distance + 1))
    return None
