"""Day 03."""

from itertools import islice, takewhile
from typing import Any, Iterator, TextIO

from utils.parse import read_lines


class EnginePart:
    """A class representing an engine part."""

    def __init__(self, number: str, start_position: tuple[int, int]) -> None:
        """Initialize with a number and position."""
        self.length = len(number)
        self.value = int(number)
        self.col, self.row = start_position

    def is_touching_symbol(self, symbols: dict[tuple[int, int], str]) -> bool:
        """Check if the part is touching a symbol."""
        for x_offset in range(-1, self.length + 1):
            for y_offset in range(-1, 2):
                if (self.col + y_offset, self.row + x_offset) in symbols:
                    return True
        return False


def read_number(s: Iterator[str]) -> str:
    """Read a number from an index in a string."""
    return "".join(takewhile(lambda c: c.isdigit(), s))


def find_adjacent_parts(
    location: tuple[int, int], part_locations: dict[tuple[int, int], EnginePart]
) -> list[EnginePart]:
    """Get a list of numbers adjacent to a space."""
    col, row = location
    adjacent_parts = set()
    for x_offset in range(-1, 2):
        for y_offset in range(-1, 2):
            part = part_locations.get((col + y_offset, row + x_offset))
            if part is not None:
                adjacent_parts.add(part)

    return list(adjacent_parts)


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 03."""
    part_locations = {}
    parts = []
    symbols = {}
    for col, line in enumerate(read_lines(file)):
        i = 0
        while i < len(line):
            if line[i].isdigit():
                num = read_number(islice(line, i, None))
                part = EnginePart(num, (col, i))
                parts.append(part)
                for x_offset in range(part.length):
                    part_locations[(col, i + x_offset)] = part
                i += len(num) - 1
            elif line[i] != ".":
                symbols[(col, i)] = line[i]
            i += 1

    part_1_total = 0
    for part in parts:
        if part.is_touching_symbol(symbols):
            part_1_total += part.value
    yield part_1_total

    part_2_total = 0
    for location, symbol in symbols.items():
        if symbol == "*":
            adjacent_numbers = find_adjacent_parts(location, part_locations)
            if len(adjacent_numbers) == 2:
                part_2_total += adjacent_numbers[0].value * adjacent_numbers[1].value
    yield part_2_total
