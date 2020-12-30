""" The solution to the 9th AOC of 2020. """

import sys

# Header length
N_HEADER = 25


def check_sum(header, result):
    """
    Verify if number is the sum of two of the (unique) numbers of header.
    """

    for index, comp_1 in enumerate(header):
        for comp_2 in header[index:]:
            if not comp_1 == comp_2 and result == (comp_1 + comp_2):
                return True

    return False


def locate_faulty_number(numbers):
    """
    Locate the first faulty number.

    A faulty number is identified by not being the sum of two unique numbers of
    the previous 25 entries.
    """

    header = numbers[:N_HEADER]

    for number in numbers[N_HEADER:]:

        if not check_sum(header, number):
            return number

        # Update header
        header = header[1:] + [number]

    print("[Warning] Did not identify a faulty number.")
    return None


def find_invalid_combo(numbers, result):
    """
    Find the set of consecutive set of (minimum two) numbers that sum up to
    result.
    """

    cur_slice = [0, 0]
    cur_sum = sum(numbers[cur_slice[0] : cur_slice[1]])

    while cur_sum != result:

        # Sane exit
        if any(
            [True for n in numbers[cur_slice[0] : cur_slice[1]] if n > result]
        ):
            print("[Warning] Could not find a solution.")
            exit(1)

        if sum(numbers[cur_slice[0] : cur_slice[1]]) > result:
            cur_slice[0] += 1
        else:
            cur_slice[1] += 1
        cur_sum = sum(numbers[cur_slice[0] : cur_slice[1]])

    return numbers[cur_slice[0] : cur_slice[1]]


if __name__ == "__main__":
    file_in = sys.argv[1]
    with open(file_in, "r") as fh:
        lines = fh.readlines()
    lines = [line.strip("\n") for line in lines]

    try:
        xmas = [int(line) for line in lines]
    except ValueError:
        print("[Warning] Cannot convert input to integer")
        exit(1)

    number = locate_faulty_number(xmas)
    print("[Task 1] First faulty number is {}.".format(number))

    # Task 2
    if len(sys.argv) > 1:
        try:
            invalid_number = int(sys.argv[2])
        except ValueError:
            print("[Warning] Cannot cast {} to integer".format(sys.argv[2]))
        combo = find_invalid_combo(xmas, invalid_number)
        print(
            "[Task 2] Lower: {} Upper: {} (total set is {}) sum: {}".format(
                min(combo),
                max(combo),
                ", ".join(map(str, combo)),
                min(combo) + max(combo),
            )
        )
