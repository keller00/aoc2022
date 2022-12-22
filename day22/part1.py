from __future__ import annotations

import argparse
import enum
import os.path
import re
from typing import Literal

import pytest

import helpers

THIS_DIR = os.path.dirname(__file__)
STEPS_RE = re.compile(r"(\d+)([LR])")
SINGLE_MOVE_END_RE = re.compile(r"(\d+)$")
previous_posns: list[tuple[helpers.pos2d, facing]] = list()


class facing(enum.Enum):
    right = 0
    down = 1
    left = 2
    up = 3


def move_if_can(
    open_tiles: set[helpers.pos2d],
    walls: set[helpers.pos2d],
    pos: helpers.pos2d,
    face: facing,
    number: int,
    letter: Literal['L', 'R'] | None,
) -> tuple[helpers.pos2d, facing]:
    if face == facing.right:
        for _ in range(number):
            new_pos = pos._replace(x=pos.x + 1)
            if new_pos not in walls and new_pos not in open_tiles:
                new_pos = pos._replace(
                    x=min(t.x for t in (walls | open_tiles) if t.y == pos.y))
            if new_pos in open_tiles:
                pos = new_pos
                previous_posns.append((pos, face))
            elif new_pos in walls:
                break
            else:
                raise Exception(f"oh no {new_pos}")
        if letter is None:
            return pos, face
        elif letter == "L":
            return pos, facing.up
        else:
            return pos, facing.down
    elif face == facing.down:
        for _ in range(number):
            new_pos = pos._replace(y=pos.y + 1)
            if new_pos not in walls and new_pos not in open_tiles:
                new_pos = pos._replace(
                    y=min(t.y for t in (walls | open_tiles) if t.x == pos.x))
            if new_pos in open_tiles:
                pos = new_pos
                previous_posns.append((pos, face))
            elif new_pos in walls:
                break
            else:
                raise Exception(f"oh no {new_pos}")
        if letter is None:
            return pos, face
        elif letter == "L":
            return pos, facing.right
        else:
            return pos, facing.left
    elif face == facing.left:
        for _ in range(number):
            new_pos = pos._replace(x=pos.x - 1)
            if new_pos not in walls and new_pos not in open_tiles:
                new_pos = pos._replace(
                    x=max(t.x for t in (walls | open_tiles) if t.y == pos.y))
            if new_pos in open_tiles:
                pos = new_pos
                previous_posns.append((pos, face))
            elif new_pos in walls:
                break
            else:
                raise Exception(f"oh no {new_pos}")
        if letter is None:
            return pos, face
        elif letter == "L":
            return pos, facing.down
        else:
            return pos, facing.up
    elif face == facing.up:
        for _ in range(number):
            new_pos = pos._replace(y=pos.y - 1)
            if new_pos not in walls and new_pos not in open_tiles:
                new_pos = pos._replace(
                    y=max(t.y for t in (walls | open_tiles) if t.x == pos.x))
            if new_pos in open_tiles:
                pos = new_pos
                previous_posns.append((pos, face))
            elif new_pos in walls:
                break
            else:
                raise Exception(f"oh no {new_pos}")
        if letter is None:
            return pos, face
        elif letter == "L":
            return pos, facing.left
        else:
            return pos, facing.right
    return pos, face


def solve(s: str) -> int:
    board_s, path = s.split("\n\n")
    open_tiles = helpers.parse_coords_symbol(board_s, '.')
    walls = helpers.parse_coords_hash(board_s)

    pos = sorted(t for t in open_tiles if t.y == 0)[0]
    face = facing.right

    previous_posns.append((pos, face))
    for number, letter in STEPS_RE.findall(path):
        assert letter in ('L', 'R')
        pos, face = move_if_can(open_tiles, walls, pos,
                                face, int(number), letter)
        previous_posns.append((pos, face))
    single_forward = SINGLE_MOVE_END_RE.search(path)
    if single_forward:
        pos, face = move_if_can(open_tiles, walls, pos,
                                face, int(single_forward.group(1)), None)

    board_to_print = board_s.splitlines()
    for pos_b, face_b in previous_posns:
        if face_b == facing.right:
            icon = '>'
        elif face_b == facing.down:
            icon = 'v'
        elif face_b == facing.left:
            icon = '<'
        elif face_b == facing.up:
            icon = '^'
        board_to_print[pos_b.y] = ''.join(
            [
                board_to_print[pos_b.y][:pos_b.x],
                icon,
                board_to_print[pos_b.y][pos_b.x + 1:],
            ])
    for line in board_to_print:
        print(line)
    return (pos.y + 1) * 1000 + (pos.x + 1) * 4 + face.value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=os.path.join(THIS_DIR, "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


INPUT_S = '''\
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
'''
EXPECTED = 6032


@pytest.mark.parametrize(
    ("s", "expected"),
    (
        (INPUT_S, EXPECTED),
        (helpers.read_file(os.path.join(THIS_DIR, "input.txt")), 117102),
    ),
)
def test(s: str, expected: int) -> None:
    assert solve(s) == expected


if __name__ == "__main__":
    raise SystemExit(main())
