from __future__ import annotations

import argparse
import os.path

import pytest

import helpers

THIS_DIR = os.path.dirname(__file__)


def score(s: str) -> int:
    if "a" <= s <= "z":
        return ord(s) - ord("a") + 1
    elif "A" <= s <= "Z":
        return ord(s) - ord("A") + 27
    else:
        raise Exception(f"{s} is not expected")


def solve(s: str) -> int:
    lines = s.splitlines()
    overall = 0
    for line in lines:
        left, right = set(line[: int(len(line) / 2)]
                          ), set(line[int(len(line) / 2):])
        common = left & right
        for e in common:
            overall += score(e)

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
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
'''
EXPECTED = 157


@pytest.mark.parametrize(
    ("s", "expected"),
    (
        (INPUT_S, EXPECTED),
        (helpers.read_file(os.path.join(THIS_DIR, "input.txt")), 7872),
    ),
)
def test(s: str, expected: int) -> None:
    assert solve(s) == expected


if __name__ == "__main__":
    raise SystemExit(main())
