""" Solution to the 7th AOC 2020. """

import re
import sys

from json import dumps

VERBOSE = False


def sanitize_input(lines):
    """ Clean the input by removing new lines and punctuations. """

    lines = [line.strip("\n") for line in lines]
    lines = [line.replace(".", "") for line in lines]

    return lines


def get_parent_color(line):
    """
    From a line (for example: red bags contain 3 white bags, 2 gold bags) get
    the parent color (red). Also return the remained of the string.
    """

    pattern = re.compile(r"^(.+) bags contain (.+)")
    result = pattern.search(line)

    # There should at least be one group (index 0 is always the full match)
    try:
        return result.group(1), result.group(2)
    except IndexError:
        print("[Warning] No parent color found in line {}".format(lines))
        exit(1)


def get_leafs(line):
    """
    From a list of bag content (for example: 3 white bags, 2 gold bags) return
    a dictionary containing the colors and amount, that is

        {'white': 3, 'gold': 2}

    If the bag cannot carry any other bags, return None.
    """

    # Early exit for empty bags
    if line == "no other bags":
        return None

    leaf_dict = dict()
    pattern = r"(\d+ [\w\s]+)"
    bag_types = re.findall(pattern, line)

    pattern = re.compile(r"(\d+) ([\w\s]+) bag")
    for bag_type in bag_types:
        results = pattern.search(bag_type)
        try:
            count = results.group(1)
            color = results.group(2)
        except IndexError:
            print("[Warning] No subbags fround in line {}".format(line))
        leaf_dict[color] = count

    if VERBOSE:
        print(
            "{} -> {}".format(
                line,
                ", ".join(
                    [
                        "{} ({})".format(value, key)
                        for key, value in leaf_dict.items()
                    ]
                ),
            )
        )

    return leaf_dict


def possible_bags(bag_tree, my_bag):
    """ Count the number of bags my_bag is included in. """

    def contains_my_bag(full_tree, key, my_bag):
        """ Recursively check if my_bag is found in the tree. """

        if full_tree[key] is None:
            return False

        if my_bag in full_tree[key]:
            return True

        # Loop through all of the leaves
        for key in full_tree[key]:
            if contains_my_bag(full_tree, key, my_bag):
                return True
        return False

    return sum(
        [1 for bag in bag_tree if contains_my_bag(bag_tree, bag, my_bag)]
    )


def bag_count(full_tree, key):
    """ Recursively count the number of bags in my_bag. """

    # Initiate count at 1 to include the current bag
    count = 1
    sub_tree = full_tree[key]

    if sub_tree is None:
        return 1

    for bag in sub_tree:
        count = count + int(sub_tree[bag]) * bag_count(full_tree, bag)

    return count


def lines_to_dict(lines):
    """
    Turn lines into a dictionary (of dictionaries) that build the dependency
    tree of bags. For example:

        red bags contain 3 white bags, 2 gold bags

    becomes

        {'red': {'white': 3, 'gold', 2}}
    """

    bag_dict = dict()

    for line in lines:
        parent_color, bag_content = get_parent_color(line)
        leafs = get_leafs(bag_content)
        bag_dict[parent_color] = leafs

    if VERBOSE:
        print(dumps(bag_dict, sort_keys=True, indent=4))

    return bag_dict


if __name__ == "__main__":
    file_in = sys.argv[1]
    my_bag = sys.argv[2]
    with open(file_in, "r") as fh:
        lines = fh.readlines()

    lines = sanitize_input(lines)
    bag_tree = lines_to_dict(lines)

    count = possible_bags(bag_tree, my_bag)
    print(
        "Your bag ({}) can be contained in {} different colors.".format(
            my_bag, count
        )
    )

    # Count bags and subtract one (don't include the golden bag)
    count = bag_count(bag_tree, my_bag) - 1
    print("Your bag ({}) contains {} other bags.".format(my_bag, count))
