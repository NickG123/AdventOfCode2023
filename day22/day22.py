"""Day 22."""
from __future__ import annotations

from collections import defaultdict
from typing import Any, Iterator, TextIO

from utils.parse import read_lines

Position = tuple[int, int, int]


class Brick:
    def __init__(self, s: str) -> None:
        """Initialize a brick from a string."""
        start_pos, stop_pos = s.split("~")
        self.start = tuple(int(x) for x in start_pos.split(","))
        self.stop = tuple(int(x) for x in stop_pos.split(","))
        self.lowest_z = min(self.start[2], self.stop[2])

    def coord_range(self, dim: int) -> range:
        """Get the range of coordinates the brick spans for a single dimension"""
        return range(
            min(self.start[dim], self.stop[dim]),
            max(self.start[dim], self.stop[dim]) + 1,
        )

    def cubes(self) -> Iterator[Position]:
        """Get all the cubes that make up this brick."""
        for x in self.coord_range(0):
            for y in self.coord_range(1):
                for z in self.coord_range(2):
                    yield (x, y, z)

    def compute_bricks_dropped(
        self,
        supported_bricks: dict[Brick, set[Brick]],
        bricks_below: dict[Brick, set[Brick]],
    ) -> int:
        """Compute how many other bricks will be dropped if this brick is disintegrated."""
        dropped_bricks = {self}
        can_drop = set(supported_bricks[self])
        while can_drop:
            for brick in set(can_drop):
                if all(
                    supported_brick in dropped_bricks
                    for supported_brick in bricks_below[brick]
                ):
                    dropped_bricks.add(brick)
                    can_drop.remove(brick)
                    can_drop.update(supported_bricks[brick])
                    break
            else:
                break
        return len(dropped_bricks) - 1


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 22."""
    settled_height: dict[tuple[int, int], int] = defaultdict(int)
    resting_bricks = {}
    bricks_below = defaultdict(set)
    supported_bricks = defaultdict(set)
    bricks = [Brick(line) for i, line in enumerate(read_lines(file))]
    for brick in sorted(bricks, key=lambda b: b.lowest_z):
        # print(brick.start, brick.stop)
        drop_distances = [
            cube[2] - settled_height[(cube[0], cube[1])] for cube in brick.cubes()
        ]
        for cube in brick.cubes():
            new_position = (cube[0], cube[1], cube[2] - min(drop_distances) + 1)
            settled_height[(cube[0], cube[1])] = new_position[2]
            resting_bricks[new_position] = brick
            spot_below = (cube[0], cube[1], new_position[2] - 1)
            if spot_below in resting_bricks:
                if resting_bricks[spot_below] != brick:
                    bricks_below[brick].add(resting_bricks[spot_below])
                    supported_bricks[resting_bricks[spot_below]].add(brick)

    p1_total = 0
    p2_total = 0
    for brick in bricks:
        bricks_dropped = brick.compute_bricks_dropped(supported_bricks, bricks_below)
        if bricks_dropped == 0:
            p1_total += 1
        else:
            p2_total += bricks_dropped
    yield p1_total
    yield p2_total
