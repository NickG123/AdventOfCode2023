"""Day 17."""

import heapq
from collections import defaultdict
from typing import Any, Iterator, TextIO

from utils.parse import read_lines

Point = tuple[int, int]

TURN_RIGHT = {
    (0, 1): (-1, 0),
    (-1, 0): (0, -1),
    (0, -1): (1, 0),
    (1, 0): (0, 1),
}
TURN_LEFT = {
    (0, 1): (1, 0),
    (-1, 0): (0, 1),
    (0, -1): (-1, 0),
    (1, 0): (0, -1),
}


class Dijkstra:
    def __init__(self, grid: list[list[int]], min_spaces: int, max_spaces: int) -> None:
        self.grid = grid
        self.width = len(grid[0])
        self.height = len(grid)
        self.min_spaces = min_spaces
        self.max_spaces = max_spaces

    def in_bounds(self, point: Point) -> bool:
        """Check if a point is in the bounds."""
        return 0 <= point[0] < self.width and 0 <= point[1] < self.height

    def neighbours(
        self, position: Point, velocity: Point, distance: int
    ) -> list[tuple[Point, Point, int]]:
        """Find the neighbours of a given point, direction and distance travelled."""
        result = []
        left_velocity = TURN_LEFT[velocity]
        if distance >= self.min_spaces - 1:
            left_new_position = (
                position[0] + left_velocity[0],
                position[1] + left_velocity[1],
            )
            result.append((left_new_position, left_velocity, 0))
            right_velocity = TURN_RIGHT[velocity]
            right_new_position = (
                position[0] + right_velocity[0],
                position[1] + right_velocity[1],
            )
            result.append((right_new_position, right_velocity, 0))
        if distance < self.max_spaces - 1:
            straight_new_position = (
                position[0] + velocity[0],
                position[1] + velocity[1],
            )
            result.append((straight_new_position, velocity, distance + 1))
        return [(p, v, d) for p, v, d in result if self.in_bounds(p)]

    def get_heat(self, point: Point) -> int:
        """Get the heat at a point."""
        return self.grid[point[1]][point[0]]

    def dijkstra(self, starting_positions: list[tuple[Point, Point]]) -> int:
        """Find the minimum heat that can be carried to the end."""
        destination = (self.width - 1, self.height - 1)

        queue = [(self.get_heat(pos), pos, dir, 0) for pos, dir in starting_positions]
        heapq.heapify(queue)

        total_heats = defaultdict[Point, dict[tuple[Point, int], int]](dict)
        for pos, dir in starting_positions:
            total_heats[pos][(dir, 0)] = self.get_heat(pos)

        while queue:
            heat, position, direction, distance = heapq.heappop(queue)

            for new_position, new_direction, new_distance in self.neighbours(
                position, direction, distance
            ):
                new_heat = heat + self.get_heat(new_position)
                neighbour_total_heats = total_heats[new_position]
                if (
                    new_direction,
                    new_distance,
                ) not in neighbour_total_heats or neighbour_total_heats[
                    (new_direction, new_distance)
                ] > new_heat:
                    neighbour_total_heats[(new_direction, new_distance)] = new_heat
                    heapq.heappush(
                        queue, (new_heat, new_position, new_direction, new_distance)
                    )

        return min(
            heat
            for (_, distance), heat in total_heats[destination].items()
            if distance >= self.min_spaces - 1
        )


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 17."""
    heats = [[int(x) for x in line] for line in read_lines(file)]
    p1_grid = Dijkstra(heats, 0, 3)
    p2_grid = Dijkstra(heats, 4, 10)
    start_points = [
        ((0, 1), (0, 1)),
        ((1, 0), (1, 0)),
    ]
    yield p1_grid.dijkstra(start_points)
    yield p2_grid.dijkstra(start_points)
