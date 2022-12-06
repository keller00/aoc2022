from __future__ import annotations

import argparse
import os.path
from collections import deque

import pytest

import helpers

THIS_DIR = os.path.dirname(__file__)


def solve(s: str) -> int:
    lines = s.splitlines()
    for line in lines:
        marker: deque[str] = deque()
        for i, c in enumerate(line):
            marker.append(c)
            if len(marker) == 4:
                if len(set(marker)) == 4:
                    return i + 1
                marker.popleft()
    raise Exception("No message found")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=os.path.join(THIS_DIR, "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


INPUT_S = '''\
mjqjpqmgbljsphdztnvjfqwrcgsmlb
'''
EXPECTED = 7


@pytest.mark.parametrize(
    ("s", "expected"),
    (
        (INPUT_S, EXPECTED),
        ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5),
        ("nppdvjthqldpwncqszvftbrmjlhg", 6),
        ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10),
        ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11),
        (helpers.read_file(os.path.join(THIS_DIR, "input.txt")), 1640),
    ),
)
def test(s: str, expected: int) -> None:
    assert solve(s) == expected


if __name__ == "__main__":
    raise SystemExit(main())
