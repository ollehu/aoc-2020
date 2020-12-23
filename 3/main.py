""" Solution to the third problem of AOC 2020. """

import sys


def lines_to_matrix(lines):
    """
    Convert a list of string into a matrix. For example, turn

    in = ['qwer', 'asdf']

        into

    out = [['q', 'w', 'e', 'r'], ['a', 's', 'd', 'f']]
    """

    for index, line in enumerate(lines):
        lines[index] = [char for char in line]

    return lines


def count_trees(matrix, dx, dy):
    """ Calculate the number of trees encountered by traversing dx, dy. """

    # We begin in the upper left corner
    x = 0
    y = 0
    count = 0

    # We continue until y > [height of matrix]
    while(y < len(matrix)):
        if matrix[y][x] == '#':
            count += 1

        # X is special since it needs to be wrapped around
        x = (x + dx) % len(matrix[0])
        y += dy

    return count


def print_block(line):
    """ Print block. """

    print('#' * len(line))
    print(line)
    print('#' * len(line))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_in = sys.argv[1]

        with open(file_in) as fh:
            lines = fh.readlines()
        lines = [line.strip('\n') for line in lines]

        # Turn the input into a matrix
        matrix = lines_to_matrix(lines)

        # TASK !
        dx = 3
        dy = 1

        # Calculate number of tress
        count = count_trees(matrix, dx, dy)
        print_block('[Task 1] Encountered {} of trees.'.format(count))

        # TASK 2
        dx_list = [1, 3, 5, 7, 1]
        dy_list = [1, 1, 1, 1, 2]
        product = 1

        for dx, dy in zip(dx_list, dy_list):
            count = count_trees(matrix, dx, dy)
            product *= count

        print_block('[Task 2] Encountered {} of trees.'.format(product))
    else:
        print('Warning: No input file provided.')

