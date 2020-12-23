""" Solution to the second problem of 2020's AOC. """

import re
import sys

def parse_lines(lines):
    """ Parse the lines into limits, characters and passwords. """

    limits = []
    chars = []
    pws = []

    pattern = r'^(\d+)-(\d+) ([a-z]): ([a-z]+)$'
    regexp = re.compile(pattern)

    for line in lines:
        re_match = regexp.match(line)

        lower = re_match.group(1)
        upper = re_match.group(2)
        char = re_match.group(3)
        pw = re_match.group(4)

        try:
            limits.append([int(lower), int(upper)])
        except ValueError:
            print('Cannot convert {} or {} to int.'.format(lower, upper))

        chars.append(char)
        pws.append(pw)

    return limits, chars, pws


def validate_passwords(limits, chars, passwords):
    """ Validate the passwords. """

    count = 0
    for index, password in enumerate(passwords):
        char_count = password.count(chars[index])
        if limits[index][0] <= char_count <= limits[index][1]:
            count += 1

    return count


def validate_passwords_2(limits, chars, passwords):
    """ Validate passwords according to the new standard. """

    count = 0
    for index, password in enumerate(passwords):
        indices = [ind - 1 for ind in limits[index]]
        char_count = sum([1 for ind in indices
                          if password[ind] == chars[index]])

        if char_count == 1:
            count += 1
            print(('Password {} has one of {} in either ' +
                   '{} or {}').format(password, chars[index],
                                      indices[0], indices[1]))
        else:
            print(('Password {} has NOT one of {} in either ' +
                   '{} or {}').format(password, chars[index],
                                      indices[0], indices[1]))

    return count


def print_block(line):
    """ Print block. """

    print('\n')
    print('#' * len(line))
    print(line)
    print('#' * len(line))
    print('\n')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file, 'r') as fh:
            lines = fh.readlines()
        lines = [line.strip('\n') for line in lines]

        limits, chars, pws = parse_lines(lines)

        count = validate_passwords(limits, chars, pws)

        out = ('[Task 1] Total number of acceptable ' +
               'passwords is {}').format(count)
        print_block(out)

        count = validate_passwords_2(limits, chars, pws)
        out = ('[Task 2] Total number of acceptable ' +
               'passwords is {}').format(count)
        print_block(out)
    else:
        print('Warning: No input file provided.')
