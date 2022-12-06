from runner_utils import expected_test_result

from collections import deque

START_OF_PACKET_SIZE = 4
START_OF_MESSAGE_SIZE = 14


def find_marker(input, size):
    q = deque(maxlen=size)
    for idx, char in enumerate(input, start=1):
        q.append(char)
        if len(set(q)) == size:
            return idx


@expected_test_result(7)
def solve1(input):
    return find_marker(input, START_OF_PACKET_SIZE)


@expected_test_result(19)
def solve2(input):
    return find_marker(input, START_OF_MESSAGE_SIZE)
