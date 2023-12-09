"""Day 08."""

from itertools import cycle
from math import lcm
from typing import Any, Iterator, TextIO

from utils.parse import read_lines


def take_step(paths: dict[str, tuple[str, str]], position: str, direction: str) -> str:
    """Take one step."""
    path = paths[position]
    return path[0] if direction == "L" else path[1]


def navigate(paths: dict[str, tuple[str, str]], route: str) -> int:
    """Navigate a path and count steps."""
    position = "AAA"
    route_cycle = cycle(route)
    steps = 0
    while position != "ZZZ":
        position = take_step(paths, position, next(route_cycle))
        steps += 1
    return steps


def find_cycle(start: str, paths: dict[str, tuple[str, str]], route: str) -> int:
    """Find the cycles through the data.

    It seems the data is very nicely crafted such that each A leads to exactly one Z,
    and after reaching that Z it loops back upon itself, and the cycle length is a
    multiple of the route length.  The initial offset of the Z and the cycle appear
    to be the same length, so we can just take the LCM of the length of these cycles.
    """
    position = start
    route_cycle = cycle(route)
    cycle_start = 0
    while not position.endswith("Z"):
        position = take_step(paths, position, next(route_cycle))
        cycle_start += 1
    cycle_position = position
    cycle_length = 0
    while True:
        position = take_step(paths, position, next(route_cycle))
        cycle_length += 1
        if position.endswith("Z"):
            if position != cycle_position:
                raise Exception("Multiple end states in one path")
            break
    if cycle_length != cycle_start:
        raise Exception("Initial offset and cycle length didn't match")
    if cycle_length % len(route) != 0:
        raise Exception("Cycle length not evenly divisible by route length")
    return cycle_length


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 08."""
    lines = read_lines(file)
    pattern = next(lines)
    next(lines)

    paths: dict[str, tuple[str, str]] = {}
    for path_line in lines:
        start, dest_str = path_line.split(" = ")
        dests = dest_str.strip("()").split(", ")
        paths[start] = (dests[0], dests[1])

    yield navigate(paths, pattern)
    yield lcm(
        *[find_cycle(node, paths, pattern) for node in paths if node.endswith("A")]
    )
