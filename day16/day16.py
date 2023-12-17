"""Day 16."""

from collections import defaultdict
from typing import Any, Iterator, TextIO

from utils.parse import read_lines

Point = tuple[int, int]


class Grid:
    def __init__(self, data: list[list[str]]) -> None:
        """Initialize a grid with an empty memo."""
        self.data = data
        self.width = len(data[0])
        self.height = len(data)
        self.size = (self.width, self.height)
        self.beam_memo = defaultdict[Point, set[Point]](set)

    def in_bounds(self, position: Point) -> bool:
        """Check if a position is in bounds."""
        return 0 <= position[0] < self.width and 0 <= position[1] < self.width

    @property
    def visited(self) -> int:
        """Get the number of positions visited by the beam."""
        return len(self.beam_memo)

    def reset(self) -> None:
        """Reset the visited positions."""
        self.beam_memo.clear()

    def follow_beam(self, start_position: Point, velocity: Point) -> None:
        """Follow a beam until it terminates or overlaps with a previous beam."""
        position = start_position
        while True:
            position = (
                position[0] + velocity[0],
                position[1] + velocity[1],
            )
            if not self.in_bounds(position):
                break
            if velocity in self.beam_memo[position]:
                break
            self.beam_memo[position].add(velocity)
            match (self.data[position[1]][position[0]], velocity):
                case "/", _:
                    velocity = (-velocity[1], -velocity[0])
                case "\\", _:
                    velocity = (velocity[1], velocity[0])
                case "-", (0, _):
                    self.follow_beam(position, (-1, 0))
                    self.follow_beam(position, (1, 0))
                    break
                case "|", (_, 0):
                    self.follow_beam(position, (0, -1))
                    self.follow_beam(position, (0, 1))
                    break


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 16."""
    grid = Grid(list(read_lines(file)))
    grid.follow_beam((-1, 0), (1, 0))
    yield grid.visited

    max_energized = 0
    for coord in [0, 1]:
        for direction in [-1, 1]:
            for entry in range(0, grid.size[coord]):
                start_position = [0, 0]
                start_position[coord] = -1 if direction == 1 else grid.size[1 - coord]
                start_position[1 - coord] = entry

                velocity = [0, 0]
                velocity[coord] = direction

                grid.reset()
                grid.follow_beam(tuple(start_position), tuple(velocity))
                max_energized = max(max_energized, grid.visited)
    yield max_energized
