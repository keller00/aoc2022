from __future__ import annotations

import argparse
import os.path

import pytest

import helpers

THIS_DIR = os.path.dirname(__file__)


def single_move(
    obstacles: set[helpers.pos2d],
    sand: helpers.pos2d,
) -> helpers.pos2d:
    under = sand._replace(y=sand.y + 1)
    under_left = sand._replace(x=sand.x - 1, y=sand.y + 1)
    under_right = sand._replace(x=sand.x + 1, y=sand.y + 1)
    if under not in obstacles:
        return under
    elif under_left not in obstacles:
        return under_left
    elif under_right not in obstacles:
        return under_right
    return sand


def move(
    rocks: set[helpers.pos2d],
    sands: set[helpers.pos2d],
    sand: helpers.pos2d,
    bottom: int,
) -> helpers.pos2d:
    obstacles = rocks | sands
    while True:
        new_sand = single_move(obstacles, sand)
        if new_sand.y > bottom:
            return new_sand
        elif new_sand == sand:
            return sand
        sand = new_sand


def solve(s: str) -> int:
    lines = s.splitlines()
    rocks: set[helpers.pos2d] = set()
    for line in lines:
        steps = line.split(" -> ")
        for i in range(0, len(steps) - 1):
            pair = list(map(lambda e: helpers.pos2d(
                *map(int, e.split(',', 1))), steps[i: i + 2]))
            from_, to = sorted(pair)
            for x in range(from_.x, to.x + 1):
                for y in range(from_.y, to.y + 1):
                    rocks.add(helpers.pos2d(x, y))
    bottom = max(map(lambda e: e.y, rocks))
    turns = 0
    sands: set[helpers.pos2d] = set()
    while True:
        sand = helpers.pos2d(500, 0)
        final_sand_loc = move(rocks, sands, sand, bottom)
        turns += 1
        if final_sand_loc == helpers.pos2d(500, 0):
            break
        sands.add(final_sand_loc)

    return turns


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=os.path.join(THIS_DIR, "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


INPUT_S = '''\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
'''
EXPECTED = 93


@pytest.mark.parametrize(
    ("s", "expected"),
    (
        (INPUT_S, EXPECTED),
        (helpers.read_file(os.path.join(THIS_DIR, "input.txt")), 24589),
    ),
)
def test(s: str, expected: int) -> None:
    assert solve(s) == expected


if __name__ == "__main__":
    raise SystemExit(main())
