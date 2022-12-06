from runner_utils import expected_test_result

import re

REGEX = r"move (\d+) from (\d+) to (\d+)"
CONTAINER_WIDTH = 4
CONTENT_INDEX = 1


def parse_stacks(raw_stacks):
    stack_amount = (len(raw_stacks[0]) + 1) // CONTAINER_WIDTH
    stacks = [[] for _ in range(stack_amount)]
 
    for line in raw_stacks:
        for idx, stack in enumerate(stacks):
            start = idx * CONTAINER_WIDTH
            end = (idx + 1) * CONTAINER_WIDTH
            content = line[start:end][CONTENT_INDEX]
            if content == " ":
                continue
            stack.insert(0, content)
    return stacks


def execute_instruction_9000(stacks, instruction):
    move, from_, to_ = map(int, re.match(REGEX, instruction).groups())
    while move:
        stacks[to_ - 1].append(stacks[from_ - 1].pop(-1))
        move -= 1


def execute_instruction_9001(stacks, instruction):
    move, from_, to_ = map(int, re.match(REGEX, instruction).groups())
    stacks[to_ - 1].extend(stacks[from_ - 1][move * -1 :])
    stacks[from_ - 1] = stacks[from_ - 1][: move * -1]


def move_stacks(input, do_move):
    stacks, instructions = input.strip().split("\n\n")
    stacks = parse_stacks(stacks.split("\n")[:-1])

    for instruction in instructions.split("\n"):
        do_move(stacks, instruction)

    return "".join([s[-1] for s in stacks])


@expected_test_result("CMZ")
def solve1(input):
    return move_stacks(input, execute_instruction_9000)


@expected_test_result("MCD")
def solve2(input):
    return move_stacks(input, execute_instruction_9001)
