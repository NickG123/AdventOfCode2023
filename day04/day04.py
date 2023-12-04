"""Day 04."""

from collections import defaultdict
from typing import Any, Iterator, TextIO

from utils.parse import read_lines


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 04."""
    part1 = 0
    copies = defaultdict[int, int](int)
    card_num = 0
    for card_num, line in enumerate(read_lines(file), start=1):
        _, numbers = line.split(": ")
        winning_number_list, my_number_list = numbers.split(" | ")
        winning_numbers = set(
            int(num) for num in winning_number_list.split(" ") if num.strip()
        )
        my_numbers = set(int(num) for num in my_number_list.split(" ") if num.strip())
        match_count = len(my_numbers.intersection(winning_numbers))
        for i in range(card_num + 1, card_num + match_count + 1):
            copies[i] += copies[card_num] + 1
        if match_count > 0:
            part1 += 2 ** (match_count - 1)
    yield part1
    yield sum(copies.values()) + card_num
