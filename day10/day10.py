"""Day 10."""

from typing import Any, Iterator, TextIO

from utils.parse import read_lines

Point = tuple[int, int]

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

OPPOSITES = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT,
}

PIPE_NEIGHBOURS = {
    "|": {UP, DOWN},
    "-": {LEFT, RIGHT},
    "L": {UP, RIGHT},
    "J": {UP, LEFT},
    "7": {LEFT, DOWN},
    "F": {RIGHT, DOWN},
}


def get_loop_spaces(
    position: Point, direction: Point, pipes: dict[Point, str], start: Point
) -> tuple[set[Point], set[Point]] | None:
    """Find spaces making up a loop, or None if it's not a loop.

    Also return the directions leading out of the start node.
    """
    spaces = {start}
    start_directions = {direction}
    while True:
        position = (position[0] + direction[0], position[1] + direction[1])
        if position == start:
            start_directions.add(OPPOSITES[direction])
            break
        new_pipe = pipes.get(position)
        if new_pipe is None:
            return None
        opposite = OPPOSITES[direction]
        pipe_neighbours = PIPE_NEIGHBOURS[new_pipe]
        if opposite not in pipe_neighbours:
            return None
        direction = next(p for p in pipe_neighbours if p != opposite)
        spaces.add(position)
    return spaces, start_directions


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 10."""
    pipes = {}
    for y, line in enumerate(read_lines(file)):
        for x, char in enumerate(line):
            if char == "S":
                start = (x, y)
            if char in PIPE_NEIGHBOURS:
                pipes[(x, y)] = char

    for direction in [UP, DOWN, LEFT, RIGHT]:
        result = get_loop_spaces(start, direction, pipes, start)
        if result is not None:
            loop, start_directions = result
            start_pipe = next(
                k for k, v in PIPE_NEIGHBOURS.items() if v == start_directions
            )
            break
    else:
        raise Exception("No loop found")

    yield len(loop) // 2

    pipes[start] = start_pipe
    min_x = min(x for x, _ in loop)
    max_x = max(x for x, _ in loop)
    min_y = min(y for _, y in loop)
    max_y = max(y for _, y in loop)

    enclosed = 0
    for y in range(min_y, max_y + 1):
        in_loop = False
        for x in range(min_x, max_x + 1):
            if (x, y) in loop:
                if UP in PIPE_NEIGHBOURS[pipes[(x, y)]]:
                    in_loop = not in_loop
            elif in_loop:
                enclosed += 1

    yield enclosed
