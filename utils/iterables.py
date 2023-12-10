"""Helper functions for iterables."""

from itertools import zip_longest
from typing import Iterable, Optional, TypeVar

T = TypeVar("T")


# Courtesy of https://docs.python.org/3/library/itertools.html
def grouper(
    iterable: Iterable[T],
    n: int,
    *,
    incomplete: str = "fill",
    fillvalue: Optional[T] = None,
) -> Iterable[Iterable[T]]:
    """Collect data into non-overlapping fixed-length chunks or blocks."""
    # grouper('ABCDEFG', 3, fillvalue='x') --> ABC DEF Gxx
    # grouper('ABCDEFG', 3, incomplete='strict') --> ABC DEF ValueError
    # grouper('ABCDEFG', 3, incomplete='ignore') --> ABC DEF
    args = [iter(iterable)] * n
    if incomplete == "fill":
        return zip_longest(*args, fillvalue=fillvalue)
    if incomplete == "strict":
        return zip(*args, strict=True)
    if incomplete == "ignore":
        return zip(*args)
    else:
        raise ValueError("Expected fill, strict, or ignore")
