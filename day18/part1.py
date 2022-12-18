from __future__ import annotations

import argparse
import os.path

import pytest

import helpers
from helpers import pos3d

THIS_DIR = os.path.dirname(__file__)


def solve(s: str) -> int:
    exposed_sides = 0
    droplets: list[pos3d] = list()
    for line in s.splitlines():
        droplets.append(pos3d(*map(int, line.split(","))))

    for d in droplets:
        for n in helpers.adjacent_6(d):
            if n not in droplets:
                exposed_sides += 1

    return exposed_sides


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=os.path.join(THIS_DIR, "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


INPUT_S = '''\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
'''
EXPECTED = 64


@pytest.mark.parametrize(
    ("s", "expected"),
    (
        (INPUT_S, EXPECTED),
        (helpers.read_file(os.path.join(THIS_DIR, "input.txt")), 4282),
    ),
)
def test(s: str, expected: int) -> None:
    assert solve(s) == expected


if __name__ == "__main__":
    raise SystemExit(main())
