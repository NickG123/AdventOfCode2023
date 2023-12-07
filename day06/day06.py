"""Day 06."""

import operator
from functools import reduce
from math import ceil, floor, sqrt
from typing import Any, Iterator, TextIO

from utils.parse import read_lines


# if d is distance, t is total time, and x is time held down, then
# d = (t - x)x
# d = tx - x^2
# x^2 - tx + d = 0
# x = (t +/- sqrt(t^2 - 4d))/2
def winning_range(time: int, distance: int) -> tuple[int, int]:
    """Find the (inclusive) range for which the record is broken."""
    offset = sqrt(time**2 - 4 * distance)
    lower_root = (time - offset) / 2
    upper_root = (time + offset) / 2

    # We want integers where the formula is greater than 0, so if the roots
    # are integers we need to adjust them
    # This wouldn't work for big enough ranges but it's good enough for this.
    if lower_root.is_integer():
        lower_root += 1
    if upper_root.is_integer():
        upper_root -= 1

    return (ceil(lower_root), floor(upper_root))


def parse_int_list(line: str) -> list[int]:
    """Parse a list of whitespace separated ints."""
    return [int(x) for x in line.split(" ") if x]


def parse_int_list_p2(line: str) -> int:
    """Parse an int ignoring whitespace."""
    return int(line.replace(" ", ""))


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 06."""
    lines = read_lines(file)
    time_line = next(lines).split(":")[-1]
    distance_line = next(lines).split(":")[-1]

    times = parse_int_list(time_line)
    distances = parse_int_list(distance_line)

    winning_ranges = [
        winning_range(time, distance) for time, distance in zip(times, distances)
    ]
    yield reduce(operator.mul, (upper - lower + 1 for (lower, upper) in winning_ranges))

    winning_range_p2 = winning_range(
        parse_int_list_p2(time_line), parse_int_list_p2(distance_line)
    )
    yield winning_range_p2[1] - winning_range_p2[0] + 1
