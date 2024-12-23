#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__revised__ = "$revised: 26/12/2021 23:11$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

from copy import deepcopy
from dataclasses import dataclass
from typing import TypeVar, Generic, Optional

from ivonet.collection import Queue, PriorityQueue
from ivonet.search import Node

V = TypeVar('V')  # type of the vertices in the graph


@dataclass
class Edge:
    u: int  # the "from" vertex
    v: int  # the "to" vertex

    def reversed(self) -> Edge:
        return Edge(self.v, self.u)

    def __str__(self) -> str:
        return f"{self.u} -> {self.v}"


@dataclass
class WeightedEdge(Edge):
    weight: float

    def reversed(self) -> WeightedEdge:
        return WeightedEdge(self.v, self.u, self.weight)

    # so that we can order edges by weight to find the minimum weight edge
    def __lt__(self, other: WeightedEdge) -> bool:
        return self.weight < other.weight

    def __repr__(self) -> str:
        return f"{self.u} {self.weight}> {self.v}"

    def __str__(self) -> str:
        return f"{self.u} {self.weight}> {self.v}"


class Graph(Generic[V]):
    """
     A class representing an undirected graph.

     This class provides methods to manage vertices and edges, including adding vertices and edges,
     retrieving vertices and edges, and finding neighbors and connected components. It supports both
     unweighted and weighted edges, and includes functionality for breadth-first search to find connected
     components and groups.

     Vertices (or nodes) are the fundamental units of a graph. They represent entities or points in the graph.
     For example, in a social network graph, vertices could represent people.
     Edges are the connections between vertices. They represent the relationships or links between the entities.
     In a social network graph, edges could represent friendships or connections between people.

     Attributes:
         _vertices (list[V]): A list of vertices in the graph.
         _edges (list[list[Edge | WeightedEdge]]): A list of lists where each sublist contains the edges for a vertex.
     """

    def __init__(self, vertices: Optional[list[V]] = None) -> None:
        self._vertices: list[V] = [] if vertices is None else vertices
        self._edges: list[list[Edge | WeightedEdge]] = [[] for _ in self._vertices]
        self.search_results = set()

    @property
    def vertices(self) -> list[V]:
        return self._vertices

    @property
    def vertex_count(self) -> int:
        return len(self._vertices)  # Number of vertices

    @property
    def edge_count(self) -> int:
        return sum(map(len, self._edges))  # Number of edges

    # Add a vertex to the graph and return its index
    def add_vertex(self, vertex: V) -> int:
        self._vertices.append(vertex)
        self._edges.append([])  # add empty list for containing edges
        return self.vertex_count - 1  # return index of added vertex

    # This is an undirected graph,
    # so we always add edges in both directions
    def add_edge(self, edge: Edge | WeightedEdge) -> None:
        self._edges[edge.u].append(edge)
        self._edges[edge.v].append(edge.reversed())

    # Add an edge using vertex indices (convenience method)
    def add_edge_by_indices(self, u: int, v: int) -> None:
        edge: Edge = Edge(u, v)
        self.add_edge(edge)

    # Add an edge by looking up vertex indices (convenience method)
    def add_edge_by_vertices(self, first: V, second: V) -> None:
        u: int = self._vertices.index(first)
        v: int = self._vertices.index(second)
        self.add_edge_by_indices(u, v)

    def vertex_at(self, index: int) -> V:
        """Return the vertex at the given index"""
        return self._vertices[index]

    def at_vertex(self, vertex: V) -> V:
        """Return the vertex by name"""
        return self.vertex_at(self.index_of(vertex))

    def index_of(self, vertex: V) -> int:
        """Find the index of a vertex in the graph"""
        return self._vertices.index(vertex)

    def neighbors_for_index(self, index: int) -> list[V]:
        """Find the vertices that a vertex at some index is connected to"""
        return list(map(self.vertex_at, [e.v for e in self._edges[index]]))

    def neighbors_for_vertex(self, vertex: V) -> list[V]:
        """Lookup a vertex's index and find its neighbors (convenience method)"""
        return self.neighbors_for_index(self.index_of(vertex))

    def edges_for_index(self, index: int) -> list[Edge] | list[WeightedEdge]:
        """Return all the edges associated with a vertex at some index"""
        return self._edges[index]

    def edges_for_vertex(self, vertex: V) -> list[Edge] | list[WeightedEdge]:
        """Lookup the index of a vertex and return its edges (convenience method)"""
        return self.edges_for_index(self.index_of(vertex))

    def connected_components(self, initial: V) -> set[V]:
        """Breath first search
        This one is adjusted so that it does not have a 'goal' per se except
        for exploring all the connections to 'initial'.

        Effectively this bfs has been changed so that it will return the
        'connected_components' https://en.wikipedia.org/wiki/Component_(graph_theory)
        """
        frontier: Queue[Node[V]] = Queue()
        frontier.push(Node(initial, None))
        explored: set[V] = {initial}

        while not frontier.empty:
            current_node: Node[V] = frontier.pop()
            current_state: V = current_node.state
            for child in self.neighbors_for_vertex(current_state):
                if child in explored:
                    continue
                explored.add(child)
                frontier.push(Node(child, current_node))
        return explored

    def search(self, initial: V) -> list[V]:
        """Perform a depth-first search to find all connected components starting from a
        given node and keep track of the longest set found.

        Was needed for 2024 day 23.
        """
        longest_set = set()
        stack = [(initial, {initial})]
        while stack:
            current_node, current_req = stack.pop()
            key = tuple(sorted(current_req))
            if key in self.search_results:
                continue
            self.search_results.add(key)
            if len(current_req) > len(longest_set):
                longest_set = current_req
            for neighbor in self.neighbors_for_vertex(current_node):
                if neighbor in current_req:
                    continue
                if not set(current_req).issubset(self.neighbors_for_vertex(neighbor)):
                    continue
                stack.append((neighbor, {*current_req, neighbor}))

        return sorted(longest_set)

    def longest_connected_component(self) -> set[V]:
        longest_set = set()
        for vertice in self.vertices:
            l = self.search(vertice)
            if l and len(l) > len(longest_set):
                longest_set = l
        return longest_set


    def connected_groups(self):
        """Create groups of all separate connected_component groups"""
        todo = deepcopy(self._vertices)
        groups = []
        while todo:
            explored = self.connected_components(todo.pop())
            todo = [vertex for vertex in todo if vertex not in explored]
            groups.append(explored)
        return sorted(groups, key=lambda x: len(x), reverse=True)

    def number_connected_groups(self):
        return len(self.connected_groups())

    # Make it easy to pretty-print a Graph
    def __str__(self) -> str:
        desc: str = "\n"
        for i in range(self.vertex_count):
            desc += f"{self.vertex_at(i)} -> {self.neighbors_for_index(i)}\n"
        return desc


