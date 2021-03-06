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

from ivonet.collection import Queue
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

    def __str__(self) -> str:
        return f"{self.u} {self.weight}> {self.v}"


class Graph(Generic[V]):
    def __init__(self, vertices: Optional[list[V]] = None) -> None:
        self._vertices: list[V] = [] if vertices is None else vertices
        self._edges: list[list[Edge]] = [[] for _ in self._vertices]

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
    def add_edge(self, edge: Edge) -> None:
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

    # Find the vertex at a specific index
    def vertex_at(self, index: int) -> V:
        return self._vertices[index]

    # Find the index of a vertex in the graph
    def index_of(self, vertex: V) -> int:
        return self._vertices.index(vertex)

    # Find the vertices that a vertex at some index is connected to
    def neighbors_for_index(self, index: int) -> list[V]:
        return list(map(self.vertex_at, [e.v for e in self._edges[index]]))

    # Lookup a vertice's index and find its neighbors (convenience method)
    def neighbors_for_vertex(self, vertex: V) -> list[V]:
        return self.neighbors_for_index(self.index_of(vertex))

    # Return all of the edges associated with a vertex at some index
    def edges_for_index(self, index: int) -> list[Edge]:
        return self._edges[index]

    # Lookup the index of a vertex and return its edges (convenience method)
    def edges_for_vertex(self, vertex: V) -> list[Edge]:
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
        desc: str = ""
        for i in range(self.vertex_count):
            desc += f"{self.vertex_at(i)} -> {self.neighbors_for_index(i)}\n"
        return desc


class WeightedGraph(Generic[V], Graph[V]):
    def __init__(self, vertices: Optional[list[V]] = None) -> None:
        self._vertices: list[V] = [] if vertices is None else vertices
        self._edges: list[list[WeightedEdge]] = [[] for _ in vertices]

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
        return distance_tuples

    def __str__(self) -> str:
        desc: str = ""
        for i in range(self.vertex_count):
            desc += f"{self.vertex_at(i)} -> {self.neighbors_for_index_with_weights(i)}\n"
        return desc
