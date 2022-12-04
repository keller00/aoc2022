from __future__ import annotations

import argparse
import os.path

import pytest

import helpers

THIS_DIR = os.path.dirname(__file__)


def solve(s: str) -> int:
    lines = s.splitlines()
    overall = 0
    for line in lines:
        lhs, rhs = line.split(",", 1)
        lhs_start, lhs_end = map(int, lhs.split("-", 1))
        rhs_start, rhs_end = map(int, rhs.split("-", 1))
        lhs_set = set(range(lhs_start, lhs_end + 1))
        rhs_set = set(range(rhs_start, rhs_end + 1))
        if lhs_set & rhs_set:
            overall += 1

    return overall


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=os.path.join(THIS_DIR, "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


INPUT_S = '''\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
'''
EXPECTED = 4


@pytest.mark.parametrize(
    ("s", "expected"),
    (
        (INPUT_S, EXPECTED),
        (helpers.read_file(os.path.join(THIS_DIR, "input.txt")), 825),
    ),
)
def test(s: str, expected: int) -> None:
    assert solve(s) == expected


if __name__ == "__main__":
    raise SystemExit(main())
