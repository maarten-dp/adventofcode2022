import re
from collections import defaultdict
from itertools import chain

from runner_utils import expected_test_result

REGEX = r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"


class Sensor:
    def __init__(self, x, y, bx, by):
        self.x = x
        self.y = y
        self.distance = abs(x - bx) + abs(y - by)

    def is_in_y_range(self, y):
        return self.y - self.distance <= y <= self.y + self.distance

    def x_range(self, y):
        from_x, to_x = self.raw_x_range(y)
        return list(range(from_x, to_x + 1))

    def raw_x_range(self, y, min_x=None, max_x=None):
        offset = abs(self.y - y)
        if offset > self.distance:
            return None
        distance = self.distance - offset
        from_x = self.x - distance
        to_x = self.x + distance

        if min_x:
            from_x = max(min_x, from_x)
        if max_x:
            to_x = min(max_x, to_x)

        return from_x, to_x

    def has_coverage(self, min_c, max_c):
        has_x_coverage = self.has_coverage_in_x_range(min_c, max_c)
        has_y_coverage = self.has_coverage_in_y_range(min_c, max_c)
        return has_x_coverage and has_y_coverage

    def has_coverage_in_x_range(self, min_x, max_x):
        min_dist_range = min_x < self.x - self.distance <= max_x
        max_dist_range = min_x < self.x + self.distance <= max_x
        return min_dist_range or max_dist_range

    def has_coverage_in_y_range(self, min_y, max_y):
        min_dist_range = min_y < self.y - self.distance <= max_y
        max_dist_range = min_y < self.y + self.distance <= max_y
        return min_dist_range or max_dist_range


def deploy_sensors(input):
    sensors = []
    beacons = set()
    for line in input.strip().splitlines():
        x, y, bx, by = map(int, re.match(REGEX, line).groups())
        sensor = Sensor(x, y, bx, by)
        beacons.add((bx, by))
        y, distance = sensor.y, sensor.distance
        sensors.append(sensor)
    return sensors, beacons


@expected_test_result(26)
def solve1(input):
    # line = 10
    line = 2000000

    sensors, beacons = deploy_sensors(input)
    y_sensors = [s for s in sensors if s.is_in_y_range(line)]

    x_range = set(chain(*[s.x_range(line) for s in y_sensors]))
    beacons_on_y = sum([b[1] == line for b in beacons])
    return len(x_range) - beacons_on_y


def resolve_overlap(fx1, tx1, fx2, tx2):
    if fx1 <= fx2 <= tx2 <= tx1:
        return [(fx1, tx1)]
    if fx2 <= fx1 <= tx1 <= tx2:
        return [(fx2, tx2)]
    if fx1 <= fx2 <= tx1 + 1:
        return [(fx1, tx2)]
    if fx1 + 1 <= tx2 <= tx1:
        return [(fx2, tx1)]
    return [(fx1, tx1), (fx2, tx2)]


def resolve_overlaps(overlaps):
    o1 = overlaps.pop(0)
    while overlaps:
        res = resolve_overlap(*o1, *overlaps.pop(0))
        if len(res) == 1:
            o1 = res[0]
        else:
            return min(res[0][1], res[1][1]) + 1


@expected_test_result(56000011)
def solve2(input):
    frequency = 4000000
    # max_coords = 20
    max_coords = 4000000

    sensors, _ = deploy_sensors(input)
    sensors = [s for s in sensors if s.has_coverage(0, max_coords)]
    for y in range(0, max_coords + 1):
        overlaps = [s.raw_x_range(y, 0, max_coords) for s in sensors]
        if result := resolve_overlaps(sorted([o for o in overlaps if o])):
            return (result * frequency) + y
