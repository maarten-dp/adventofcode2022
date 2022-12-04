from runner_utils import expected_test_result


def get_range(sections):
    start, end = map(int, sections.split("-"))
    return set(range(start, end + 1))


def get_ranges(line):
    sections1, sections2 = line.split(",")
    range1 = get_range(sections1)
    range2 = get_range(sections2)
    return range1, range2


@expected_test_result(2)
def solve1(input):
    containing_pairs = 0
    for line in input.strip().split("\n"):
        range1, range2 = get_ranges(line)
        containing_pairs += range1.issubset(range2) or range2.issubset(range1)
    return containing_pairs


@expected_test_result(4)
def solve2(input):
    overlapping_pairs = 0
    for line in input.strip().split("\n"):
        range1, range2 = get_ranges(line)
        overlapping_pairs += bool(range1.intersection(range2))
    return overlapping_pairs
