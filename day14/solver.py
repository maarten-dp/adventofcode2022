from runner_utils import expected_test_result

SPAWN = (500, 0)


def to_coordinates(raw_coordinates):
    return list(map(int, raw_coordinates.split(",")))


def populate_line(line, occupied_spaces):
    coordinates = list(map(to_coordinates, line.split(" -> ")))
    lowest_y = 0
    for (from_x, from_y), (to_x, to_y) in zip(coordinates, coordinates[1:]):
        if from_x == to_x:
            from_y, to_y = sorted([from_y, to_y])
            [occupied_spaces.add((from_x, y)) for y in range(from_y, to_y + 1)]
        else:
            from_x, to_x = sorted([from_x, to_x])
            [occupied_spaces.add((x, from_y)) for x in range(from_x, to_x + 1)]
        lowest_y = max([lowest_y, from_y, to_y])
    return lowest_y


def populate(input):
    lines = input.strip().splitlines()
    lowest_y = 0
    occupied_spaces = set()
    for line in lines:
        lowest_y = max(lowest_y, populate_line(line, occupied_spaces))
    return lowest_y, occupied_spaces


def move(x, y, occupied_spaces):
    for x_offset in (0, -1, 1):
        if (x + x_offset, y + 1) not in occupied_spaces:
            return False, (x + x_offset, y + 1)
    occupied_spaces.add((x, y))
    return True, (x, y)


def simulate_abyss(lowest_y, occupied_spaces):
    x, y = SPAWN
    is_resting = False
    while not is_resting:
        if y + 1 > lowest_y:
            return False
        is_resting, (x, y) = move(x, y, occupied_spaces)
    return True


def simulate_floor(lowest_y, occupied_spaces):
    x, y = SPAWN
    is_resting = False
    while not is_resting:
        if y + 1 == lowest_y + 2:
            occupied_spaces.add((x, y))
            return True
        is_resting, (x, y) = move(x, y, occupied_spaces)
        if (x, y) == SPAWN:
            return False
    return True


@expected_test_result(24)
def solve1(input):
    lowest_y, occupied_spaces = populate(input)

    i = 0
    while simulate_abyss(lowest_y, occupied_spaces):
        i += 1
    return i


@expected_test_result(93)
def solve2(input):
    lowest_y, occupied_spaces = populate(input)

    i = 1
    while simulate_floor(lowest_y, occupied_spaces):
        i += 1
    return i
