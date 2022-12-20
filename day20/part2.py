from __future__ import annotations

import argparse
import os.path
from collections import deque
from itertools import cycle
from typing import Iterable

import pytest

import helpers

THIS_DIR = os.path.dirname(__file__)


def get_index_of(it: Iterable[int], looking_for: int) -> int:
    for i, e in enumerate(it):
        if e == looking_for:
            return i
    raise Exception("should have never reached this")


def solve(s: str) -> int:
    numbers = helpers.parse_numbers_split(s)
    nums = deque(map(lambda e: e * 811589153, numbers))
    indexes = deque([i for i in range(len(numbers))])
    for _ in range(10):
        current_index = 0
        while current_index < len(nums):
            swapping = get_index_of(indexes, current_index)
            for _ in range(swapping):
                nums.append(nums.popleft())
                indexes.append(indexes.popleft())
            num = nums.popleft()
            index = indexes.popleft()
            assert index == current_index, index
            if num > 0:
                for _ in range(num % (len(numbers) - 1)):
                    nums.append(nums.popleft())
                    indexes.append(indexes.popleft())
            elif num < 0:
                for _ in range(abs(num) % (len(numbers) - 1)):
                    nums.appendleft(nums.pop())
                    indexes.appendleft(indexes.pop())
            nums.appendleft(num)
            indexes.appendleft(index)
            current_index += 1
    while nums[0] != 0:
        nums.append(nums.popleft())
    nums.append(nums.popleft())
    answer = 0
    for i, n in enumerate(cycle(nums)):
        if i == 3000:
            break
        if i % 1000 == 999:
            answer += n

    return answer


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=os.path.join(THIS_DIR, "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


INPUT_S = '''\
1
2
-3
3
-2
0
4
'''
EXPECTED = 1623178306


@pytest.mark.parametrize(
    ("s", "expected"),
    (
        (INPUT_S, EXPECTED),
        (
            helpers.read_file(os.path.join(THIS_DIR, "input.txt")),
            9995532008348,
        ),
    ),
)
def test(s: str, expected: int) -> None:
    assert solve(s) == expected


if __name__ == "__main__":
    raise SystemExit(main())
