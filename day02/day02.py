"""Day 02."""

from collections import Counter
from dataclasses import dataclass
from enum import Enum
from math import prod
from typing import Any, Iterator, TextIO

from utils.parse import read_lines


class Cube(Enum):
    """A class representing a cube."""

    RED = "red"
    BLUE = "blue"
    GREEN = "green"


@dataclass
class Game:
    """A class representing a game."""

    game_id: int
    turns: list[Counter[Cube]]


def parse_game(line: str) -> Game:
    """Parse a game of cubes."""
    game, turns = line.split(": ")
    game_id = int(game.removeprefix("Game "))
    turn_list = []
    for turn in turns.split("; "):
        turn_dict = Counter[Cube]()
        for cube in turn.split(", "):
            number, color = cube.split(" ")
            turn_dict[Cube(color)] = int(number)
        turn_list.append(turn_dict)
    return Game(game_id, turn_list)


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 02."""
    part_1_guess = Counter({Cube.RED: 12, Cube.GREEN: 13, Cube.BLUE: 14})
    part_1_total = 0
    part_2_total = 0

    for line in read_lines(file):
        game = parse_game(line)

        if all(turn <= part_1_guess for turn in game.turns):
            part_1_total += game.game_id

        part_2_total += prod(
            [max(turn.get(cube, 0) for turn in game.turns) for cube in Cube]
        )

    yield part_1_total
    yield part_2_total
