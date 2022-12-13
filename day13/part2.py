from __future__ import annotations

import argparse
import json
import os.path
from functools import cmp_to_key

import pytest

import helpers

THIS_DIR = os.path.dirname(__file__)

intOrList = int | list["intOrList"]


def right_order(lhs: intOrList, rhs: intOrList) -> bool | None:
    if isinstance(lhs, int) and isinstance(rhs, int):
        if lhs < rhs:
            return True
        elif lhs > rhs:
            return False
        return None
    elif isinstance(lhs, list) and isinstance(rhs, list):
        for left, right in zip(lhs, rhs):
            order_good = right_order(left, right)
            if order_good is not None:
                return order_good
        if len(lhs) < len(rhs):
            return True
        elif len(rhs) < len(lhs):
            return False
        return None
    else:
        lhs_l: intOrList = [lhs, ] if isinstance(lhs, int) else lhs
        rhs_l: intOrList = [rhs, ] if isinstance(rhs, int) else rhs
        return right_order(lhs_l, rhs_l)


def right_order_cmp(lhs: intOrList, rhs: intOrList) -> int:
    order = right_order(lhs, rhs)
    if order is None:
        return 0
    if order is True:
        return -1
    else:
        return 1


def solve(s: str) -> int:
    lines = list(map(json.loads, filter(lambda e: e != "", s.splitlines())))
    start = [[2]]
    end = [[6]]
    lines.append(start)
    lines.append(end)
    lines = sorted(lines, key=cmp_to_key(right_order_cmp))
    # for j in range(0, len(lines) - 1, -1, -1):
    #     for k in range(1, len(lines)):
    #         if not right_order(lines[j], lines[k]):
    #             lines[j], lines[k] = lines[k], lines[j]
    return (lines.index(start) + 1) * (lines.index(end) + 1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=os.path.join(THIS_DIR, "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


INPUT_S = '''\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
'''
EXPECTED = 140


@pytest.mark.parametrize(
    ("s", "expected"),
    (
        (INPUT_S, EXPECTED),
        (helpers.read_file(os.path.join(THIS_DIR, "input.txt")), 19570),
    ),
)
def test(s: str, expected: int) -> None:
    assert solve(s) == expected


if __name__ == "__main__":
    raise SystemExit(main())
