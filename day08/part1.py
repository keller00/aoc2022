from __future__ import annotations

import argparse
import os.path

import pytest

import helpers

THIS_DIR = os.path.dirname(__file__)


def is_visible(
    board: dict[tuple[int, int], int],
    width: int,
    height: int,
    x_c: int,
    y_c: int,
) -> bool:
    tree_height = board[(x_c, y_c)]
    v_above = True
    for y in range(y_c - 1, -1, -1):
        if board[(x_c, y)] >= tree_height:
            v_above = False
    v_below = True
    for y in range(y_c + 1, height):
        if board[(x_c, y)] >= tree_height:
            v_below = False
    v_left = True
    for x in range(x_c - 1, -1, -1):
        if board[(x, y_c)] >= tree_height:
            v_left = False
    v_right = True
    for x in range(x_c + 1, width):
        if board[(x, y_c)] >= tree_height:
            v_right = False
    return v_above or v_right or v_left or v_below


def solve(s: str) -> int:
    visible_trees = 0
    board, width, height = helpers.parse_coords_int(s)
    visible_trees += 2 * height
    visible_trees += 2 * (width - 2)
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if is_visible(board, width, height, x, y):
                visible_trees += 1

    return visible_trees


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
EXPECTED = 21


@pytest.mark.parametrize(
    ("s", "expected"),
    (
        (INPUT_S, EXPECTED),
        (helpers.read_file(os.path.join(THIS_DIR, "input.txt")), 1647),
    ),
)
def test(s: str, expected: int) -> None:
    assert solve(s) == expected


if __name__ == "__main__":
    raise SystemExit(main())
