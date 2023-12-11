"""Day 11."""

from itertools import combinations
from typing import Any, Iterator, TextIO

from utils.parse import read_lines

Point = tuple[int, int]


def expand(galaxies: set[Point], coord: int, expansion_factor: int = 2) -> set[Point]:
    """Expand the galaxies vertically or horizontally."""
    current_offset = 0
    current_coord = 0

    new_galaxies = set[Point]()
    for galaxy in sorted(galaxies, key=lambda galaxy: galaxy[coord]):
        new_coord = galaxy[coord]
        if new_coord - current_coord > 1:
            current_offset += (new_coord - current_coord - 1) * (expansion_factor - 1)

        mutable = list(galaxy)
        mutable[coord] += current_offset
        new_galaxies.add((mutable[0], mutable[1]))

        current_coord = new_coord

    return new_galaxies


def manhattan_distance(p1: Point, p2: Point) -> int:
    """Return the manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 11."""
    galaxies = set()

    for y, line in enumerate(read_lines(file)):
        for x, char in enumerate(line):
            if char == "#":
                galaxies.add((x, y))

    expanded = expand(expand(galaxies, 0), 1)
    expanded_2 = expand(expand(galaxies, 0, 1_000_000), 1, 1_000_000)

    yield sum(manhattan_distance(p1, p2) for p1, p2 in combinations(expanded, 2))
    yield sum(manhattan_distance(p1, p2) for p1, p2 in combinations(expanded_2, 2))
