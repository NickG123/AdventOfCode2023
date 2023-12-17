"""Day 14."""

from collections import defaultdict
from enum import Enum
from typing import Any, Iterator, TextIO

from utils.parse import read_lines


class Rock(Enum):
    ROUND = "O"
    CUBE = "#"
    EMPTY = "."


def parse_rocks(platform: Iterator[str]) -> list[list[Rock]]:
    """Parse the rocks on the platform."""
    return [[Rock(char) for char in row] for row in platform]


def move_rocks(rocks: list[list[Rock]]) -> None:
    """Move rocks to the top of the platform (mutating the input array)."""
    next_roll_point = defaultdict(int)
    for row, line in enumerate(rocks):
        for col, rock in enumerate(line):
            if rock == Rock.CUBE:
                next_roll_point[col] = row + 1
            elif rock == Rock.ROUND:
                if next_roll_point[col] != row:
                    rocks[next_roll_point[col]][col] = Rock.ROUND
                    rocks[row][col] = Rock.EMPTY
                next_roll_point[col] += 1


def rotate_platform(rocks: list[list[Rock]]) -> list[list[Rock]]:
    """Rotate the platform 90 degrees."""
    return [
        [rocks[len(rocks) - j - 1][i] for j in range(len(rocks))]
        for i in range(len(rocks[0]))
    ]


def run_cycle(rocks: list[list[Rock]]) -> list[list[Rock]]:
    """Run a cycle of rotating the platform all the way around."""
    for _ in range(4):
        move_rocks(rocks)
        rocks = rotate_platform(rocks)
    return rocks


def compute_load(rocks: list[list[Rock]]) -> int:
    """Compute the load of the rocks."""
    load = 0
    for row_num, row in enumerate(rocks):
        for rock in row:
            if rock == Rock.ROUND:
                load += len(rocks) - row_num
    return load


def run_cycles(rocks: list[list[Rock]], cycles: int) -> list[list[Rock]]:
    """Run a specified number of cycles using cycle detection."""
    state: dict[tuple[tuple[int, int], ...], int] = {}
    for cycle_num in range(cycles):
        rocks = run_cycle(rocks)

        state_val = tuple(
            (x, y)
            for y, row in enumerate(rocks)
            for x, rock in enumerate(row)
            if rock == Rock.ROUND
        )
        if state_val in state:
            cycle_size = cycle_num - state[state_val]
            break
        else:
            state[state_val] = cycle_num
    remaining_cycles = (cycles - cycle_num - 1) % cycle_size
    for _ in range(remaining_cycles):
        rocks = run_cycle(rocks)

    return rocks


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 14."""
    rocks = parse_rocks(read_lines(file))
    move_rocks(rocks)
    yield compute_load(rocks)
    rocks = run_cycles(rocks, 1000000000)
    yield compute_load(rocks)
