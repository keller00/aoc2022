from __future__ import annotations

import argparse
import os.path
import re
from collections import deque
from copy import deepcopy
from typing import Generator

import pytest

import helpers

THIS_DIR = os.path.dirname(__file__)
BLUEPRINT_NAME_RE = re.compile(r"Blueprint (\d+):")
BLUEPRINT_SINGLE_RE = re.compile(r"  Each (\w+) robot costs (\d+) (\w+).")
BLUEPRINT_DOUBLE_RE = re.compile(
    r"  Each (\w+) robot costs (\d+) (\w+) and (\d+) (\w+).")


def create_dependency_graph(blueprint: dict[str, int]) -> list[str]:
    l: list[str] = ["geode"]

    def _recursive_fn(name: str) -> None:
        l.extend(blueprint[name].keys())
        for i in blueprint[name].keys():
            if i == name:
                continue
            _recursive_fn(i)
    _recursive_fn("geode")
    return l


def get_enoughs(blueprint: dict[str, int]) -> dict[str, int]:
    enoughs = {r: 0 for r in ["geode", "obsidian", "clay", "ore"]}

    for u in blueprint.values():
        for k, v in u.items():
            enoughs[k] = max(enoughs[k], v)

    return enoughs


def quality_level(blueprint: dict[str, int], id: int, robots: dict[str, int]) -> int:
    resources = {e: 0 for e in ("ore", "clay", "geode", "obsidian")}
    robot_build_order = create_dependency_graph(blueprint)
    enough = get_enoughs(blueprint)

    for i in range(24):
        for r, amount in robots.items():
            resources[r] += amount
        for r in robot_build_order:
            if robots[r] == enough[r]:
                continue
            needs = blueprint[r]
            can_build = all(resources[ingredient] >=
                            am for ingredient, am in needs.items())
            if can_build:
                for ingredient, am in needs.items():
                    resources[ingredient] -= am
                robots[r] += 1

    return resources["geode"]


def solve(s: str) -> int:
    overall_quality = 0
    blueprints: list[dict[str, int]] = []
    for b in map(lambda e: e.splitlines(), s.split("\n\n")):
        b_name = int(BLUEPRINT_NAME_RE.fullmatch(b[0]).group(1))
        this_b = dict()
        for line in b[1:]:
            single = BLUEPRINT_SINGLE_RE.fullmatch(line)
            if single:
                this_b[single.group(1)] = {
                    single.group(3): int(single.group(2))}
            else:
                double = BLUEPRINT_DOUBLE_RE.fullmatch(line)
                assert double is not None
                this_b[double.group(1)] = {
                    double.group(3): int(double.group(2)),
                    double.group(5): int(double.group(4)),
                }
        blueprints.append(this_b)
    for i, b in enumerate(blueprints):
        overall_quality += quality_level(b, i + 1,
                                         {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0})
    return overall_quality


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=os.path.join(THIS_DIR, "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


INPUT_S = '''\
Blueprint 1:
  Each ore robot costs 4 ore.
  Each clay robot costs 2 ore.
  Each obsidian robot costs 3 ore and 14 clay.
  Each geode robot costs 2 ore and 7 obsidian.

Blueprint 2:
  Each ore robot costs 2 ore.
  Each clay robot costs 3 ore.
  Each obsidian robot costs 3 ore and 8 clay.
  Each geode robot costs 3 ore and 12 obsidian.
'''
EXPECTED = 33


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
