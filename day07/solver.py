from runner_utils import expected_test_result


class Directory:
    def __init__(self, name, pardir=None):
        self.pardir = pardir
        self.name = name
        self.contents = []
        self.directories = {}

    def __radd__(self, other):
        return self.size + other

    @property
    def size(self):
        return sum(self.contents)

    def add(self, item):
        if isinstance(item, Directory):
            self.directories[item.name] = item
        self.contents.append(item)


class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def __radd__(self, other):
        return self.size + other


class Terminal:
    def __init__(self, commands):
        self.directories = []
        self.root = Directory("/")
        self.current_directory = None
        self.commands = commands

    def parse_commands(self):
        while self.commands:
            command = self.commands.pop(0)
            if command == "$ ls":
                self.handle_output()
            else:
                self.handle_cd(command)

    def handle_cd(self, command):
        location = command.split(" ")[-1]
        if location == "/":
            self.current_directory = self.root
        elif location == "..":
            if self.current_directory.pardir:
                self.current_directory = self.current_directory.pardir
        else:
            directory = self.current_directory.directories.get(location)
            self.current_directory = directory

    def handle_output(self):
        while self.commands and not self.commands[0].startswith("$"):
            line = self.commands.pop(0)
            size_or_dir, name = line.split(" ")
            if size_or_dir == "dir":
                item = Directory(name, self.current_directory)
                self.directories.append(item)
            else:
                item = File(name, int(size_or_dir))
            self.current_directory.add(item)


@expected_test_result(95437)
def solve1(input):
    terminal = Terminal(input.strip().splitlines())
    terminal.parse_commands()

    total_size = 0
    for directory in terminal.directories:
        size = directory.size
        if size <= 100000:
            total_size += size
    return total_size


@expected_test_result(24933642)
def solve2(input):
    terminal = Terminal(input.strip().splitlines())
    terminal.parse_commands()

    space_needed = 30000000
    total_space = 70000000
    free_space = total_space - terminal.root.size
    current_smallest_size = total_space
    for directory in terminal.directories:
        size = directory.size
        potential_free_space = free_space + size
        if potential_free_space > space_needed:
            current_smallest_size = min(current_smallest_size, size)
    return current_smallest_size
