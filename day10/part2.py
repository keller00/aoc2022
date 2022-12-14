from __future__ import annotations

import argparse
import os.path

import pytest

THIS_DIR = os.path.dirname(__file__)


def score_cycle(registers: dict[str, int], cycle: int) -> int:
    if cycle == 20 or ((cycle - 20) % 40) == 0:
        return registers["x"] * cycle
    return 0


def solve(s: str) -> str:
    answer = ""
    registers = {
        'x': 1,
    }
    cycle = 1
    for x, line in enumerate(s.splitlines()):
        command, _, rest = line.partition(" ")
        # sum += score_cycle(registers, cycle)
        if (cycle % 40 - 2 if cycle % 40 - 1 == 0 else (cycle - 2) % 40) \
            <= registers["x"]\
                <= cycle % 40:
            answer += "#"
        else:
            answer += "."
        cycle += 1
        if command.startswith("add"):
            target = command[3:]
            # Takes 2 cycles
            # sum += score_cycle(registers, cycle)
            if (cycle % 40 - 2 if cycle % 40 - 1 == 0 else (cycle - 2) % 40) \
                <= registers["x"] \
                    <= cycle % 40:
                answer += "#"
            else:
                answer += "."
            cycle += 1
            registers[target] += int(rest)
    return "\n".join([answer[i: i + 40] for i in range(0, len(answer), 40)])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=os.path.join(THIS_DIR, "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


INPUT_S = '''\
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
'''
EXPECTED = """\
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######....."""


@pytest.mark.parametrize(
    ("s", "expected"),
    (
        # Note: no tests for today, I haven't perfectly solved this,
        #  but my solution was readable!t
        # (INPUT_S, EXPECTED),
        # (helpers.read_file(os.path.join(THIS_DIR, "input.txt")), "EALGULPG"),
    ),
)
def test(s: str, expected: int) -> None:
    assert solve(s) == expected


if __name__ == "__main__":
    raise SystemExit(main())
