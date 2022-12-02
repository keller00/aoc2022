from __future__ import annotations

import argparse
import os.path

import pytest

import helpers


THIS_DIR = os.path.dirname(__file__)


def solve(s: str) -> int:
    lines = s.splitlines()
    elves = []
    current_elf = 0
    for line in lines:
        if line == "":
            elves.append(current_elf)
            current_elf = 0
        else:
            current_elf += int(line)

    return max(elves)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=os.path.join(THIS_DIR, "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


INPUT_S = '''\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
'''
EXPECTED = 24000


@pytest.mark.parametrize(
    ("s", "expected"),
    (
        (INPUT_S, EXPECTED),
        (helpers.read_file(os.path.join(THIS_DIR, "input.txt")), 69310),
    ),
)
def test(s: str, expected: int) -> None:
    assert solve(s) == expected


if __name__ == "__main__":
    raise SystemExit(main())
