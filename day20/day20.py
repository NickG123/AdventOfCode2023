"""Day 20."""

from collections import defaultdict, deque
from dataclasses import dataclass, field
from itertools import count
from math import lcm
from typing import Any, Iterator, TextIO

from utils.parse import read_lines


@dataclass
class FlipFlop:
    """Simple dataclass to represent a flip-flop."""

    state: bool = False

    def reset(self) -> None:
        """Reset this module"""
        self.state = False

    def __hash__(self) -> int:
        return hash(self.state)


@dataclass
class Conjunction:
    """Simple dataclass to represent a conjunction."""

    state: dict[str, bool] = field(default_factory=dict)

    def reset(self) -> None:
        """Reset this module"""
        for key in self.state:
            self.state[key] = False

    def __hash__(self) -> int:
        return hash(self.state.values())


@dataclass
class Broadcaster:
    """Simple dataclass to represent a broadcaster."""

    def reset(self) -> None:
        """Reset this module"""

    def __hash__(self) -> int:
        return id(self)


Module = FlipFlop | Conjunction | Broadcaster


def push_button(
    modules: dict[str, Module],
    connections: dict[str, list[str]],
) -> tuple[int, int, set[str]]:
    pulses = deque([("button", "broadcaster", False)])
    high_pulses = 0
    low_pulses = 0
    interesting_signals = set()
    while pulses:
        source_name, module_name, pulse = pulses.popleft()
        if module_name == "zr" and pulse:
            interesting_signals.add(source_name)
        if pulse:
            high_pulses += 1
        else:
            low_pulses += 1
        if module_name not in modules:
            # If a module name is not in the module, then it's untyped
            # just move on to the next pulse.
            continue
        module = modules[module_name]
        match module, pulse:
            case FlipFlop() as f, False:
                f.state = not f.state
                result: None | bool = f.state
            case FlipFlop(), True:
                result = None
            case Conjunction() as c, _:
                c.state[source_name] = pulse
                result = not all(c.state.values())
            case _:
                result = pulse
        if result is not None:
            for destination in connections[module_name]:
                pulses.append((module_name, destination, result))
    return (low_pulses, high_pulses, interesting_signals)


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 20."""

    connections = {}
    incoming_connections = defaultdict(list)
    modules: dict[str, Module] = {}
    for line in read_lines(file):
        source, destination_str = line.split(" -> ")
        destinations = destination_str.split(", ")

        if source.startswith("%"):
            source_name = source[1:]
            modules[source_name] = FlipFlop()
        elif source.startswith("&"):
            source_name = source[1:]
            modules[source_name] = Conjunction()
        elif source == "broadcaster":
            source_name = source
            modules[source_name] = Broadcaster()
        else:
            raise RuntimeError(f"Got unexpected source {source}")

        connections[source_name] = destinations
        for destination in destinations:
            incoming_connections[destination].append(source_name)

    # Initialize conjunctions
    for name, module in modules.items():
        if isinstance(module, Conjunction):
            for incoming_connection in incoming_connections[name]:
                module.state[incoming_connection] = False

    total_low_pulses = 0
    total_high_pulses = 0

    for i in range(1000):
        low_pulses, high_pulses, _ = push_button(modules, connections)
        total_low_pulses += low_pulses
        total_high_pulses += high_pulses
    yield total_low_pulses * total_high_pulses

    for m in modules.values():
        m.reset()

    # I hate the questions where you have to look at the input...
    interesting_module_offsets = {}
    for i in count(1):
        _, _, interesting_modules = push_button(modules, connections)
        for interesting_module in interesting_modules:
            if interesting_module not in interesting_module_offsets:
                interesting_module_offsets[interesting_module] = i
        if len(interesting_module_offsets) == 4:
            break
    yield lcm(*interesting_module_offsets.values())
