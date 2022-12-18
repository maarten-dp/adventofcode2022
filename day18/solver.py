from runner_utils import expected_test_result

MODIFS = [
    (-1, 0, 0),
    (1, 0, 0),
    (0, -1, 0),
    (0, 1, 0),
    (0, 0, -1),
    (0, 0, 1),
]


def register_neighbours(cube, registry):
    for x_mod, y_mod, z_mod in MODIFS:
        key = (cube.x + x_mod, cube.y + y_mod, cube.z + z_mod)
        if neighbour_cube := registry.get(key):
            cube.register_neighbour(neighbour_cube)


def make_cubes(input):
    registry = {}
    for cube_coords in input.strip().splitlines():
        x, y, z = map(int, cube_coords.split(","))
        cube = Cube(x, y, z)
        registry[(x, y, z)] = cube
        register_neighbours(cube, registry)
    return registry


def make_air(registry):
    max_x = max([c.x for c in registry.values()])
    min_x = min([c.x for c in registry.values()])
    max_y = max([c.y for c in registry.values()])
    min_y = min([c.y for c in registry.values()])
    max_z = max([c.z for c in registry.values()])
    min_z = min([c.z for c in registry.values()])

    air_cubes = []
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            for z in range(min_z, max_z + 1):
                if (x, y, z) not in registry:
                    air = Air(x, y, z)
                    registry[(x, y, z)] = air
                    air_cubes.append(air)
                    register_neighbours(air, registry)
    return air_cubes


class Cube:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.neighbours = []

    def register_neighbour(self, neighbour):
        self.neighbours.append(neighbour)
        neighbour.neighbours.append(self)


class Air(Cube):
    def contained(self):
        if len(self.neighbours) != 6:
            for neighbour in self.neighbours[:]:
                self.unregister_neighbour(neighbour)
            return False
        return True

    def unregister_neighbour(self, neighbour):
        self.neighbours.pop(self.neighbours.index(neighbour))
        neighbour.neighbours.pop(neighbour.neighbours.index(self))


@expected_test_result(64)
def solve1(input):
    registry = make_cubes(input)

    surface_area = 0
    for cube in registry.values():
        surface_area += 6 - len(cube.neighbours)
    return surface_area


@expected_test_result(58)
def solve2(input):
    registry = registry = make_cubes(input)

    cubes = list(registry.values())
    air_cubes = make_air(registry)

    loose_air = True
    while loose_air:
        loose_air = False
        for air_cube in air_cubes[:]:
            if not air_cube.contained():
                air_cubes.pop(air_cubes.index(air_cube))
                loose_air = True

    surface_area = 0
    for cube in cubes:
        surface_area += 6 - len(cube.neighbours)
    return surface_area
