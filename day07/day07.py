"""Day 07."""

from collections import Counter
from enum import Enum
from functools import total_ordering
from typing import Any, Iterator, TextIO

from utils.parse import read_lines


class HandType(Enum):
    """The various types of hands, ranked."""

    HighCard = 1
    OnePair = 2
    TwoPair = 3
    ThreeOfAKind = 4
    FullHouse = 5
    FourOfAKind = 6
    FiveOfAKind = 7


P1_CARD_RANKS = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}
P2_CARD_RANKS = P1_CARD_RANKS | {"J": 1}


@total_ordering
class Hand:
    """A class representing a hand of camel cards."""

    def __init__(self, line: str, jokers: bool, card_ranks: dict[str, int]) -> None:
        cards, bid = line.split(" ")
        self.cards = cards
        self.bid = int(bid)
        self.card_ranks = card_ranks

        counts = Counter(cards)
        if jokers and cards != "JJJJJ":
            wildcards = counts.pop("J", 0)
            most_common = counts.most_common(1)[0][0]
            counts[most_common] += wildcards

        match [val for _, val in counts.most_common(2)]:
            case [5]:
                self.rank = HandType.FiveOfAKind
            case [4, _]:
                self.rank = HandType.FourOfAKind
            case [3, 2]:
                self.rank = HandType.FullHouse
            case [3, _]:
                self.rank = HandType.ThreeOfAKind
            case [2, 2]:
                self.rank = HandType.TwoPair
            case [2, _]:
                self.rank = HandType.OnePair
            case _:
                self.rank = HandType.HighCard

    def __eq__(self, other: Any) -> bool:
        """Check if a hand is equal to another."""
        if not isinstance(other, Hand):
            return NotImplemented
        if self.rank != other.rank or self.cards != other.cards:
            return False
        return True

    def __le__(self, other: Any) -> bool:
        """Check if a hand is less than another."""
        if not isinstance(other, Hand):
            return NotImplemented
        if self.rank != other.rank:
            return self.rank.value <= other.rank.value
        for card, other_card in zip(self.cards, other.cards):
            if card != other_card:
                return self.card_ranks[card] <= self.card_ranks[other_card]
        return True


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 07."""
    lines = list(read_lines(file))
    p1_hands = [Hand(line, False, P1_CARD_RANKS) for line in lines]
    p2_hands = [Hand(line, True, P2_CARD_RANKS) for line in lines]
    yield sum(rank * hand.bid for rank, hand in enumerate(sorted(p1_hands), start=1))
    yield sum(rank * hand.bid for rank, hand in enumerate(sorted(p2_hands), start=1))
