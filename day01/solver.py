from runner_utils import expected_test_result


@expected_test_result(24000)
def solve1(input):
    current_backpack = 0
    max_calories = 0
    for backpack in input.split('\n\n'):
        calories = sum(map(int, [f for f in backpack.split("\n") if f]))
        max_calories = max(max_calories, calories)
    return max_calories


@expected_test_result(45000)
def solve2(input):
    current_backpack = 0
    max_calories = []
    for backpack in input.split('\n\n'):
        calories = sum(map(int, [f for f in backpack.split("\n") if f]))
        if len(max_calories) < 3:
            max_calories.append(calories)
        else:
            lowest = min(*max_calories)
            highest = max(lowest, calories)
            if lowest != highest:
                max_calories.remove(lowest)
                max_calories.append(highest)
    return sum(max_calories)
