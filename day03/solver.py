import string
from runner_utils import expected_test_result

PRIORITY_INDEX = string.printable[9:]


@expected_test_result(157)
def solve1(input):
    priority_sum = 0
    for backpack in input.strip().split("\n"):
        size = len(backpack) // 2
        compartment1 = backpack[:size]
        compartment2 = backpack[size:]
        wrong_item, = set(compartment1).intersection(compartment2)
        priority_sum += PRIORITY_INDEX.index(wrong_item)
    return priority_sum


@expected_test_result(70)
def solve2(input):
    backpacks = input.strip().split("\n")
    priority_sum = 0
    while backpacks:
        common = set(backpacks.pop(0)).intersection(backpacks.pop(0))
        badge_priority, = common.intersection(backpacks.pop(0))
        priority_sum += PRIORITY_INDEX.index(badge_priority)
    return priority_sum
