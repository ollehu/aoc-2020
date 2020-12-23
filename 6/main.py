""" Solution to the sixth problem of 2020's AOC. """

import sys


def convert_lines(lines):
    """ Convert lines into a list of lists that contain unique characters. """

    index = 0
    out_list = [[]]

    for line in lines:
        if not line and out_list[index]:
            index += 1
            out_list.append([])
            continue

        out_list[index].extend([char for char in line])

    # Sort out the duplicate values
    out_list = list(map(lambda x: list(set(x)), out_list))

    return out_list


def convert_lines_advanced(lines):
    """ Convert lines according to the advanced instructions. """

    index = 0
    out_list = [[]]

    for line in lines:
        if not line and out_list[index]:
            index += 1
            out_list.append([])
            continue

        out_list[index].append(line)

    # Get all the questions that all pasengers (in the same group)
    # answered yes to
    out_chars = []
    for group in out_list:
        group_chars = []
        for char in group[0]:
            char_in_groups = True
            for passenger in group[1:]:
                if not char in passenger:
                    char_in_groups = False
                    break
            if char_in_groups:
                group_chars.append(char)
        out_chars.append(group_chars)

    return out_chars

if __name__ == '__main__':
    file_in = sys.argv[1]
    with open(file_in, 'r') as fh:
        lines = fh.readlines()
    lines = [line.strip('\n') for line in lines]
    group_list = convert_lines(lines)

    group_sum = 0
    for index, group in enumerate(group_list):
        group_sum += len(group)
        print(('Group {} answered yes to {} ' +
               'question(s) ({})').format(index, len(group), ', '.join(group)))

    print('[Task 1] Sum of groups is: {}'.format(group_sum))

    group_list = convert_lines_advanced(lines)
    group_sum = 0
    for group in group_list:
        group_sum += len(group)

    print('[Task 2] Sum of groups is: {}'.format(group_sum))
