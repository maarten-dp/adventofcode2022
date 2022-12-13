from runner_utils import expected_test_result


def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left != right:
            return left < right
    elif isinstance(left, int):
        return compare([left], right)
    elif isinstance(right, int):
        return compare(left, [right])
    else:
        for l, r in zip(left, right):
            if (result := compare(l, r)) is not None:
                return result
        if len(left) != len(right):
            return len(left) < len(right)


class Packet:
    def __init__(self, packet):
        self.packet = eval(packet)

    def __lt__(self, other):
        return compare(self.packet, other.packet)


@expected_test_result(13)
def solve1(input):
    correct_pairs = 0
    for idx, pair in enumerate(input.strip().split("\n\n"), start=1):
        left, right = pair.splitlines()
        result = compare(eval(left), eval(right))
        if result is True:
            correct_pairs += idx
    return correct_pairs


@expected_test_result(140)
def solve2(input):
    divider_packet1 = Packet("[[2]]")
    divider_packet2 = Packet("[[6]]")
    packets = [Packet(p) for p in input.strip().splitlines() if p]
    packets.extend((divider_packet1, divider_packet2))

    sorted_packets = sorted(packets)
    index1 = sorted_packets.index(divider_packet1) + 1
    index2 = sorted_packets.index(divider_packet2) + 1

    return index1 * index2
