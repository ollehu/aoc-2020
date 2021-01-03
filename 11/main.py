""" Solution to the eleventh AOC of 2020. """

import sys

from copy import deepcopy
from itertools import product


def print_map(iteration, seat_map):
    """ Print a seat map and its iteration. """

    print("Seat map of iteration {}:".format(iteration))
    print("-" * len(seat_map[0]))
    print("\n".join(["".join(row) for row in seat_map]))
    print("-" * len(seat_map[0]))


def count_neighbours(seat_map, x, y, ray_trace=False):
    """ Count the number of adjacent occupied seats in index (x, y). """

    count = 0
    xmax = len(seat_map[0])
    ymax = len(seat_map)

    search_dirs = product(range(-1, 2), repeat=2)

    search_dirs = [
        (x_, y_) for x_, y_ in search_dirs if x_ != 0 or y_ != 0
    ]

    for x_direction, y_direction in search_dirs:
        step_length = 1
        while True:
            x_coord = x + x_direction * step_length
            y_coord = y + y_direction * step_length

            if not (0 <= x_coord < xmax and 0 <= y_coord < ymax):
                break

            if seat_map[y_coord][x_coord] == "L":
                break
            elif seat_map[y_coord][x_coord] == "#":
                count += 1
                break

            if not ray_trace:
                break

            step_length += 1

    return count


def update_seat_map(seat_map, max_neighbours=5, ray_trace=False):
    """ Update the seat map and return it. """

    new_seat_map = deepcopy(seat_map)

    # Loop through seats
    for y, row in enumerate(seat_map):
        for x, seat in enumerate(row):
            neighbours = count_neighbours(seat_map, x, y, ray_trace=ray_trace)
            if seat == ".":
                continue

            if seat == "L" and neighbours == 0:
                new_seat_map[y][x] = "#"
            elif seat == "#" and neighbours >= max_neighbours:
                new_seat_map[y][x] = "L"

    return new_seat_map


def equal_maps(map_1, map_2):
    """ Compare two maps by elements. """

    for row_1, row_2 in zip(map_1, map_2):
        for col_1, col_2 in zip(row_1, row_2):
            if col_1 != col_2:
                return False
    return True


def converge_seat_map(seat_map, ray_trace=False):
    """ Converge the seat map and return the number of occupied seats. """

    iteration = 0
    updated_map = None

    # Print initial seat map
    print_map(iteration, seat_map)

    # Execute first iteration
    iteration += 1
    previos_seat_map = deepcopy(seat_map)
    updated_map = update_seat_map(seat_map, ray_trace=ray_trace)
    print_map(iteration, updated_map)

    while not equal_maps(previos_seat_map, updated_map):
        iteration += 1
        previos_seat_map = deepcopy(updated_map)
        updated_map = update_seat_map(updated_map, ray_trace=ray_trace)
        print_map(iteration, updated_map)

    full_str = "".join([item for sublist in updated_map for item in sublist])
    return full_str.count("#")


if __name__ == "__main__":
    file_in = sys.argv[1]
    with open(file_in, "r") as fh:
        rows = fh.readlines()
    rows = [row.strip("\n") for row in rows]

    # Turn into 2D array, first index i y (row) and second index is x (column)
    seat_map = list(map(list, rows))

    count = converge_seat_map(seat_map)
    print("[Task 1] Total number of occupied seats: {}".format(count))

    count = converge_seat_map(seat_map, ray_trace=True)
    print("[Task 2] Total number of occupied seats: {}".format(count))
