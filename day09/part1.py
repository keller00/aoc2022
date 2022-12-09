from __future__ import annotations

import argparse
import os.path
from typing import NamedTuple

import pytest

import helpers

THIS_DIR = os.path.dirname(__file__)


class pos2d(NamedTuple):
    x: int
    y: int


def move_tail(
    h_pos: pos2d,
    t_pos: pos2d,
) -> pos2d:
    if h_pos.x == t_pos.x and h_pos.y == t_pos.y:
        return t_pos
    if h_pos.x == t_pos.x:
        # Same horizontal line
        if t_pos.y - 2 == h_pos.y:
            return t_pos._replace(y=t_pos.y - 1)
        elif t_pos.y + 2 == h_pos.y:
            return t_pos._replace(y=t_pos.y + 1)
    elif h_pos.y == t_pos.y:
        # Same vertical line
        if t_pos.x - 2 == h_pos.x:
            return t_pos._replace(x=t_pos.x - 1)
        elif t_pos.x + 2 == h_pos.x:
            return t_pos._replace(x=t_pos.x + 1)
    else:
        # Diagonal
        x_diff = h_pos.x - t_pos.x
        y_diff = h_pos.y - t_pos.y
        if abs(x_diff) + abs(y_diff) == 3:
            return pos2d(
                t_pos.x + int(x_diff / abs(x_diff)),
                t_pos.y + int(y_diff / abs(y_diff)),
            )
    return t_pos


def solve(s: str) -> int:
    lines = s.splitlines()
    h_pos: pos2d = pos2d(0, 0)
    t_pos: pos2d = pos2d(0, 0)
    visited: set[pos2d] = {t_pos}
    for line in lines:
        motion, times = line.split()
        for _ in range(int(times)):
            if motion == "U":
                h_pos = h_pos._replace(y=h_pos.y + 1)
            elif motion == "D":
                h_pos = h_pos._replace(y=h_pos.y - 1)
            elif motion == "L":
                h_pos = h_pos._replace(x=h_pos.x - 1)
            elif motion == "R":
                h_pos = h_pos._replace(x=h_pos.x + 1)
            t_pos = move_tail(h_pos, t_pos)
            visited.add(t_pos)
    return len(visited)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=os.path.join(THIS_DIR, "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


INPUT_S = '''\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
'''
EXPECTED = 13


@pytest.mark.parametrize(
    ("s", "expected"),
    (
        (INPUT_S, EXPECTED),
        (helpers.read_file(os.path.join(THIS_DIR, "input.txt")), 5710),
    ),
)
def test(s: str, expected: int) -> None:
    assert solve(s) == expected


if __name__ == "__main__":
    raise SystemExit(main())
