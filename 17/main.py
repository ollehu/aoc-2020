""" Solution to the 17th AOC of 2020. """

from copy import deepcopy
from itertools import product
from operator import add
from sys import argv

N_CYCLES = 6


class Space:
    """ Class for managing the space. """

    def __init__(self, dim=3):
        """ Constructor for space. """
        self.active_cubes = []
        self.dim = dim

    def set_initial_state(self, lines):
        """ Set up the initial state. """

        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == "#":
                    t = (x, y)
                    # remaining dimensions are zero
                    for _ in range(self.dim - len(t)):
                        t += (0,)
                    self.active_cubes.append(t)

    def simulate(self):
        """ Simulate one iterations. """

        # Keep track of visisted coordinates
        visited = []

        # We need to keep track of two spaces simultaneously
        new_space = deepcopy(self.active_cubes)

        # We need to update the given coordinates and surrounding ones
        for coord_ in self.active_cubes:
            for coord in self.get_adjacent_coords(coord_, include_self=True):
                if coord in visited:
                    continue
                if (
                    coord in self.active_cubes
                    and not 2 <= self.count_neighbours(coord) <= 3
                ):
                    new_space.remove(coord)
                elif (
                    coord not in self.active_cubes
                    and self.count_neighbours(coord) == 3
                ):
                    new_space.append(coord)
                visited.append(coord)

        self.active_cubes = new_space

    def count_neighbours(self, coords):
        """ Count the active neighbours from a coordingate. """

        coords = self.get_adjacent_coords(coords)
        return sum([1 for coord in coords if coord in self.active_cubes])

    def sum_cubes(self):
        """ Sum the number of active cubes. """
        return len(self.active_cubes)

    def get_cubes(self):
        """ Return the list of active_cubes. """
        return self.active_cubes

    def print_space(self):
        """ Print space through cutting planes. """

        if self.dim > 3:
            print("print_space not compatible with more than three dimensions")
            raise NotImplementedError

        xmax = max([x for x, _, _ in self.active_cubes])
        xmin = min([x for x, _, _ in self.active_cubes])
        ymax = max([y for _, y, _ in self.active_cubes])
        ymin = min([y for _, y, _ in self.active_cubes])
        zmax = max([z for _, _, z in self.active_cubes])
        zmin = min([z for _, _, z in self.active_cubes])

        coord = product(range(xmin, xmax + 1), range(ymin, ymax + 1))

        # Sort in printing order
        coord = sorted(coord, key=lambda x: x[0])
        coord = sorted(coord, key=lambda x: x[1], reverse=True)

        for z in range(zmin, zmax + 1):
            print("Z layer: {}".format(z))
            for x, y in coord:
                if (x, y, z) in self.active_cubes:
                    print("#", end="")
                else:
                    print(".", end="")
                if x == xmax:
                    print()
            print()

    def get_adjacent_coords(self, center, include_self=False):
        """ Get a list of adjacent coordinates. """

        coords = list(product([-1, 0, 1], repeat=self.dim))
        if not include_self:
            coords = [
                coord for coord in coords if not all(v == 0 for v in coord)
            ]

        # Center around given coordinate
        coord = [tuple(map(add, center, coord_)) for coord_ in coords]

        return coord


if __name__ == "__main__":
    file_in = argv[1]
    with open(file_in, "r") as fh:
        lines = [line.rstrip() for line in fh.readlines()]

    space = Space()

    # Let (0, 0) be bottom left
    space.set_initial_state(reversed(lines))

    for iteration in range(N_CYCLES):
        print("==== ITERATION {} ====".format(iteration))
        space.print_space()
        space.simulate()

    space.print_space()
    n_cubes = space.sum_cubes()
    print("[Task 1] Sum of cubes is: {}".format(n_cubes))

    space = Space(dim=4)

    # Let (0, 0) be bottom left
    space.set_initial_state(reversed(lines))

    for iteration in range(N_CYCLES):
        print("==== ITERATION {} ====".format(iteration))
        space.simulate()

    n_cubes = space.sum_cubes()
    print("[Task 2] Sum of cubes is: {}".format(n_cubes))
