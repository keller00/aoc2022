from __future__ import annotations

import argparse
import os.path
from collections import deque

import pytest

import helpers
from helpers import pos3d

THIS_DIR = os.path.dirname(__file__)


def flod(
    p: pos3d,
    droplets: set[pos3d],
    max_size: tuple[
        tuple[int, int],
        tuple[int, int],
        tuple[int, int],
    ],
) -> bool:
    to_be_checked = deque([p])
    seen: set[pos3d] = set()
    while to_be_checked:
        checking = to_be_checked.popleft()
        seen.add(checking)
        for n in helpers.adjacent_6(checking):
            if (
                n.x < max_size[0][0]
                or n.x > max_size[0][1]
                or n.y < max_size[1][0]
                or n.y > max_size[1][1]
                or n.z < max_size[2][0]
                or n.z > max_size[2][1]
            ):
                break
            if n not in droplets and n not in seen:
                seen.add(n)
                to_be_checked.append(n)
        else:
            continue
        break

    else:
        return False
    return True


def solve(s: str) -> int:
    exposed_sides = 0
    droplets: set[pos3d] = set()
    for line in s.splitlines():
        droplets.add(pos3d(*map(int, line.split(","))))

    droplets_x = [d.x for d in droplets]
    droplets_y = [d.y for d in droplets]
    droplets_z = [d.z for d in droplets]
    volume = (
        (min(droplets_x), max(droplets_x)),
        (min(droplets_y), max(droplets_y)),
        (min(droplets_z), max(droplets_z)),
    )

    for d in droplets:
        for n in helpers.adjacent_6(d):
            if n not in droplets:
                just_saw = flod(n, droplets, volume)
                if just_saw:
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
EXPECTED = 58


@pytest.mark.parametrize(
    ("s", "expected"),
    (
        (INPUT_S, EXPECTED),
        (helpers.read_file(os.path.join(THIS_DIR, "input.txt")), 2452),
    ),
)
def test(s: str, expected: int) -> None:
    assert solve(s) == expected


if __name__ == "__main__":
    raise SystemExit(main())
