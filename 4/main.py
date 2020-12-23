""" Solution to the fourth problem of AOC (2020). """

import re
import sys


def sanitize_input(lines):
    """
    Sanitize the input into a list of strings (one per passport). An empty line
    signals a new passport.
    """

    lines_out = ['']
    for line in lines:
        if not line and lines_out[-1]:
            lines_out.append('')
            continue

        lines_out[-1] += ' ' + line.strip()

    return [line.strip() for line in lines_out]


def validate_passports(lines, require_cid=False):
    """ Find the number of valid passpoprts. """

    count = 0
    pattern = r'([a-z]+):'

    # Set up required fields
    required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    if require_cid:
        required_fields.append('cid')

    for line in lines:
        fields = re.findall(pattern, line)
        missing_fields = list(set(required_fields) - set(fields))
        if not missing_fields:
            count += 1
    return count


def validate_strict(lines):
    """ Validate strict passports. """

    count = 0
    pattern = r'([a-z]+):(\S+)'
    required_keys = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

    for line in lines:
        valid_fields = True

        pairs = re.findall(pattern, line)

        # Ignore cid
        pairs = [pair for pair in pairs if pair[0] != 'cid']

        # Check if keys are missing
        keys = [key[0] for key in pairs]
        missing_keys = list(set(required_keys) - set(keys))
        if missing_keys:
            continue

        # Check if key, value pairs are valid
        for pair in pairs:
            if not valid_field(pair[0], pair[1]):
                valid_fields = False
                break

        if valid_fields:
            count += 1

    return count


def valid_field(key, value):
    """ Validate a key, value pair. """

    # Height is special and probably best taken care of separately
    hgt_pattern = r'(\d+)(in|cm)'
    match = re.findall(hgt_pattern, value)
    if key == 'hgt' and match:
        length = int(match[0][0])
        unit = match[0][1]
        return ((150 <= length <= 193) and unit == 'cm') or \
               ((59 <= length <= 76) and unit == 'in')

    # Hair color pattern
    hcl_pattern = r'^#[0-9a-f]{6}$'

    # Eye color pattern
    ecl_pattern = r'^(amb|blu|brn|gry|grn|hzl|oth)$'

    # Passport id pattern
    pid_pattern = r'^[0-9]{9}$'

    return (key == 'byr' and (1920 <= int(value) <= 2002)) or \
           (key == 'iyr' and (2010 <= int(value) <= 2020)) or \
           (key == 'eyr' and (2020 <= int(value) <= 2030)) or \
           (key == 'hgt' and bool(re.findall(hgt_pattern, value))) or \
           (key == 'hcl' and bool(re.findall(hcl_pattern, value))) or \
           (key == 'ecl' and bool(re.findall(ecl_pattern, value))) or \
           (key == 'pid' and bool(re.findall(pid_pattern, value)))

def print_block(line):
    """ Print block. """

    print('#' * len(line))
    print(line)
    print('#' * len(line))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_in = sys.argv[1]
        with open(file_in, 'r') as fh:
            lines = fh.readlines()
        lines = [line.strip('\n') for line in lines]

        # Turn the input into a complete line per passport
        lines = sanitize_input(lines)
        print(lines)

        # Validate passports
        count = validate_passports(lines)
        print_block('[Task 1] {} valid passports found'.format(count))

        # Validate strict passports
        count = validate_strict(lines)
        print_block('[Task 2] {} valid passports found'.format(count))
