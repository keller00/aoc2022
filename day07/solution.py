from __future__ import annotations

import argparse
import os.path
from collections import deque
from typing import Any

import pytest

import helpers

THIS_DIR = os.path.dirname(__file__)


def solve(s: str) -> int:
    answer = 0
    disk: dict[str, dict[str, Any]] = {}
    lines = s.splitlines()
    cwd: list[str] = []
    for line in lines:
        if line.startswith("$"):
            # process command
            l = line.lstrip("$ ")
            if " " in l:
                cmd, rest = l.split(" ", 1)
            else:
                cmd = l
            if cmd == "cd":
                if rest == "..":
                    cwd = cwd[:-1]
                elif rest == "/":
                    cwd = list()
                else:
                    cwd.append(rest)
        else:
            this = disk
            if len(cwd) > 0:
                this = disk[cwd[0]]
            for p in cwd[1:]:
                this = this[p]
            size, name = line.split(maxsplit=1)
            if size == "dir":
                this[name] = {}
            else:
                this[name] = int(size)

    directories = list()

    def calculate_folder_size(e: int | dict[str, int | dict[str, Any]]) -> int:
        nonlocal answer
        if isinstance(e, int):
            return e
        else:
            a = 0
            for f in e:
                a += calculate_folder_size(e[f])
            if a < 100000:
                answer += a
            directories.append(a)
            return a
    overall_space = 70000000
    needed = 30000000 - (overall_space - calculate_folder_size(disk))
    for e in sorted(directories):
        if e > needed:
            return e
    raise Exception("fell off?")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=os.path.join(THIS_DIR, "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


INPUT_S = '''\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''
EXPECTED = 24933642


@pytest.mark.parametrize(
    ("s", "expected"),
    (
        (INPUT_S, EXPECTED),
        (helpers.read_file(os.path.join(THIS_DIR, "input.txt")), 3866390),
    ),
)
def test(s: str, expected: int) -> None:
    assert solve(s) == expected


if __name__ == "__main__":
    raise SystemExit(main())
