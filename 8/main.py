""" Solution to the eight AOC of 2020. """

import re
import sys

from copy import copy


def lines_to_tuples(lines):
    """
    Convert lines to a list of tuples where each tuple contains the
    instruction and value, for example ('nop', +0) or ('jmp', -5).
    """

    tuples = []
    pattern = re.compile(r"(acc|jmp|nop) ([\+-]\d+)")

    for line in lines:
        results = pattern.search(line)
        try:
            op = results.group(1)
            count = int(results.group(2))
        except IndexError:
            print("[Warning] Could not parse line {}".format(line))
            exit(1)
        except ValueError:
            print("[Warning] Could not cast {}".format(results.group(2)))

        tuples.append((op, count))

    return tuples


def execute_instructions(instructions):
    """
    Execute the instructions (beginning at the zeroth instructions) until the
    same instructions is about to be executed twice. Return the accumulator's
    value and the number of operations at that point.
    """

    address = 0
    addresses = []
    exit_code = 1
    accumulator = 0
    executed = [False] * len(instructions)

    while not executed[address]:
        executed[address] = True
        addresses.append(address)

        # Get operation
        op = instructions[address][0]
        count = instructions[address][1]

        if op == "acc":
            accumulator += count
            address += 1
        elif op == "jmp":
            address += count
        elif instructions[address][0] == "nop":
            address += 1

        # Check if we exited successfully
        if not address < len(instructions):
            exit_code = 0
            break

    return accumulator, addresses, exit_code


def execute_instructions_bug_fix(instructions):
    """
    Execute the instructions (beginning at the zeroth instructions) until the
    same instructions is about to be executed twice. Return the accumulator's
    value and the number of operations at that point.

    With bug fixed.
    """

    # First, execute the program without bugs fixed
    _, addresses, _ = execute_instructions(instructions)

    # From the beginning of addresses, begin by replacing jmp (with nop) or nop
    # (with jmp) until we can execute with an exit code of 0
    for address in addresses:
        op = instructions[address][0]
        count = instructions[address][1]

        altered_instructions = copy(instructions)
        if op == "jmp":
            altered_instructions[address] = ("nop", count)
        elif op == "nop":
            altered_instructions[address] = ("jmp", count)

        accumulator, addresses, exit_code = execute_instructions(
            altered_instructions
        )

        if not exit_code:
            print("Fixed bug at address {}".format(address))
            return accumulator, addresses, exit_code

    print("[Warning] Did not manage to fix bug")


if __name__ == "__main__":
    input_file = sys.argv[1]
    with open(input_file, "r") as fh:
        lines = fh.readlines()
    lines = [line.strip("\n") for line in lines]

    instructions = lines_to_tuples(lines)

    acc_count, addresses, exit_code = execute_instructions(instructions)
    print(
        (
            "[Task 1] The accumulator is at \033[1m{}\033[0m after {} number "
            + "of operations (exit code {})"
        ).format(acc_count, len(addresses), exit_code)
    )

    acc_count, addresses, exit_code = execute_instructions_bug_fix(instructions)
    print(
        (
            "[Task 2] The accumulator is at \033[1m{}\033[0m after {} number "
            + "of operations (exit_code {})"
        ).format(acc_count, len(addresses), exit_code)
    )
