from __future__ import annotations

import argparse
import os.path

import pytest

import helpers

THIS_DIR = os.path.dirname(__file__)


def score(
    board: dict[tuple[int, int], int],
    width: int,
    height: int,
    x_c: int,
    y_c: int,
) -> int:
    tree_height = board[(x_c, y_c)]
    v_above = 0
    for y in range(y_c - 1, -1, -1):
        v_above += 1
        if board[(x_c, y)] >= tree_height:
            break
    v_below = 0
    for y in range(y_c + 1, height):
        v_below += 1
        if board[(x_c, y)] >= tree_height:
            break
    v_left = 0
    for x in range(x_c - 1, -1, -1):
        v_left += 1
        if board[(x, y_c)] >= tree_height:
            break
    v_right = 0
    for x in range(x_c + 1, width):
        v_right += 1
        if board[(x, y_c)] >= tree_height:
            break
    return v_above * v_right * v_left * v_below


def solve(s: str) -> int:
    visible_trees = 0
    board, width, height = helpers.parse_coords_int(s)
    visible_trees += 2 * height
    visible_trees += 2 * (width - 2)
    max_score = 0
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            max_score = max(max_score, score(board, width, height, x, y))

    return max_score


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=os.path.join(THIS_DIR, "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 8


@pytest.mark.parametrize(
    ("s", "expected"),
    (
        (INPUT_S, EXPECTED),
        (helpers.read_file(os.path.join(THIS_DIR, "input.txt")), 392080),
    ),
)
def test(s: str, expected: int) -> None:
    assert solve(s) == expected


if __name__ == "__main__":
    raise SystemExit(main())
