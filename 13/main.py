""" Solution to the 13th of 2020's AOC. """

from math import ceil, floor
from sys import argv


def parse_input(lines):
    """
    Parse input into arrival_time and bus_ids.

    Bus IDs of x are ignored.
    """

    try:
        arrival_time = int(lines[0])
    except ValueError:
        raise ValueError("Could not parse arrival time.")

    bus_ids = lines[1].split(",")
    bus_indices = list(range(len(bus_ids)))

    try:
        bus_indices = [
            index
            for index, bus_id in zip(bus_indices, bus_ids)
            if bus_id != "x"
        ]
        bus_ids = [int(bus_id) for bus_id in bus_ids if bus_id != "x"]
    except ValueError:
        raise ValueError("Could not parse bus IDs.")

    return arrival_time, bus_ids, bus_indices


def calculate_delta(arrival_time, bus_ids, look_back=False):
    """
    Calculate the waiting time for each bus assuming that the passenger
    arrives at arrival_time.

    Times are calculated according to (for each bus_id in bus_ids):

        time = ceil(arrival_time / bus_id) * bus_id - arrival_time

    If look_back is set, then the "recently missed" bus is returned.
    """

    if isinstance(bus_ids, int):
        if look_back:
            return floor(arrival_time / bus_ids) * bus_ids - arrival_time
        else:
            return ceil(arrival_time / bus_ids) * bus_ids - arrival_time

    if look_back:
        return [
            floor(arrival_time / bus_id) * bus_id - arrival_time
            for bus_id in bus_ids
        ]
    else:
        return [
            ceil(arrival_time / bus_id) * bus_id - arrival_time
            for bus_id in bus_ids
        ]


def find_consecutive_seq2(bus_ids, bus_indices):
    """
    Keep adding the least common multiple until we get a number that is
    divisible by the previous prime.
    """

    lcm = 1
    origin = 0

    for index in range(len(bus_ids) - 1):
        bus_id = bus_ids[index+1]
        index_ = bus_indices[index+1]
        lcm *= bus_ids[index]

        while (origin + index_) % bus_id != 0:
            origin += lcm

    return origin


if __name__ == "__main__":
    file_in = argv[1]
    with open(file_in, "r") as fh:
        lines = fh.readlines()
    lines = [line.strip("\n") for line in lines]

    arrival_time, bus_ids, bus_indices = parse_input(lines)
    waiting_times = calculate_delta(arrival_time, bus_ids)

    # Get the shortest waiting time
    index = waiting_times.index(min(waiting_times))
    bus_id = bus_ids[index]
    waiting_time = waiting_times[index]
    print("[Task 1] Product is: {}".format(bus_id * waiting_time))

    index = find_consecutive_seq2(bus_ids, bus_indices)
    print("[Task 2] First index is: {}".format(index))
