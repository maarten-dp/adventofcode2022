from runner_utils import expected_test_result


class Noop:
    def __init__(self, cpu, value):
        pass

    def perform(self):
        return True


class Addx:
    def __init__(self, cpu, value):
        self.cpu = cpu
        self.value = int(value)
        self.remaining_cycles = 2

    def perform(self):
        self.remaining_cycles -= 1
        is_done = not self.remaining_cycles
        if is_done:
            self.cpu.register += self.value
        return is_done


OPERATIONS = {
    "noop": Noop,
    "addx": Addx,
}


class CPU:
    def __init__(self):
        self.register = 1
        self.cycle = 0
        self.signal_strength = 0
        self.operations = []
        self.current_operation = None

    def load_program(self, input):
        for line in input:
            args = line.split(" ")
            op, value = args[0], args[-1]
            self.operations.append(OPERATIONS[op](self, value))
        self.current_operation = self.operations.pop(0)

    def perform_cycle(self):
        self.cycle += 1
        self.signal_strength = self.register * self.cycle

        if self.current_operation.perform():
            self.current_operation = self.operations.pop(0)

        return bool(self.operations)


class Sprite:
    def __init__(self):
        self.x = 0

    def move(self, position):
        self.x = position

    def is_visible(self, coordinate):
        return coordinate in list(range(self.x, self.x + 3))


class CRT:
    def __init__(self, cpu, sprite):
        self.cpu = cpu
        self.sprite = sprite
        self.buffer = []

    def draw(self, pixel):
        output = "."
        if self.sprite.is_visible(pixel):
            output = "#"
        self.buffer.append(output)
        self.sprite.move(self.cpu.register)

    def flush(self):
        print("".join(self.buffer))
        self.buffer = []
        

@expected_test_result(13140)
def solve1(input):
    cpu = CPU()
    cpu.load_program(input.strip().splitlines())

    measurements = [20, 60, 100, 140, 180, 220]
    signal_strength = 0
    while cpu.perform_cycle():
        if cpu.cycle in measurements:
            signal_strength += cpu.signal_strength
    return signal_strength


@expected_test_result(None)
def solve2(input):
    sprite = Sprite()
    cpu = CPU()
    cpu.load_program(input.strip().splitlines())
    crt = CRT(cpu, sprite)

    screen_width = 40
    while cpu.perform_cycle():
        pixel = (cpu.cycle % screen_width) or screen_width
        crt.draw(pixel)
        if pixel == screen_width:
            crt.flush()
        
    crt.flush()
