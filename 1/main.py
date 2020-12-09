""" Entry for AOC 2020 Dat 1. """

import sys

def calculate_product_1(exp_report):
    """ Find the two entries that sum to 2020 and calculate their product. """

    # Issue an early exit if list is one element long (we have then not been
    # able to find the product
    if len(exp_report) == 1:
        print("No valid sum found")
        return None

    first_entry = exp_report[0]
    for second_entry in exp_report[1:]:
        if (first_entry + second_entry) == 2020:
            print('Entries are {}, and {}'.format(first_entry,
                                                  second_entry))
            return (first_entry * second_entry)

    # Recursively try the slice of exp_report
    return calculate_product_1(exp_report[1:])

def calculate_product_2(exp_report):
    """
    Find the three entries that sum to 2020 and calculate their product.
    """

    # Issue an early exit if list is one element long (we have then not been
    # able to find the product
    if len(exp_report) == 1:
        print("No valid sum found")
        return None

    first_entry = exp_report[0]
    for index, second_entry in enumerate(exp_report[1:]):
        for third_entry in exp_report[index+2:]:
            if (first_entry + second_entry + third_entry) == 2020:
                print('Entries are {}, {} and {}'.format(first_entry,
                                                         second_entry,
                                                         third_entry))
                return (first_entry * second_entry * third_entry)

    # Recursively try the slice of exp_report
    return calculate_product_2(exp_report[1:])


if __name__ == '__main__':
    if len(sys.argv) > 1:
        in_file = sys.argv[1]
    else:
        print('Missing text file input')
        exit(1)

    with open(in_file, 'r') as file_h:
        exp_report = file_h.readlines()
    exp_report = [int(entry.replace(r'\n', '')) for entry in exp_report]

    product = calculate_product_1(exp_report)
    print('Product is (task 1): {}'.format(product))

    product = calculate_product_2(exp_report)
    print('Product is (task 2): {}'.format(product))
