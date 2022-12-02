from runner_utils import expected_test_result

LOSE = 0
DRAW = 3
WIN = 6


class Gesture:
    def __init__(self, points):
        self.points = points
        self._wins_against = None
        self._loses_against = None

    def wins_against(self, gesture):
        self._wins_against = gesture
        gesture._loses_against = self

    def __add__(self, other):
        if other is self._loses_against:
            return self.points + LOSE
        if other is self._wins_against:
            return self.points + WIN
        return self.points + DRAW


ROCK = Gesture(1)
PAPER = Gesture(2)
SCISSORS = Gesture(3)

ROCK.wins_against(SCISSORS)
SCISSORS.wins_against(PAPER)
PAPER.wins_against(ROCK)

GESTURE_MAPPER = {
    "A": ROCK,
    "B": PAPER,
    "C": SCISSORS,
    "X": ROCK,
    "Y": PAPER,
    "Z": SCISSORS,
}


@expected_test_result(15)
def solve1(input):
    points = 0
    for line in [m for m in input.split("\n") if m]:
        points += GESTURE_MAPPER[line[2]] + GESTURE_MAPPER[line[0]]
    return points


OUTCOME_MAPPER = {
    "X": "lose",
    "Y": "draw",
    "Z": "win",
}


def get_gesture_for_outcome(gesture, outcome):
    outcomes = {
        "draw": gesture,
        "win": gesture._loses_against,
        "lose": gesture._wins_against,
    }
    return outcomes[outcome]


@expected_test_result(12)
def solve2(input):
    points = 0
    for line in [m for m in input.split("\n") if m]:
        gesture = GESTURE_MAPPER[line[0]]
        outcome = OUTCOME_MAPPER[line[2]]
        points += get_gesture_for_outcome(gesture, outcome) + gesture
    return points
