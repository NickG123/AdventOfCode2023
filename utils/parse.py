"""Helper functions for parsing input."""
from typing import Iterator, TextIO


def read_lines(file: TextIO) -> Iterator[str]:
    """Read lines from a file, stripping newlines."""
    for line in file:
        yield line.strip("\r\n")
