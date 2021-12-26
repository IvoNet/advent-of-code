#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from dataclasses import dataclass
from pathlib import Path

from ivonet.files import read_rows
from ivonet.graph import WeightedGraph
from ivonet.iter import ints
from ivonet.search import PriorityQueue

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


@dataclass
class DijkstraNode:
    vertex: int
    distance: float

    def __lt__(self, other: DijkstraNode) -> bool:
        return self.distance < other.distance

    def __eq__(self, other: DijkstraNode) -> bool:
        return self.distance == other.distance


def dijkstra(wg: WeightedGraph[V], root: V) -> Tuple[List[Optional[float]], Dict[int, WeightedEdge]]:
    first: int = wg.index_of(root)  # find starting index
    # distances are unknown at first
    distances: List[Optional[float]] = [None] * wg.vertex_count
    distances[first] = 0  # the root is 0 away from the root
    path_dict: Dict[int, WeightedEdge] = {}  # how we got to each vertex
    pq: PriorityQueue[DijkstraNode] = PriorityQueue()
    pq.push(DijkstraNode(first, 0))

    while not pq.empty:
        u: int = pq.pop().vertex  # explore the next closest vertex
        dist_u: float = distances[u]  # should already have seen it
        # look at every edge/vertex from the vertex in question
        for we in wg.edges_for_index(u):
            # the old distance to this vertex
            dist_v: float = distances[we.v]
            # no old distance or found shorter path
            if dist_v is None or dist_v > we.weight + dist_u:
                # update distance to this vertex
                distances[we.v] = we.weight + dist_u
                # update the edge on the shortest path to this vertex
                path_dict[we.v] = we
                # explore it soon
                pq.push(DijkstraNode(we.v, we.weight + dist_u))

    return distances, path_dict


# Helper function to get easier access to dijkstra results
def distance_array_to_vertex_dict(wg: WeightedGraph[V], distances: List[Optional[float]]) -> Dict[V, Optional[float]]:
    distance_dict: Dict[V, Optional[float]] = {}
    for i in range(len(distances)):
        distance_dict[wg.vertex_at(i)] = distances[i]
    return distance_dict


def total_weight(wp: WeightedPath) -> float:
    return sum([e.weight for e in wp])


def print_weighted_path(wg: WeightedGraph, wp: WeightedPath) -> None:
    for edge in wp:
        print(f"{wg.vertex_at(edge.u)} {edge.weight}> {wg.vertex_at(edge.v)}")
    print(f"Total Weight: {total_weight(wp)}")


# Takes a dictionary of edges to reach each node and returns a list of
# edges that goes from `start` to `end`
def path_dict_to_path(start: int, end: int, path_dict: Dict[int, WeightedEdge]) -> WeightedPath:
    if len(path_dict) == 0:
        return []
    edge_path: WeightedPath = []
    e: WeightedEdge = path_dict[end]
    edge_path.append(e)
    while e.u != start:
        e = path_dict[e.u]
        edge_path.append(e)
    return list(reversed(edge_path))


def mst(wg: WeightedGraph[V], start: int = 0) -> Optional[WeightedPath]:
    if start > (wg.vertex_count - 1) or start < 0:
        return None
    result: WeightedPath = []  # holds the final MST
    pq: PriorityQueue[WeightedEdge] = PriorityQueue()
    visited: List[bool] = [False] * wg.vertex_count  # where we've been

    def visit(index: int):
        visited[index] = True  # mark as visited
        for edge in wg.edges_for_index(index):
            # add all edges coming from here to pq
            if not visited[edge.v]:
                pq.push(edge)

    visit(start)  # the first vertex is where everything begins

    while not pq.empty:  # keep going while there are edges to process
        edge = pq.pop()
        if visited[edge.v]:
            continue  # don't ever revisit
        # this is the current smallest, so add it to solution
        result.append(edge)
        visit(edge.v)  # visit where this connects

    return result


def part_1(source):
    cities = set()
    combis = []
    for line in source:
        city1, to, city2, equal, distance = line.split()
        cities.add(city1)
        cities.add(city2)
        combis.append((city1, city2, distance))

    city_graph: WeightedGraph[str] = WeightedGraph(list(cities))
    for c1, c2, d in combis:
        city_graph.add_edge_by_vertices(c1, c2, int(d))

    for i in range(city_graph.vertex_count):
        result: Optional[WeightedPath] = mst(city_graph, start=i)
        print()
        if result is None:
            print("No solution found!")
        else:
            print_weighted_path(city_graph, result)

    return 0


def part_2(source):
    return 0


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"day_{day.zfill(2)}.input")
        self.test_source = read_rows("""London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141""")

    def test_example_data_part_1(self):
        self.assertEqual(None, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(None, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