class WeightedGraph(Generic[V], Graph[V]):
    """
     See y2023/day_23 for a nice example of how to use this class.
    """

    def __init__(self, vertices: Optional[list[V]] = None) -> None:
        self._vertices: list[V] = [] if vertices is None else vertices
        self._edges: list[list[WeightedEdge]] = [[] for _ in self._vertices]

    def add_edge_by_indices(self, u: int, v: int, weight: float) -> None:
        edge: WeightedEdge = WeightedEdge(u, v, weight)
        self.add_edge(edge)  # call superclass version

    def add_edge_by_vertices(self, first: V, second: V, weight: float) -> None:
        u: int = self._vertices.index(first)
        v: int = self._vertices.index(second)
        self.add_edge_by_indices(u, v, weight)

    def neighbors_for_index_with_weights(self, index: int) -> list[tuple[V, float]]:
        distance_tuples: list[tuple[V, float]] = []
        for edge in self.edges_for_index(index):
            distance_tuples.append((self.vertex_at(edge.v), edge.weight))
        return list(set(distance_tuples))

    def neighbors_for_vertex_with_weights(self, vertex: V) -> list[tuple[V, float]]:
        return self.neighbors_for_index_with_weights(self.index_of(vertex))

    def __str__(self) -> str:
        desc: str = ""
        for i in range(self.vertex_count):
            desc += f"{self.vertex_at(i)} -> {self.neighbors_for_index_with_weights(i)}\n"
        return desc


WeightedPath = list[WeightedEdge]


def total_weight(wp: WeightedPath) -> float:
    return sum([e.weight for e in wp])


def mst(wg: WeightedGraph[V], start: int = 0) -> Optional[WeightedPath]:
    """
    This function implements Prim's algorithm to find the Minimum Spanning Tree (MST) of a weighted,
    undirected graph.
    A Minimum Spanning Tree of a graph is a subset of the edges of the graph that connects all the
    vertices together, without any cycles and with the minimum possible total edge weight.

    Parameters:
    wg (WeightedGraph): The weighted graph on which to find the MST.
    start (int, optional): The index of the starting vertex. Defaults to 0.

    Returns:
    Optional[WeightedPath]: The MST as a list of weighted edges. If the start vertex is not within the range of the
                            vertices in the graph, returns None.
    """
    if start > (wg.vertex_count - 1) or start < 0:
        return None
    result: WeightedPath = []  # holds the final MST
    pq: PriorityQueue[WeightedEdge] = PriorityQueue()
    visited: list[bool] = [False] * wg.vertex_count  # where we've been

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


def print_weighted_path(wg: WeightedGraph, wp: WeightedPath) -> None:
    for edge in wp:
        print(f"{wg.vertex_at(edge.u)} {edge.weight}> {wg.vertex_at(edge.v)}")
    print(f"Total Weight: {total_weight(wp)}")
