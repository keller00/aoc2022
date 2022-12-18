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


def obstacles_to_str(
    obstacles: set[pos2d],
    height_start: int,
    height_end: int = 0,
) -> str:
    answer: list[str] = list()
    for y in range(height_start, height_end - 1, -1):
        line = ""
        for x in range(7):
            if pos2d(x, y) in obstacles:
                line += "#"
            else:
                line += "."
        answer.append(line)
    return "".join(answer)


def solve(inp: str) -> int:
    lines = inp.splitlines()
    moves = lines[0]
    height = 0
    obstacles: set[pos2d] = set()
    moves_g = enumerate(cycle(moves))
    shapes_g = cycle(shapes)
    lookback_size = 20
    state = tuple[int, str, int]
    cache: dict[state, tuple[int, int]] = dict()
    cycle_start: int | None = None
    cycle_end: int | None = None
    cycle_height: int | None = None
    found_cycle: int | None = None
    heights: list[int] = list()
    for s_i in range(1000_000):
        if cycle_end and s_i > cycle_end:
            break
        s_ba = next(shapes_g)
        # Add new shape
        s = tuple(p._replace(x=p.x + 2, y=p.y + height + 3) for p in s_ba)
        for m_i, m in moves_g:
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
                st: state = (
                    s_i % len(shapes),
                    obstacles_to_str(obstacles, height,
                                     height - lookback_size),
                    m_i % len(moves),
                )
                if s_i > lookback_size and not found_cycle:
                    if st in cache:
                        cycle_start = cache[st][0]
                        cycle_end = s_i
                        cycle_height = height - cache[st][1]
                        print(
                            f"found cycle {cycle_start} -> {cycle_end} "
                            f"for {cycle_height}", flush=True)
                        found_cycle = (
                            1000000000000 - cycle_start
                        ) % (cycle_end - cycle_start) + cycle_start
                    cache[st] = (s_i, height)
                for p in s:
                    obstacles.add(p)
                    height = max(height, p.y + 1)
                heights.append(height)
                break
    assert isinstance(cycle_height, int)
    assert isinstance(cycle_start, int)
    assert isinstance(cycle_end, int)
    assert isinstance(found_cycle, int)
    return (
        heights[cycle_start - 1]
        + cycle_height * (
            (1000000000000 - cycle_start) // (cycle_end - cycle_start)
        )
        + heights[found_cycle - 1] - heights[cycle_start - 1])


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
EXPECTED = 1514285714288


@pytest.mark.parametrize(
    ("s", "expected"),
    (
        (INPUT_S, EXPECTED),
        (
            helpers.read_file(os.path.join(THIS_DIR, "input.txt")),
            1565242165201,
        ),
    ),
)
def test(s: str, expected: int) -> None:
    assert solve(s) == expected


if __name__ == "__main__":
    raise SystemExit(main())
