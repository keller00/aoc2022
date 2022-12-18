from __future__ import annotations

import argparse
import os.path
from itertools import cycle

import pytest

import helpers
from helpers import pos2d

THIS_DIR = os.path.dirname(__file__)

shapes: tuple[tuple[pos2d, ...], ...] = (
    (
        pos2d(x=0, y=0),
        pos2d(x=1, y=0),
        pos2d(x=2, y=0),
        pos2d(x=3, y=0),
    ),
    (
        pos2d(x=1, y=0),
        pos2d(x=0, y=1),
        pos2d(x=1, y=1),
        pos2d(x=2, y=1),
        pos2d(x=1, y=2),
    ),
    (
        pos2d(x=0, y=0),
        pos2d(x=1, y=0),
        pos2d(x=2, y=0),
        pos2d(x=2, y=1),
        pos2d(x=2, y=2),
    ),
    (
        pos2d(x=0, y=0),
        pos2d(x=0, y=1),
        pos2d(x=0, y=2),
        pos2d(x=0, y=3),
    ),
    (
        pos2d(x=0, y=0),
        pos2d(x=1, y=0),
        pos2d(x=0, y=1),
        pos2d(x=1, y=1),
    ),
)


def solve(inp: str) -> int:
    lines = inp.splitlines()
    moves = lines[0]
    height = 0
    obstacles: set[pos2d] = set()
    moves_g = cycle(moves)
    for i, s_ba in enumerate(cycle(shapes)):
        if i == 1405:
            break
        # Add new shape
        s = tuple(p._replace(x=p.x + 2, y=p.y + height + 3) for p in s_ba)
        for m in moves_g:
            # Jet move
            if m == "<" and not any(p.x == 0 for p in s):
                moved = tuple(p._replace(x=p.x - 1) for p in s)
                can_move = not any(p in obstacles for p in moved)
                if can_move:
                    s = moved
            elif m == ">" and not any(p.x == 6 for p in s):
                moved = tuple(p._replace(x=p.x + 1) for p in s)
                can_move = not any(p in obstacles for p in moved)
                if can_move:
                    s = moved
            # Can fall?
            fallen = tuple(p._replace(y=p.y - 1) for p in s)
            can_fall = not any(p.y == -1 or p in obstacles for p in fallen)
            if can_fall:
                #  Yes: keep going!
                s = fallen
            else:
                #  No: add to obstacles move on
                pass
                for p in s:
                    obstacles.add(p)
                    height = max(height, p.y + 1)
                break
    return height


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=os.path.join(THIS_DIR, "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


INPUT_S = '''\
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
'''
EXPECTED = 3068


@pytest.mark.parametrize(
    ("s", "expected"),
    (
        (INPUT_S, EXPECTED),
        (helpers.read_file(os.path.join(THIS_DIR, "input.txt")), 3144),
    ),
)
def test(s: str, expected: int) -> None:
    assert solve(s) == expected


if __name__ == "__main__":
    raise SystemExit(main())
