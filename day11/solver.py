from runner_utils import expected_test_result
import re

NAME_REGEX = r"Monkey (\d)"
STARTING_ITEMS_REGEX = r"Starting items: (.+)"
OP_REGEX = r"Operation: new = (.+)"
TEST_REGEX = r"Test: divisible by (\d+)"
TRUE_REGEX = r"If true: throw to monkey (\d)"
FALSE_REGEX = r"If false: throw to monkey (\d)"


PROCESSORS = {
    NAME_REGEX: lambda v, m: m.registry.update({v: m}),
    STARTING_ITEMS_REGEX: lambda v, m: list(map(m.make_item, v.split(", "))),
    OP_REGEX: lambda v, m: setattr(m, "operation", v.replace("old", "{old}")),
    TEST_REGEX: lambda v, m: setattr(m, "test_number", int(v)),
    TRUE_REGEX: lambda v, m: m.throws_to.update({True: v}),
    FALSE_REGEX: lambda v, m: m.throws_to.update({False: v}),
}


class SimpleItem:
    def __init__(self, worry_level):
        self.worry_level = worry_level

    def do_operation(self, operation):
        worry_level = eval(operation.format(old=self.worry_level))
        self.worry_level = worry_level // 3

    def is_divisable(self, number):
        return not self.worry_level % number


class Item:
    def __init__(self, worry_level):
        self.worry_level = worry_level
        self.divisors = {}

    def add_divisor(self, divisor):
        self.divisors[divisor] = self.worry_level

    def do_operation(self, operation):
        for divisor, remainder in self.divisors.items():
            worry_level = eval(operation.format(old=remainder))
            self.divisors[divisor] = worry_level % divisor

    def is_divisable(self, number):
        return not self.divisors[number]


class Monkey:
    def __init__(self, registry, item_factory):
        self.items = []
        self.registry = registry
        self.item_factory = item_factory
        self.throws_to = {}
        self.operation = None
        self.test_number = None
        self.total_inspected_items = 0

    def make_item(self, value):
        self.items.append(self.item_factory(value))

    def inspect_items(self):
        while self.items:
            item = self.items.pop(0)
            item.do_operation(self.operation)
            result = item.is_divisable(self.test_number)
            monkey = self.throws_to[result]
            self.registry[monkey].catch(item)
            self.total_inspected_items += 1

    def catch(self, item):
        self.items.append(item)


def parse_monkeys(input, item_factory):
    registry = {}
    for monkey_instructions in input.strip().split("\n\n"):
        monkey = Monkey(registry, item_factory)
        lines = monkey_instructions.splitlines()
        for line, (regex, processor) in zip(lines, PROCESSORS.items()):
            result = re.match(regex, line.strip())
            value, = result.groups()
            processor(value, monkey)
    return registry


def get_monkey_business(registry, rounds):
    for _ in range(rounds):
        for monkey in sorted(registry.keys()):
            registry[monkey].inspect_items()
    a, b = sorted([r.total_inspected_items for r in registry.values()])[-2:]
    return a * b


@expected_test_result(10605)
def solve1(input):
    registry = parse_monkeys(input, SimpleItem)
    return get_monkey_business(registry, 20)


@expected_test_result(2713310158)
def solve2(input):
    registry = parse_monkeys(input, Item)

    divisors = [m.test_number for m in registry.values()]
    for monkey in registry.values():
        for item in monkey.items:
            for divisor in divisors:
                item.add_divisor(divisor)

    return get_monkey_business(registry, 10000)
