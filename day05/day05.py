"""Day 05."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterator, TextIO

from utils.iterables import grouper
from utils.parse import read_lines


@dataclass
class Range:
    """A range."""

    lower: int
    upper: int

    @property
    def empty(self) -> bool:
        return self.upper <= self.lower

    def get_overlap(self, other: Range) -> Range | None:
        """Get the overlapping portion of two ranges."""
        lower = max(self.lower, other.lower)
        upper = min(self.upper, other.upper)
        if lower < upper:
            return Range(lower, upper)
        return None

    def remove_range(self, other: Range) -> list[Range]:
        """Get the leftover portion of a range when a part is removed."""
        lower = Range(self.lower, other.lower)
        upper = Range(other.upper, self.upper)
        return [r for r in [lower, upper] if not r.empty]


@dataclass
class MappingRange(Range):
    """A mapping from the range of one category to another."""

    offset: int


@dataclass
class Mapping:
    """A class that maps one category to another."""

    source_category: str
    dest_category: str
    special_ranges: list[MappingRange]

    def map(self, value: int) -> int:
        """Map a value from the input category to the destination category."""
        for special_range in self.special_ranges:
            if special_range.lower <= value <= special_range.upper:
                return value + special_range.offset
        return value

    def map_range(self, starting_range: Range) -> list[Range]:
        """Map a range from the input category to the destination category."""
        result = []
        input_ranges = [starting_range]
        while input_ranges:
            input_range = input_ranges.pop()
            for special_range in self.special_ranges:
                overlap = input_range.get_overlap(special_range)
                if overlap:
                    result.append(
                        Range(
                            overlap.lower + special_range.offset,
                            overlap.upper + special_range.offset,
                        )
                    )
                    input_ranges.extend(input_range.remove_range(overlap))
                    break
            else:
                result.append(input_range)
        return result


def parse_mappings(lines: Iterator[str]) -> dict[str, Mapping]:
    """Parse the mappings."""
    result = {}
    for title in lines:
        map_name = title.split(" ")[0]
        source_category, _, dest_category = map_name.split("-")
        special_ranges = []
        for mapping_line in lines:
            if not mapping_line:
                break
            dest_range_start, source_range_start, range_length = [
                int(x) for x in mapping_line.split(" ")
            ]
            mapping_range = MappingRange(
                source_range_start,
                source_range_start + range_length,
                dest_range_start - source_range_start,
            )
            special_ranges.append(mapping_range)
        result[source_category] = Mapping(
            source_category, dest_category, special_ranges
        )
    return result


def map_seed(mappings: dict[str, Mapping], seed: int, target: str) -> int:
    """Map a seed to a target category."""
    category = "seed"
    value = seed
    while category != target:
        mapping = mappings[category]
        value = mapping.map(value)
        category = mapping.dest_category
    return value


def map_seed_range(
    mappings: dict[str, Mapping], input_range: Range, target: str
) -> list[Range]:
    """Map a range of seeds to a target category."""
    category = "seed"
    current_ranges = [input_range]
    while category != target:
        mapping = mappings[category]
        new_ranges = []

        for current_range in current_ranges:
            for new_range in mapping.map_range(current_range):
                new_ranges.append(new_range)

        current_ranges = new_ranges
        category = mapping.dest_category
    return current_ranges


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 05."""
    lines = read_lines(file)
    seed_line = next(lines)
    next(lines)

    seeds = [int(x) for x in seed_line.split(": ")[-1].split(" ")]
    mappings = parse_mappings(lines)

    locations = [map_seed(mappings, seed, "location") for seed in seeds]
    yield min(locations)

    seed_ranges = [Range(lower, lower + length) for lower, length in grouper(seeds, 2)]
    location_ranges = [
        output_range
        for input_range in seed_ranges
        for output_range in map_seed_range(mappings, input_range, "location")
    ]

    yield min(r.lower for r in location_ranges)
