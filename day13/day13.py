"""Day 13."""
from __future__ import annotations

from itertools import takewhile
from typing import Any, Iterator, TextIO

from utils.parse import read_lines


def find_mirror_in_data(
    data: list[list[str]], num_differences_required: int
) -> int | None:
    """Find where the mirror is in a grid."""
    for row_num in range(0, len(data) - 1):
        upper_range = range(row_num, -1, -1)
        lower_range = range(row_num + 1, len(data))
        total_differences = 0
        for left, right in zip(upper_range, lower_range):
            differences = sum(
                left_char != right_char
                for left_char, right_char in zip(data[left], data[right])
            )
            total_differences += differences
            if total_differences > num_differences_required:
                break
        else:
            if total_differences == num_differences_required:
                return row_num + 1

    return None


def read_grid(line_iter: Iterator[str]) -> list[list[str]] | None:
    """Parse the grid from an iterator of lines."""
    return [list(line) for line in takewhile(bool, line_iter)]


def find_mirror(data: list[list[str]], num_differences_required: int) -> int:
    """Find where the mirror is."""
    row_result = find_mirror_in_data(data, num_differences_required)
    if row_result is not None:
        return row_result * 100
    transpose = [[row[i] for row in data] for i in range(len(data[0]))]
    col_result = find_mirror_in_data(transpose, num_differences_required)
    if col_result is not None:
        return col_result
    raise RuntimeError("No mirror found")


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 13."""
    lines = read_lines(file)
    p1_total = 0
    p2_total = 0
    while True:
        grid = read_grid(lines)
        if not grid:
            break
        p1_total += find_mirror(grid, 0)
        p2_total += find_mirror(grid, 1)
    yield p1_total
    yield p2_total
