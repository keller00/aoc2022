from __future__ import annotations

import argparse
import os.path

import pytest

import helpers

THIS_DIR = os.path.dirname(__file__)


def solve(s: str) -> str:
    board_s, _, movements = s.partition("\n\n")
    board_lines = board_s.splitlines()
    board: list[list[str]] = [list() for _ in board_lines.pop().split()]

    for line in reversed(board_lines):
        for i in range(len(board)):
            loc = i * 4 + 1
            if loc < len(line):
                ch = line[loc]
                if ch != " ":
                    board[i].append(ch)
    for m in movements.splitlines():
        _, amount, _, from_, _, to = m.split()
        for _ in range(int(amount)):
            board[int(to) - 1].append(board[int(from_) - 1].pop())

    return "".join([c.pop() for c in board])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=os.path.join(THIS_DIR, "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


INPUT_S = '''\
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''
EXPECTED = "CMZ"


@pytest.mark.parametrize(
    ("s", "expected"),
    (
        (INPUT_S, EXPECTED),
        (helpers.read_file(os.path.join(THIS_DIR, "input.txt")), "JRVNHHCSJ"),
    ),
)
def test(s: str, expected: int) -> None:
    assert solve(s) == expected


if __name__ == "__main__":
    raise SystemExit(main())
