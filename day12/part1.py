from __future__ import annotations

import argparse
import os.path
from collections import deque

import pytest

import helpers
from helpers import pos2d

THIS_DIR = os.path.dirname(__file__)


def solve(s: str) -> int:
    lines = s.splitlines()
    heights: dict[pos2d, int] = dict()
    start: pos2d | None = None
    end: pos2d | None = None
    cost_to_finish: dict[pos2d, int | None] = dict()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            cost_to_finish[pos2d(x, y)] = None
            if c == 'S':
                start = pos2d(x, y)
                c = "a"
            elif c == 'E':
                end = pos2d(x, y)
                c = "z"
            heights[pos2d(x, y)] = ord(c) - ord("a")
    assert start is not None
    assert end is not None
    d: deque[pos2d] = deque([end])
    height = max([coord.y for coord in heights.keys()]) + 1
    width = max([coord.x for coord in heights.keys()]) + 1
    cost_to_finish[end] = 0
    while d:
        i = d.popleft()
        assert cost_to_finish[i] is not None
        for n in helpers.adjacent_4(i.x, i.y):
            p = pos2d(*n)
            if (
                p.x == -1
                or p.x == width
                or p.y == -1
                or p.y == height
            ):
                continue
            n_val = cost_to_finish[p]
            c_val = cost_to_finish[i]
            assert isinstance(c_val, int)
            if (
                heights[p] >= heights[i] - 1
                and (
                    n_val is None or n_val > c_val + 1
                )
            ):
                cost_to_finish[p] = c_val + 1
                d.append(p)
    finish_cost = cost_to_finish[start]
    assert isinstance(finish_cost, int)
    return finish_cost


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=os.path.join(THIS_DIR, "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


INPUT_S = '''\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''
EXPECTED = 31


@pytest.mark.parametrize(
    ("s", "expected"),
    (
        (INPUT_S, EXPECTED),
        (helpers.read_file(os.path.join(THIS_DIR, "input.txt")), 339),
    ),
)
def test(s: str, expected: int) -> None:
    assert solve(s) == expected


if __name__ == "__main__":
    raise SystemExit(main())
