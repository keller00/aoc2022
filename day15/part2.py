from __future__ import annotations

import argparse
import os.path
import re

import pytest

import helpers

THIS_DIR = os.path.dirname(__file__)
INPUT_RE = re.compile(
    r"Sensor at x=(-?\d+), y=(-?\d+): closest "
    r"beacon is at x=(-?\d+), y=(-?\d+)",
)


def manhattan_distance(lhs: helpers.pos2d, rhs: helpers.pos2d) -> int:
    return abs(lhs.x - rhs.x) + abs(lhs.y - rhs.y)


def tuning_frequency(beacon: helpers.pos2d) -> int:
    return beacon.x * 4000000 + beacon.y


class Rhombus:
    def __init__(
        self,
        middle: helpers.pos2d,
        distance: int,
    ):
        self.middle = middle
        self.distance = distance


def solve_for_row(rs: set[Rhombus], col: int) -> int | None:
    ranges: list[tuple[int, int]] = list()
    for r in rs:
        d_from_x = r.distance - abs(col - r.middle.y)
        if d_from_x >= 0:
            ranges.append((r.middle.x - d_from_x, r.middle.x + d_from_x))
            m_r = helpers.merge_ranges(ranges)
            if len(m_r) > 1:
                return tuning_frequency(helpers.pos2d(m_r[0][1] + 1, col))
    return None


def solve(s: str, n: int) -> int:
    lines = s.splitlines()
    rhombuses: set[Rhombus] = set()
    for line in lines:
        ma = INPUT_RE.fullmatch(line)
        assert ma, line
        x_s, y_s, x_b, y_b = map(int, ma.groups())
        distance = abs(x_s - x_b) + abs(y_s - y_b)
        rhombuses.add(Rhombus(helpers.pos2d(x_s, y_s), distance))

    for i in range(n):
        a = solve_for_row(rhombuses, i)
        if a is not None:
            return a
    raise Exception("we didn't find a solution?")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=os.path.join(THIS_DIR, "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read(), 4000001))

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
    ("s", "n", "expected"),
    (
        (INPUT_S, 21, 56000011),
        (
            helpers.read_file(os.path.join(THIS_DIR, "input.txt")),
            4000001,
            13360899249595,
        ),
    ),
)
def test(s: str, n: int, expected: int) -> None:
    assert solve(s, n) == expected


if __name__ == "__main__":
    raise SystemExit(main())
