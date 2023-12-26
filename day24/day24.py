"""Day 24."""

from dataclasses import dataclass
from itertools import combinations
from typing import Any, Iterator, TextIO

from sympy import Symbol, solve_poly_system, symbols

from utils.parse import read_lines

Point = tuple[int, int, int]


@dataclass
class Hailstone:
    """A class to represent a hailstone."""

    position: Point
    velocity: Point


# Finding 2d intersection...
# x1 + (dx1 * a) == x2 + (dx2 * b) -> a = (x2 + (dx2 * b) - x1) / dx1
# y1 + (dy1 * a) == y2 + (dy2 * b) -> a = (y2 + (dy2 * b) - y1) / dy1
#
# (x2 + (dx2 * b) - x1) / dx1 = (y2 + (dy2 * b) - y1) / dy1
# (dy1 * x2 / dx1) + (dx2 * b / dx1 * dy1) - (dy1 * x1 / dx1) = y2 + (dy2 * b) - y1
# (dy1 * x2 / dx1) - (dy1 * x1 / dx1) - y2 + y1 = (dy2 * b) - (dx2 * b / dx1 * dy1)
# b = ((dy1 * x2 / dx1) - (dy1 * x1 / dx1) - y2 + y1) / (dy2 - dx2 / dx1 * dy1)


def find_intersection(h1: Hailstone, h2: Hailstone) -> tuple[float, float] | None:
    """Find the point at which the two hailstones intersect."""
    x1, y1, _ = h1.position
    dx1, dy1, _ = h1.velocity
    x2, y2, _ = h2.position
    dx2, dy2, _ = h2.velocity

    denominator = dy2 - dx2 / dx1 * dy1
    if denominator == 0:
        # Hailstones never intersect
        return None
    b = ((dy1 * x2 / dx1) - (dy1 * x1 / dx1) - y2 + y1) / denominator
    if b < 0:
        # Hailstones intersected in the past for h2
        return None
    a = ((y2 + (dy2 * b) - y1) / dy1) if dy1 != 0 else ((x2 + (dx2 * b) - x1) / dx1)
    if a < 0:
        # Hailstones intersected in the past for h1
        return None
    return (x2 + dx2 * b, y2 + dy2 * b)


def solve_equations(hailstones: list[Hailstone]) -> tuple[int, int, int]:
    """Spent way too long trying to math this, and now I give up.

    We'll just use sympy.
    """
    position = symbols(["x", "y", "z"])
    velocity = symbols(["dx", "dy", "dz"])

    equations = []
    all_symbols = position + velocity

    for i, hailstone in enumerate(hailstones):
        t = Symbol(f"hailstone_{i}_t")

        coord_equal = [
            (velocity[c] * t + position[c])
            - (hailstone.velocity[c] * t + hailstone.position[c])
            for c in range(3)
        ]
        equations.extend(coord_equal)
        all_symbols.append(t)

    [result] = solve_poly_system(equations, *all_symbols)
    return tuple(result[:3])


def parse_position(s: str) -> Point:
    """Parse a position from the point."""
    x, y, z = s.split(", ")
    return (int(x), int(y), int(z))


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 24."""
    bounds = (200000000000000, 400000000000000)
    hailstones = []
    for line in read_lines(file):
        position_str, velocity_str = line.split(" @ ")
        position = parse_position(position_str)
        velocity = parse_position(velocity_str)
        hailstones.append(Hailstone(position, velocity))

    p1_total = 0
    for h1, h2 in combinations(hailstones, 2):
        result = find_intersection(h1, h2)
        if result is None:
            continue
        x, y = result
        if bounds[0] <= x <= bounds[1] and bounds[0] <= y <= bounds[1]:
            p1_total += 1

    yield p1_total
    # We shouldn't actually need any more than 3 unique hailstones
    yield sum(solve_equations(hailstones[:5]))
