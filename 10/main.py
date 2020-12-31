""" Solution to the tenth AOC of 2020. """

import sys
from collections import OrderedDict as odict


def calc_f_diffs(jolts):
    """
    Calculate the number of 1, 2 and 3 jolt diffs between the chain
    connection all jolt rated adapters in the input.

    Input is assumed to be sorted in ascending order.
    """

    jolt_diffs = [0] * 3
    for jolt_1, jolt_2 in zip(jolts[:-1], jolts[1:]):
        try:
            # -1 because of zero-indexing, duh
            jolt_diffs[jolt_2 - jolt_1 - 1] += 1
        except IndexError:
            print(
                (
                    "[Warning] Index out of bound, joltage diff between "
                    "adapters too big"
                )
            )
            exit(1)

    return jolt_diffs


def count_arrangements(jolts):
    """
    Recursively count the number of combinations of descending (with
    descending increments of max 3) jolts there are.

    Input is assumed to be sorted in ascending order.
    """

    comb = {0: 1}
    for jolt in jolts[1:]:
        comb[jolt] = (
            comb.get(jolt - 3, 0)
            + comb.get(jolt - 2, 0)
            + comb.get(jolt - 1, 0)
        )

    return comb[jolts[-1]]


if __name__ == "__main__":
    file_in = sys.argv[1]
    with open(file_in, "r") as fh:
        lines = fh.readlines()
    lines = [line.strip("\n") for line in lines]
    try:
        jolts = list(map(int, lines))
    except ValueError:
        print("[Warning] Could not cast input to integers.")
        exit(1)

    # The charger has a joltage (?) of 0
    jolts.insert(0, 0)

    # The output has a joltage (?) of 3 larger that the maximum rating of your
    # adapter
    jolts.append(max(jolts) + 3)

    jolts = sorted(jolts)

    j_diffs = calc_f_diffs(jolts)
    print(
        "[Task 1] {} [1 J diffs], {} [2 J diffs] and {} [3 J diffs]".format(
            j_diffs[0], j_diffs[1], j_diffs[2]
        )
    )
    print(
        "[Task 1] {} of [1 J diffs * 3 J diffs]".format(j_diffs[0] * j_diffs[2])
    )

    count = count_arrangements(jolts)
    print("[Task 2] {} number of combinations possible".format(count))
