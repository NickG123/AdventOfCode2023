"""Day 23."""

from collections import defaultdict, deque
from typing import Any, Iterator, TextIO

from utils.parse import read_lines

Point = tuple[int, int]

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
SLOPES = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}


class Grid:
    def __init__(self, data: list[list[str]], slippery: bool) -> None:
        """Initialize from data."""
        self.data = data
        self.height = len(data)
        self.width = len(data[0])
        self.slippery = slippery

    def in_bounds(self, point: Point) -> bool:
        """Determine if a point is in bounds."""
        return 0 <= point[0] < self.width and 0 <= point[1] < self.height

    def get_value(self, point: Point) -> str:
        """Get the value at a point."""
        x, y = point
        return self.data[y][x]

    def neighbours(self, point: Point) -> Iterator[tuple[Point, Point]]:
        """Find the neighbours of a point."""
        current_val = self.get_value(point)
        if current_val in SLOPES and self.slippery:
            d = SLOPES[current_val]
            yield (point[0] + d[0], point[1] + d[1]), d
            return

        for d in DIRECTIONS:
            new_point = (point[0] + d[0], point[1] + d[1])
            if self.in_bounds(new_point):
                val = self.get_value(new_point)
                if (
                    val == "."
                    or SLOPES.get(val) == d
                    or (val in SLOPES and not self.slippery)
                ):
                    yield new_point, d

    def build_graph(
        self, start: Point, end: Point
    ) -> dict[Point, list[tuple[Point, int]]]:
        """Build a graph between each intersection in the maze."""
        graph = defaultdict(list)
        to_process = deque([start])
        visited = set()

        while to_process:
            node = to_process.pop()
            if node in visited:
                continue
            visited.add(node)
            for n, d in self.neighbours(node):
                result = self.find_node(node, d, end)
                if result is not None:
                    next_node, n_visited = result
                    to_process.append(next_node)
                    graph[node].append((next_node, len(n_visited) - 1))

        return graph

    def find_node(
        self, start: Point, direction: Point, end: Point
    ) -> tuple[Point, set[Point]] | None:
        """Find the next node in a path."""
        next_node = (start[0] + direction[0], start[1] + direction[1])
        visited = {start, next_node}
        while True:
            if next_node == end:
                return (next_node, visited)
            neighbours = [n for n, _ in self.neighbours(next_node) if n not in visited]
            match neighbours:
                case []:
                    return None
                case [neighbour]:
                    next_node = neighbour
                    visited.add(next_node)
                case _:
                    return (next_node, visited)


def graph_longest_path(
    graph: dict[Point, list[tuple[Point, int]]], start: Point, end: Point
) -> int:
    """Run BFS on the graph to find the longest path."""
    queue = deque[tuple[Point, set[Point], int]]([(start, set(), 0)])
    longest_path = 0

    while queue:
        p, visited, distance_travelled = queue.popleft()
        if p == end:
            longest_path = max(distance_travelled, longest_path)
        new_visited = visited | {p}
        for n, distance in graph[p]:
            if n not in visited:
                queue.append((n, new_visited, distance_travelled + distance))

    return longest_path


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 23."""
    data = [list(line) for line in read_lines(file)]
    p1_grid = Grid(data, True)
    p2_grid = Grid(data, False)

    start = (1, 0)
    end = (p1_grid.width - 2, p1_grid.height - 1)

    yield graph_longest_path(p1_grid.build_graph(start, end), start, end)
    yield graph_longest_path(p2_grid.build_graph(start, end), start, end)
