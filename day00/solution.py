from __future__ import annotations

import argparse
import os.path

import pytest

import helpers

THIS_DIR = os.path.dirname(__file__)


def solve(s: str) -> int:
    numbers = helpers.parse_numbers_split(s)
    solution = 0

    for n in numbers:
        ...

    return solution


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=os.path.join(THIS_DIR, "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


INPUT_S = '''\

'''
EXPECTED = 1


@pytest.mark.parametrize(
    ("s", "expected"),
    (
        (INPUT_S, EXPECTED),
        # (helpers.read_file(os.path.join(THIS_DIR, "input.txt")), solution),
    ),
)
def test(s: str, expected: int) -> None:
    assert solve(s) == expected


if __name__ == "__main__":
    raise SystemExit(main())
