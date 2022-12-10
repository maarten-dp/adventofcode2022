from runner_utils import expected_test_result

MOVE = {
    "U": (0, -1),
    "D": (0, 1),
    "L": (-1, 0),
    "R": (1, 0),
}


class Knot:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.visited = set([(0, 0)])
        self.child_knot = None

    def make_knots(self, knots):
        if knots:
            self.child_knot = Knot()
            return self.child_knot.make_knots(knots - 1)
        return self

    def keep_up(self, x, y):
        x_diff = x - self.x
        y_diff = y - self.y

        if abs(x_diff) == 2 or abs(y_diff) == 2:
            self.x += x_diff / abs(x_diff) if x_diff else 0
            self.y += y_diff / abs(y_diff) if y_diff else 0

        self.visited.add((self.x, self.y))
        if self.child_knot:
            self.child_knot.keep_up(self.x, self.y)


def move_head(head, direction, amount):
    x_mod, y_mod = MOVE[direction]
    while amount:
        head.x += x_mod
        head.y += y_mod
        head.child_knot.keep_up(head.x, head.y)
        amount -= 1


def get_visited_amount(input, knot_length):
    head = Knot()
    tail = head.make_knots(knots=knot_length)
    for line in input.strip().splitlines():
        direction, amount = line.split(" ")
        move_head(head, direction, int(amount))
    return len(tail.visited)


@expected_test_result(13)
def solve1(input):
    return get_visited_amount(input, knot_length=1)


@expected_test_result(None)
def solve2(input):
    return get_visited_amount(input, knot_length=9)
