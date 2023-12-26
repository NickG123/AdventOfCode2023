"""Day 25."""

import heapq
import random
from collections import Counter, defaultdict
from itertools import pairwise
from typing import Any, Iterator, TextIO

from utils.parse import read_lines


def order_tuple(s1: str, s2: str) -> tuple[str, str]:
    """Order a tuple."""
    if s1 <= s2:
        return (s1, s2)
    return (s2, s1)


def dijkstra(graph: dict[str, list[str]], source: str, dest: str) -> list[str]:
    """Find the shortest path between two nodes."""
    queue = [(0, source, [source])]
    heapq.heapify(queue)

    total_distances = {source: 0}

    while queue:
        distance, node, path = heapq.heappop(queue)

        for new_node in graph[node]:
            if new_node == dest:
                return path + [new_node]

            new_distance = distance + 1
            if (
                new_node not in total_distances
                or new_distance < total_distances[new_node]
            ):
                total_distances[new_node] = new_distance
                heapq.heappush(queue, (new_distance, new_node, path + [new_node]))

    raise ValueError("No path found")


def explore_graph(
    graph: dict[str, list[str]], source: str, removed_edges: set[tuple[str, str]]
) -> set[str]:
    """Compute the size of a graph

    Start from a provided node and skip any edges in the removed_edges set.
    """
    nodes = [source]
    visited = set()
    for node in nodes:
        visited.add(node)
        nodes.extend(
            n
            for n in graph[node]
            if n not in visited and order_tuple(node, n) not in removed_edges
        )
    return visited


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 25."""
    graph = defaultdict[str, list[str]](list)
    for line in read_lines(file):
        source, destinations = line.split(": ")
        dests = destinations.split(" ")
        for dest in dests:
            graph[source].append(dest)
            graph[dest].append(source)
    nodes = list(graph.keys())

    # Randomly choose two points and run a BFS between them
    # Keep track of how many time each edge shows up in the BFS
    edge_counts = Counter[tuple[str, str]]()
    while True:
        for _ in range(100):
            source = random.choice(nodes)
            dest = random.choice(nodes)
            path = dijkstra(graph, source, dest)
            for p1, p2 in pairwise(path):
                edge_counts[order_tuple(p1, p2)] += 1
        removed_edges = {edge for edge, _ in edge_counts.most_common(3)}

        new_graph = explore_graph(graph, nodes[0], removed_edges)
        if len(new_graph) != len(nodes):
            break

    yield len(new_graph) * (len(nodes) - len(new_graph))
