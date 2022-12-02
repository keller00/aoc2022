from __future__ import annotations

import argparse
import os.path
from typing import Literal

import pytest

import helpers

THIS_DIR = os.path.dirname(__file__)

move = Literal["scissors", "rock", "paper"]

moves: dict[str, move] = {
    "A": "rock",
    "B": "paper",
    "C": "scissors",
}

reactions: dict[str, move] = {
    "X": "rock",
    "Y": "paper",
    "Z": "scissors",
}

score: dict[move, int] = {
    "rock": 1,
    "paper": 2,
    "scissors": 3,
}
# 0 if lost
# 3 if draw
# 6 if won


def calculate_score(enemy: move, me: move) -> int:
    if enemy == me:
        return score[me] + 3
    outcomes = {
        # enemy, me
        ("rock", "paper"): 6,
        ("rock", "scissors"): 0,
        ("paper", "scissors"): 6,
        ("paper", "rock"): 0,
        ("scissors", "paper"): 0,
        ("scissors", "rock"): 6,
    }
    return outcomes[(enemy, me)] + score[me]


def solve(s: str) -> int:
    lines = s.splitlines()
    total_score = 0
    for line in lines:
        enemy, outcome = line.split(" ", 1)
        enemy_move = moves[enemy]
        # X lose
        # Y draw
        # Z win
        suggested_moves: dict[tuple[move, str], move] = {
            ("rock", "X"): "scissors",
            ("rock", "Y"): "rock",
            ("rock", "Z"): "paper",
            ("paper", "X"): "rock",
            ("paper", "Y"): "paper",
            ("paper", "Z"): "scissors",
            ("scissors", "X"): "paper",
            ("scissors", "Y"): "scissors",
            ("scissors", "Z"): "rock",
        }
        suggested_move = suggested_moves[(enemy_move, outcome)]
        total_score += calculate_score(enemy_move, suggested_move)
    return total_score


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=os.path.join(THIS_DIR, "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


INPUT_S = '''\
A Y
B X
C Z
'''
EXPECTED = 12


@pytest.mark.parametrize(
    ("s", "expected"),
    (
        (INPUT_S, EXPECTED),
        (helpers.read_file(os.path.join(THIS_DIR, "input.txt")), 11186),
    ),
)
def test(s: str, expected: int) -> None:
    assert solve(s) == expected


if __name__ == "__main__":
    raise SystemExit(main())
