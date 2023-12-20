"""Day 18."""

from itertools import pairwise
from typing import Any, Iterator, TextIO

from utils.parse import read_lines

Point = tuple[int, int]

DIRECTIONS = {
    "U": (0, -1),
    "D": (0, 1),
    "R": (1, 0),
    "L": (-1, 0),
}
DIRECTIONS_P2 = {
    "0": (1, 0),
    "1": (0, 1),
    "2": (-1, 0),
    "3": (0, -1),
}


def shoelace(corners: list[Point]) -> int:
    """Use shoelace to calculate area."""
    total = 0
    for (p1x, p1y), (p2x, p2y) in pairwise(corners):
        total += (p1x * p2y) - (p2x * p1y)
    return total // 2


def reverse_picks(area: int, boundary_points: int) -> int:
    """Had to look up lots of theorems today.

    Get the number of interior points based on the area and number of boundary points.
    """
    return (area + 1) - (boundary_points // 2)


def dig(paths: list[tuple[Point, int]]) -> int:
    position = (0, 0)
    border_points = 0
    corners = []
    for direction, distance in paths:
        corners.append(position)
        border_points += distance
        position = (
            position[0] + direction[0] * distance,
            position[1] + direction[1] * distance,
        )
    corners.append(position)
    area = shoelace(corners)
    interior_points = reverse_picks(area, border_points)
    return interior_points + border_points


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 18."""
    data = [line.split(" ") for line in read_lines(file)]

    yield dig(
        [(DIRECTIONS[direction], int(distance)) for direction, distance, _ in data]
    )
    yield dig(
        [(DIRECTIONS_P2[colors[-2]], int(colors[2:-2], 16)) for _, _, colors in data]
    )
