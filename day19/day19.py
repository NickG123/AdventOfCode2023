"""Day 19."""
from __future__ import annotations

import operator
from dataclasses import dataclass
from enum import Enum
from itertools import takewhile
from math import prod
from typing import Any, Callable, Iterator, TextIO

from utils.parse import read_lines

comparitors = {
    "<": operator.lt,
    ">": operator.gt,
}


class Result(Enum):
    """A class containing the options for the result."""

    REJECTED = "R"
    ACCEPTED = "A"


Item = dict[str, int]


@dataclass
class RuleCondition:
    """The condition portion of a rule."""

    item_property: str
    comparitor: Callable[[int, int], bool]
    comparison: int

    @staticmethod
    def parse(data: str) -> RuleCondition:
        """Parse the condition from a string."""
        item_property = data[0]
        comparitor = comparitors[data[1]]
        comparison = int(data[2:])
        return RuleCondition(item_property, comparitor, comparison)

    def evaluate(self, item: Item) -> bool:
        """Evaluate the item against this condition."""
        return self.comparitor(item[self.item_property], self.comparison)

    def split_range(
        self, lower: int, upper: int
    ) -> tuple[tuple[int, int], tuple[int, int]]:
        """Split a range into the True and False halves."""
        if self.comparitor == operator.lt:
            return (lower, self.comparison - 1), (self.comparison, upper)
        else:
            return (
                (self.comparison + 1, upper),
                (lower, self.comparison),
            )


@dataclass
class ProcessingTreeNode:
    """A single workflow in the processing tree."""

    name: str
    rules: list[tuple[RuleCondition, ProcessingTreeNode | Result]]
    default: ProcessingTreeNode | Result

    def _next_step(self, item: Item) -> ProcessingTreeNode | Result:
        """Get the next step of evaluation."""
        for rule_condition, result in self.rules:
            if rule_condition.evaluate(item):
                return result
        return self.default

    def evaluate(self, item: Item) -> Result:
        """Evaluate an item against this node."""
        next_step = self._next_step(item)
        if isinstance(next_step, ProcessingTreeNode):
            return next_step.evaluate(item)
        return next_step

    def _find_rule_restrictions(
        self,
        next_step: Result | ProcessingTreeNode,
        restrictions: dict[str, tuple[int, int]],
    ) -> list[dict[str, tuple[int, int]]]:
        """Handle the next step of either recursing or returning."""
        if isinstance(next_step, ProcessingTreeNode):
            return next_step.find_restrictions(restrictions)
        elif next_step == Result.ACCEPTED:
            return [restrictions]
        return []

    def find_restrictions(
        self, restrictions: dict[str, tuple[int, int]]
    ) -> list[dict[str, tuple[int, int]]]:
        """Find the list of restrictions on accepted ranges of data."""
        new_restrictions = dict(restrictions)
        accepted_ranges: list[dict[str, tuple[int, int]]] = []

        for rule_condition, result in self.rules:
            current_restriction = new_restrictions[rule_condition.item_property]
            true_half, false_half = rule_condition.split_range(*current_restriction)

            # Handle the true half, if it exists
            if true_half[0] <= true_half[1]:
                accepted_ranges.extend(
                    self._find_rule_restrictions(
                        result,
                        new_restrictions | {rule_condition.item_property: true_half},
                    )
                )

            # Handle the false half.  If it doesn't exist, the remaining rules are
            # never hit, so just break.
            if false_half[0] <= false_half[1]:
                new_restrictions[rule_condition.item_property] = false_half
            else:
                break
        else:
            accepted_ranges.extend(
                self._find_rule_restrictions(self.default, new_restrictions)
            )

        return accepted_ranges

    @staticmethod
    def _build_result(
        workflows: dict[str, str], result_label: str
    ) -> ProcessingTreeNode | Result:
        """Get the result or next processing node."""
        try:
            return Result(result_label)
        except ValueError:
            return ProcessingTreeNode.build_processing_tree(workflows, result_label)

    @staticmethod
    def build_processing_tree(
        workflows: dict[str, str], root_node: str
    ) -> ProcessingTreeNode:
        """Build the processing tree."""
        # Just to verify that we don't have any circular references, we'll remove
        # each node as we process it
        workflow = workflows.pop(root_node)
        rule_strings = workflow.split(",")
        rules: list[tuple[RuleCondition, Result | ProcessingTreeNode]] = []
        for rule in rule_strings[:-1]:
            condition, result = rule.split(":")
            rules.append(
                (
                    RuleCondition.parse(condition),
                    ProcessingTreeNode._build_result(workflows, result),
                )
            )

        return ProcessingTreeNode(
            name=root_node,
            rules=rules,
            default=ProcessingTreeNode._build_result(workflows, rule_strings[-1]),
        )


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 19."""
    data = read_lines(file)
    workflows = list(takewhile(lambda s: s, data))
    workflows_by_name = {
        name: value.rstrip("}")
        for name, value in [workflow.split("{") for workflow in workflows]
    }
    processing_tree = ProcessingTreeNode.build_processing_tree(workflows_by_name, "in")
    total = 0
    for part_data in data:
        part_pieces = [p.split("=") for p in part_data.strip("{}").split(",")]
        part = {key: int(value) for key, value in part_pieces}
        if processing_tree.evaluate(part) == Result.ACCEPTED:
            total += sum(part.values())

    yield total

    restrictions = processing_tree.find_restrictions(
        {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}
    )
    yield sum(
        prod(upper - lower + 1 for lower, upper in restriction.values())
        for restriction in restrictions
    )
