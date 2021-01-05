""" Solution to the 18th AOC of 2020. """

import re

from sys import argv

def get_parenthesis_body(line):
    """ Return the body of the outermost parenthesis. """

    # The opening parenthesis is at index 0
    lower = 1

    depth = 0
    for upper, char in enumerate(line[lower:]):
        if char == '(':
            depth += 1
        elif char == ')' and depth > 0:
            depth -= 1
        elif char == ')' and depth == 0:
            return line[lower:upper+1], line[upper+2:]

def calculate(line):
    """ Execute the calculation. """

    #import pudb; pu.db

    # Check if we are at a single integer
    try:
        return int(line)
    except ValueError:
        pass

    # Check if we can carry out a simple calculation
    match = re.match(r'^(\d+) ([*+]) (.*)', line)
    if match:
        lhs = int(match.group(1))
        operator = match.group(2)
        remainder = match.group(3)
        if operator == '*':
            return lhs * calculate(remainder)
        elif operator == '+':
            return lhs + calculate(remainder)
    elif line[0] == '(':
        body, tail = get_parenthesis_body(line)
        return calculate(str(calculate(body)) + tail)


def calc_flipped_precedence(line):
    """
    An orthodox solution for this one. Override the __add__ and __mul__ to be
    flipped for a new class and replace the * and + characters in the string.
    """

    class _():
        """ Class with reversed + and * operators. """
        def __init__(self, value):
            """ Constructor for flipped operator class. """
            self.value = value
        def __add__(self, other):
            """ Replaced with multiplication. """
            return _(self.value * other.value)
        def __mul__(self, other):
            """ Replaced with addition. """
            return _(self.value + other.value)
        def __str__(self):
            """ Print the value. """
            return str(self.value)
        def __int__(self):
            """ Return the value. """
            return self.value

    line_ = line

    # Replace integers with _() calls
    line = re.sub(r'(\d+)', r'_(\1)', line)

    # Let + become * and * become +
    line = line.replace('*', '#')
    line = line.replace('+', '*')
    line = line.replace('#', '+')

    # Evaluate the expression
    val = eval(line)
    return int(val)


if __name__ == "__main__":
    file_in = argv[1]
    with open(file_in, 'r') as fh:
        lines = [line.rstrip() for line in fh.readlines()]

    s = 0
    for line in lines:
        line_ = line[::-1]
        line_ = line_.replace('(', '#')
        line_ = line_.replace(')', '(')
        line_ = line_.replace('#', ')')
        s += calculate(line_)
    print("[Task 1] Sum is: {}".format(s))

    s = 0
    for line in lines:
        s += calc_flipped_precedence(line)
    print("[Task 2] Sum is: {}".format(s))
