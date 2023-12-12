"""Day 12."""

from functools import cache
from typing import Any, Iterator, TextIO

from utils.parse import read_lines


def can_fit(s: tuple[str], count: int) -> bool:
    """Check if a count can fit at the start of the string."""
    for offset in range(count):
        if offset >= len(s) or s[offset] == ".":
            return False
    if count < len(s) and s[count] == "#":
        return False
    return True


@cache
def possible_arrangements(s: tuple[str], counts: tuple[int]) -> int:
    """Find the possible arrangements of springs."""
    if not counts:
        if all(c != "#" for c in s):
            return 1
        else:
            return 0
    if not s:
        return 0

    next_count = counts[0]
    match s[0]:
        case "#":
            if not can_fit(s, next_count):
                return 0
            return possible_arrangements(s[next_count + 1 :], counts[1:])
        case "?":
            total = 0
            if can_fit(s, next_count):
                total += possible_arrangements(s[next_count + 1 :], counts[1:])
            total += possible_arrangements(s[1:], counts)
            return total
        case ".":
            return possible_arrangements(s[1:], counts)
        case _:
            raise Exception(f"Unexpected character {s[0]}")


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 12."""
    total = 0
    p2_total = 0
    for line in read_lines(file):
        springs, count_list = line.split(" ")
        counts = tuple([int(x) for x in count_list.split(",")])
        total += possible_arrangements(tuple(springs), counts)

        p2_springs = "?".join(springs for _ in range(5))
        p2_counts = counts * 5
        p2_total += possible_arrangements(tuple(p2_springs), p2_counts)

    yield total
    yield p2_total
