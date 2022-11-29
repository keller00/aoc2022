# Advent of code 2022 solutions

My solutions for https://adventofcode.com/2022

All `part1.py`s and `part2.py`s are what I used to submit my solutions. Some days I might sacrifice readability for
speed if I feel like I could be competitive, while on some days I might just take my time from the beginning for better
design.

In some cases when I feel like I want to take a different approach later I will rewrite my solutions, these will be
obviously labeled.

## Workflow

1. `cp -r day00 dayNN` start by copying the folder `day00`, it serves as a template for new days
2. `cd dayNN`
3. `aoc-download-input`
4. `python solution.py | aoc-submit --part 1`
5. `cp solution.py part1.py` once the solution is finalized for part 1, save it as `part1.py` and keep working on
   `solution.py`
6. `python solution.py | aoc-submit --part 2`
7. `mv solution.py part2.py` once the solution is finished for part 2
