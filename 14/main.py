""" Solution to the 14th of 2020's AOC. """

import re

from itertools import product
from sys import argv


def parse_input(lines):
    """
    Parse the input into subprograms.

    A subprogram is defined by a mask followed by a number of assignments. That
    is, a subprogram may be

        ['XXX01X', (8, 11), (7, 101)]

    where 'XXX01X' is the mask and the following tuples are assignments (first
    index is the register and the second index is the value).
    """

    subprogram = None
    subprograms = []

    for line in lines:
        if "mask = " in line:
            if subprogram:
                subprograms.append(subprogram)
            mask = line.lstrip("mask = ")
            subprogram = [mask]
            continue

        match = re.match(r"mem\[(\d+)\] = (\d+)", line)
        if match and subprogram and len(match.groups()) == 2:
            try:
                subprogram.append(tuple(map(int, match.groups())))
            except ValueError:
                raise ValueError("Could not cast to int.")

    # Make sure to append the final subprogram
    subprograms.append(subprogram)

    return subprograms


def execute_programs(programs):
    """
    Execute the programs and return the non-empty memory addresses and their
    values.

    Execute programs in reverse order in order to avoid overwriting.
    """

    def apply_mask(mask, value):
        """
        Apply the mask to the value.

            X = unchanged
            1 = force 1
            0 = force 0
        """

        # First, OR the mask with X replaced with 0
        mask_ = mask.replace("X", "0")
        mask_ = int(mask_, 2)
        value_ = value | mask_

        # Then, AND the mask with X replaced with 1
        mask_ = mask.replace("X", "1")
        mask_ = int(mask_, 2)
        value_ &= mask_

        print(
            "Applying\n{} to\n{} ({})\n{}\n{}\n".format(
                mask,
                format(value, "0{}b".format(len(mask))),
                value,
                "-" * len(mask),
                format(value_, "0{}b".format(len(mask))),
            )
        )

        return value_

    memory = []

    for program in programs[::-1]:
        mask = program[0]
        for address, value in reversed(program[1:]):
            if [item for item in memory if item[0] == address]:
                continue
            memory.append((address, apply_mask(mask, value)))

    return memory


def execute_programs_2(programs):
    """ Execute the programs according to version 2. """

    def apply_mask(mask, address):
        """ Apply the mask to address. """

        address_ = list(format(address, "0{}b".format(len(mask))))

        for index, char in enumerate(mask):
            if char == "X":
                address_[index] = "X"
            elif char == "1":
                address_[index] = "1"

        print(
            "Applying\n{} to\n{} ({})\n{}\n{}\n".format(
                mask,
                format(address, "0{}b".format(len(mask))),
                address,
                "-" * len(mask),
                "".join(address_),
            )
        )

        return "".join(address_)

    def gen_addresses(masked_address):
        """ Generate all combinations of addresses. """

        dof = masked_address.count("X")
        combos = product("01", repeat=dof)

        addresses = []

        for combo in combos:
            address = masked_address
            for char in combo:
                address = address.replace("X", char, 1)
            addresses.append(address)

        return [int(b, 2) for b in addresses]

    memory = {}

    for program in programs:
        mask = program[0]
        for address, value in program[1:]:
            masked_address = apply_mask(mask, address)
            for address in gen_addresses(masked_address):
                memory[address] = value
    return memory


if __name__ == "__main__":
    file_in = argv[1]
    with open(file_in, "r") as fh:
        lines = [line.rstrip() for line in fh.readlines()]

    subprograms = parse_input(lines)

    program = execute_programs(subprograms)
    value_sum = sum(n for _, n in program)
    print("[Task 1] Sum is: {}".format(value_sum))

    program = execute_programs_2(subprograms)
    value_sum = sum(program.values())
    print("[Task 2] Sum is: {}".format(value_sum))
