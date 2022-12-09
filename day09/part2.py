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
        if abs(x_diff) + abs(y_diff) >= 3:
            return pos2d(
                t_pos.x + int(x_diff / abs(x_diff)),
                t_pos.y + int(y_diff / abs(y_diff)),
            )
    return t_pos


def solve(s: str) -> int:
    lines = s.splitlines()
    visited: set[pos2d] = {pos2d(0, 0)}
    knot_num = 10
    knots = [pos2d(0, 0)] * knot_num
    for line in lines:
        motion, times = line.split()
        for _ in range(int(times)):
            if motion == "U":
                knots[0] = knots[0]._replace(y=knots[0].y + 1)
            elif motion == "D":
                knots[0] = knots[0]._replace(y=knots[0].y - 1)
            elif motion == "L":
                knots[0] = knots[0]._replace(x=knots[0].x - 1)
            elif motion == "R":
                knots[0] = knots[0]._replace(x=knots[0].x + 1)
            for i in range(1, knot_num):
                knots[i] = move_tail(knots[i - 1], knots[i])
            visited.add(knots[knot_num - 1])
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
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
'''
EXPECTED = 36


@pytest.mark.parametrize(
    ("s", "expected"),
    (
        (INPUT_S, EXPECTED),
        (helpers.read_file(os.path.join(THIS_DIR, "input.txt")), 2259),
    ),
)
def test(s: str, expected: int) -> None:
    assert solve(s) == expected


if __name__ == "__main__":
    raise SystemExit(main())
