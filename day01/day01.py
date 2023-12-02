"""Day 01."""

from typing import Any, Iterator, Sequence, TextIO

from utils.parse import read_lines

words_to_numbers = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def is_word(s: Sequence[str], index: int, word: str) -> bool:
    """Check if the provided index in the string is the start of the provided word."""
    for offset, char in enumerate(word):
        if index + offset >= len(s) or s[index + offset] != char:
            return False
    return True


def first_digit(s: Sequence[str], forward: bool, check_words: bool) -> str:
    """Find the first digit in a string, moving front to back or back to front.

    If check_words is true, also looks for numbers written as words.
    """
    if forward:
        r = range(len(s))
    else:
        r = range(len(s) - 1, -1, -1)
    for i in r:
        if s[i].isdigit():
            return s[i]
        if check_words:
            for word, val in words_to_numbers.items():
                if is_word(s, i, word):
                    return val
    raise ValueError(f"Failed to find a number in string {s}")


# def first_digit(s: Iterable[str]) -> str:
#     return next(dropwhile(lambda x: not x.isdigit(), s))


def get_calibration_code(s: str, check_words: bool) -> int:
    first_number = first_digit(s, True, check_words)
    last_number = first_digit(s, False, check_words)

    return int(first_number + last_number)


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 01."""
    lines = list(read_lines(file))

    yield sum(get_calibration_code(line, False) for line in lines)
    yield sum(get_calibration_code(line, True) for line in lines)
