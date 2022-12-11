from __future__ import annotations

import argparse
import operator
import os.path
from collections import deque
from typing import Callable

import pytest

import helpers

THIS_DIR = os.path.dirname(__file__)


class Monkey:

    def __init__(
        self,
        num: int,
        items: list[int],
        operation: Callable[[int, int], int],
        operation_num: str,
        test: Callable[[int, int], bool],
        test_num: int,
        true_throw: int,
        false_throw: int,
    ):
        self.num = num
        self.items = deque(items)
        self.operation = operation
        self.operation_num = operation_num
        self.test = test
        self.test_num = test_num
        self.true_throw = true_throw
        self.false_throw = false_throw
        self.inspected_items = 0

    def do_turn(self, monkeys: dict[int, Monkey]) -> None:
        while self.items:
            i = self.items.popleft()
            new_i = self.operation(
                i,
                int(self.operation_num) if self.operation_num != "old" else i,
            )
            new_i = new_i // 3
            give_to = self.true_throw if self.test(
                new_i, self.test_num) == 0 else self.false_throw
            monkeys[give_to].items.append(new_i)
            self.inspected_items += 1


def solve(s: str) -> int:
    monkeys: dict[int, Monkey] = dict()
    monkey_lines = s.split("\n\n")
    for monkey_desc in monkey_lines:
        lines = monkey_desc.splitlines()
        number = int(lines[0][:-1].split(" ", 1)[1])
        items = list(map(int, lines[1].partition(": ")[2].split(", ")))
        operator_action, operator_num = lines[2].split()[-2:]
        if operator_action == "+":
            operation = operator.add
        elif operator_action == "*":
            operation = operator.mul
        else:
            raise Exception(f"what is {operator_action}")

        test_action, _, test_num = lines[3].split()[1: 4]
        if test_action == "divisible":
            test = operator.mod
        else:
            raise Exception(f"what is {test_action}")
        true_throw = int(lines[4].split()[-1])
        false_throw = int(lines[5].split()[-1])
        monkey = Monkey(
            number,
            items,
            operation,
            operator_num,
            test,
            int(test_num),
            true_throw,
            false_throw,
        )
        monkeys[number] = monkey
    for _ in range(20):
        for m in monkeys.values():
            m.do_turn(monkeys)
    monkeys_inspected = sorted(
        [m.inspected_items for m in monkeys.values()], reverse=True)
    return monkeys_inspected[0] * monkeys_inspected[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=os.path.join(THIS_DIR, "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


INPUT_S = '''\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
'''
EXPECTED = 10605


@pytest.mark.parametrize(
    ("s", "expected"),
    (
        (INPUT_S, EXPECTED),
        (helpers.read_file(os.path.join(THIS_DIR, "input.txt")), 113220),
    ),
)
def test(s: str, expected: int) -> None:
    assert solve(s) == expected


if __name__ == "__main__":
    raise SystemExit(main())
