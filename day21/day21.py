"""Day 21."""

from typing import Any, Iterator, TextIO

from utils.parse import read_lines

Point = tuple[int, int]

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


class Grid:
    """A class representing the grid."""

    def __init__(self, data: list[list[str]], wrap: bool) -> None:
        """Initialize from data."""
        self.height = len(data)
        self.width = len(data[0])
        self.data = data
        self.wrap = wrap

    def in_bounds(self, point: Point) -> bool:
        """Determine if a point is in bounds."""
        if self.wrap:
            return True
        return 0 <= point[0] < self.width and 0 <= point[1] < self.height

    def neighbours(self, point: Point) -> list[Point]:
        """Find neighbours of a point."""
        result = [(point[0] + dir[0], point[1] + dir[1]) for dir in DIRECTIONS]
        return [p for p in result if self.in_bounds(p) and self.get_data(p) == "."]

    def get_data(self, point: Point) -> str:
        x, y = point
        if self.wrap:
            x %= self.width
            y %= self.height
        return self.data[y][x]

    def bfs(self, start_positions: set[Point], steps: int) -> set[Point]:
        """Breadth first search for a certain number of steps."""
        positions = start_positions
        for _ in range(steps):
            new_positions = set()
            for position in positions:
                for n in self.neighbours(position):
                    new_positions.add(n)
            positions = new_positions
        return positions


def newton_polynomial(y1: int, y2: int, y3: int, n: int) -> int:
    """What a terrible problem.

    Reddit tells me this can be predicted using a newton polynomial
    (Except only the actual version, not the sample problem)
    """
    d1 = y1
    d2 = y2 - y1
    d3 = y3 - y2
    return ((n * (n - 1) // 2) * (d3 - d2)) + (d2 * n) + d1


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 21."""
    data = []
    for y, line in enumerate(read_lines(file)):
        row = []
        for x, char in enumerate(line):
            if char == "S":
                start_position = (x, y)
                row.append(".")
            else:
                row.append(char)
        data.append(row)

    grid = Grid(data, False)
    positions = grid.bfs({start_position}, 64)

    yield len(positions)

    grid_p2 = Grid(data, True)
    p1 = grid_p2.bfs(positions, 1)
    p2 = grid_p2.bfs(p1, 131)
    p3 = grid_p2.bfs(p2, 131)

    yield newton_polynomial(len(p1), len(p2), len(p3), (26501365 - 65) // 131)
