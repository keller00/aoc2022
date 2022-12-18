from __future__ import annotations

import argparse
import os.path
import re

import pytest

import helpers
from helpers import pos2d

THIS_DIR = os.path.dirname(__file__)
INPUT_RE = re.compile(
    r"Sensor at x=(-?\d+), y=(-?\d+): closest "
    r"beacon is at x=(-?\d+), y=(-?\d+)",
)


def manhattan_distance(lhs: helpers.pos2d, rhs: helpers.pos2d) -> int:
    return abs(lhs.x - rhs.x) + abs(lhs.y - rhs.y)


def solve(inp: str, y: int) -> int:
    seen: set[pos2d] = set()
    scanners: dict[pos2d, pos2d] = dict()
    for line in inp.splitlines():
        ma = INPUT_RE.fullmatch(line)
        assert ma
        x_s, y_s, x_b, y_b = map(int, ma.groups())
        scanners[pos2d(x_s, y_s)] = pos2d(x_b, y_b)
    for s, b in scanners.items():
        d = manhattan_distance(s, b)
        distance = abs(s.y - y)
        if distance <= d:
            for i in range(1, d - distance + 1):
                seen.add(pos2d(s.x - i, y))
                seen.add(pos2d(s.x + i, y))
            seen.add(pos2d(s.x, y))
            if b in seen:
                seen.remove(b)
    return len({c for c in seen})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=os.path.join(THIS_DIR, "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read(), 2000000))

    return 0


INPUT_S = '''\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
'''


@pytest.mark.parametrize(
    ("s", "y", "expected"),
    (
        (INPUT_S, 10, 26),
        (
            helpers.read_file(os.path.join(THIS_DIR, "input.txt")),
            2000000,
            5832528,
        ),
    ),
)
def test(s: str, y: int, expected: int) -> None:
    assert solve(s, y) == expected


if __name__ == "__main__":
    raise SystemExit(main())
