"""Day 15."""

from collections import defaultdict
from typing import Any, Iterator, TextIO


def compute_hash(s: str) -> int:
    """Compute the hash of a string."""
    val = 0
    for char in s:
        val += ord(char)
        val = (val * 17) % 256
    return val


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 15."""
    sequence = file.read().strip()
    total_p1 = 0
    boxes = defaultdict[int, dict[str, int]](dict)
    for operation in sequence.split(","):
        total_p1 += compute_hash(operation)

        if operation.endswith("-"):
            label = operation[:-1]
            box = compute_hash(label)
            boxes[box].pop(label, None)
        else:
            value = int(operation[-1])
            label = operation[:-2]
            box = compute_hash(label)
            boxes[box][label] = value

    yield total_p1

    total_p2 = 0
    for box, lenses in boxes.items():
        for i, value in enumerate(lenses.values()):
            total_p2 += (box + 1) * (i + 1) * value
    yield total_p2
