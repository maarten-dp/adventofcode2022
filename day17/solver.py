from copy import deepcopy
from runner_utils import expected_test_result


SHAPE1 = [[0, 0], [1, 0], [2, 0], [3, 0]]
SHAPE2 = [[0, 1], [1, 0], [1, 1], [1, 2], [2, 1]]
SHAPE3 = [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2]]
SHAPE4 = [[0, 0], [0, 1], [0, 2], [0, 3]]
SHAPE5 = [[0, 0], [1, 0], [0, 1], [1, 1]]

ROUNDS = 1000000000000

MOVES = {
    ">": (1, 0),
    "<": (-1, 0),
    "v": (0, -1)
}

class InfiniteList(list):
    def __getitem__(self, index):
        index %= len(self)
        return list.__getitem__(self, index)


class Rock:
    def __init__(self, shape, bottom):
        self.shape = deepcopy(shape)
        self.left_most = self.shape[0]
        self.right_most = self.shape[-1]
        self._move(2, bottom + 4)

    def move(self, move, floor):
        x_mod, y_mod = MOVES[move]
        if self.left_most[0] + x_mod < 0:
            return True
        if self.right_most[0] + x_mod >= 7:
            return True
        if self.collides(x_mod, y_mod, floor):
            if move == "v":
                return False
            return True
        self._move(x_mod, y_mod)
        return True

    def _move(self, x_mod, y_mod):
        for coords in self.shape:
            coords[0] = coords[0] + x_mod
            coords[1] = coords[1] + y_mod

    def collides(self, x_mod, y_mod, floor):
        next_move = set([(x + x_mod, y + y_mod) for x, y in self.shape])
        return bool(next_move.intersection(floor))


@expected_test_result(3068)
def solve1(input):
    stream = InfiniteList(input.strip())
    rocks = InfiniteList([SHAPE1, SHAPE2, SHAPE3, SHAPE4, SHAPE5])
    floor = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)]

    stream_idx = 0
    rock_idx = 0
    current_bottom = 0
    for rock_idx in range(2022):
        print(rock_idx)
        rock = Rock(rocks[rock_idx], current_bottom)
        rock.move(stream[stream_idx], floor)
        while rock.move("v", floor) :
            stream_idx += 1
            rock.move(stream[stream_idx], floor)
        stream_idx += 1
        for _, y in rock.shape:
            current_bottom = max(current_bottom, y)
        floor.extend([(x, y) for x, y in rock.shape])
    return current_bottom


@expected_test_result(1514285714288)
def solve2(input):
    stream = InfiniteList(input.strip())
    rocks = InfiniteList([SHAPE1, SHAPE2, SHAPE3, SHAPE4, SHAPE5])
    floor = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)]

    stream_idx = 0
    rock_idx = 0
    current_bottom = 0

    pattern = {}
    heights = {}

    for rock_idx in range(ROUNDS):
        rock = Rock(rocks[rock_idx], current_bottom)
        rock.move(stream[stream_idx], floor)
        while rock.move("v", floor):
            stream_idx += 1
            rock.move(stream[stream_idx], floor)
        stream_idx += 1
        for _, y in rock.shape:
            current_bottom = max(current_bottom, y)
        floor.extend([(x, y) for x, y in rock.shape])

        key = (rock_idx % 5, stream_idx % len(input.strip()))

        if key not in pattern:
            pattern[key] = (rock_idx, current_bottom)
            heights[rock_idx] = current_bottom
        else:
            if (ROUNDS - rock_idx) % (rock_idx - pattern[key][0]) == 0:
                break
    
    pr_idx, bot = pattern[key]
    pattern_len = rock_idx - pr_idx
    pattern_height = current_bottom - bot
    interval = (ROUNDS - pr_idx) // pattern_len
    rest = (ROUNDS - pr_idx) % pattern_len
    height = (interval * pattern_height) + bot

    return height - 1
