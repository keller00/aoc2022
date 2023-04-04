from __future__ import annotations

import argparse
import os.path
import re
from functools import lru_cache
from typing import NamedTuple

import pytest

import helpers

THIS_DIR = os.path.dirname(__file__)
INPUT_RE = re.compile(
    r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)")

valves: dict[str, Valve] = {}
state = tuple[tuple[str, ...], str]
cache: dict[int, dict[state, int]] = {i: dict() for i in range(1, 31)}


class Valve(NamedTuple):
    flow_rate: int
    leads_to: list[str]


def release_most_pressure(
    open_valves: tuple[str, ...],
    c_v: str,
    time_left: int,
) -> int:
    possible_outcomes: list[tuple[state, int]] = []
    c_valve = valves[c_v]
    for s, released_so_far in cache[time_left].items():
        if c_v not in open_valves and valves[c_v].flow_rate > 0:
            # open current valve
            possible_outcomes.append(
                (
                    (open_valves + (c_v,), c_v),
                    released_so_far + time_left * valves[c_v].flow_rate,
                )
            )
        for d in c_valve.leads_to:
            # move on
            possible_outcomes.append(
                (
                    (open_valves, d),
                    released_so_far,
                )
            )
        for outcome, so_far in possible_outcomes:
            if outcome in cache[time_left]:
                cache[time_left][outcome] = max(
                    cache[time_left][outcome], so_far)
            else:
                cache[time_left][outcome] = so_far
    return max(cache[time_left].values())


def solve(s: str) -> int:
    lines = s.splitlines()
    for line in lines:
        parsed_line = INPUT_RE.fullmatch(line)
        if parsed_line is None:
            raise Exception(f"What is this {line}")
        valve, flow_rate, leads_to_s = parsed_line.groups()
        leads_to = leads_to_s.split(", ")
        valves[valve] = Valve(int(flow_rate), leads_to)

    # for k, (_, _, ne) in valves.items():
    #     for i, n in enumerate(ne):
    #         if isinstance(valves[k].leads_to[i], str):
    #             valves[k].leads_to[i] = valves[n]
    return release_most_pressure(tuple(), "AA", 0, 30)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=os.path.join(THIS_DIR, "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


INPUT_S = '''\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
'''
EXPECTED = 1651


@pytest.mark.parametrize(
    ("s", "expected"),
    (
        (INPUT_S, EXPECTED),
        # (helpers.read_file(os.path.join(THIS_DIR, "input.txt")), solution),
    ),
)
def test(s: str, expected: int) -> None:
    assert solve(s) == expected


if __name__ == "__main__":
    raise SystemExit(main())
