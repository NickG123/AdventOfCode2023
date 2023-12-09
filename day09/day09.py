"""Day 09."""

from itertools import pairwise
from typing import Any, Iterator, TextIO

from utils.parse import read_lines


def extrapolate(line: list[int]) -> tuple[int, int]:
    """Recursively extrapolate the next and previous value.

    Feels like there's probably some magic explicit formula, but I don't know it.
    """
    new_line = [b - a for a, b in pairwise(line)]
    if all(x == 0 for x in new_line):
        return (line[0], line[-1])
    else:
        left, right = extrapolate(new_line)
        return line[0] - left, right + line[-1]


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 09."""
    lines = list(read_lines(file))
    data = [[int(x) for x in line.split(" ")] for line in lines]
    results = [extrapolate(x) for x in data]
    yield sum(val for _, val in results)
    yield sum(val for val, _ in results)
