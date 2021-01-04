""" Solution to the 16th AOC of 2020. """

import re

from sys import argv


class Validator:
    """ Class for validating tickets. """

    def __init__(self):
        """ Constructor for ticket validating class. """

        self.intervals = {}

    def add_string_interval(self, string):
        """
        Convert a string of the format

            class: 1-3 or 5-7

        to the two intervals 1-3 and 5-7.
        """

        name = string[: string.index(":")]
        intervals = re.findall(r"(\d+-\d+)", string)

        self.intervals[name] = []
        for interval in intervals:
            self.intervals[name].append(tuple(map(int, interval.split("-"))))

    def validate_ticket(self, ticket):
        """
        Parse a ticket (as a list of numbers) and return all fields which
        violate an interval.
        """
        violations = []
        for field in ticket:
            accepted = False
            for intervals in self.intervals.values():
                if any(
                    [
                        1 if lower <= field <= upper else 0
                        for lower, upper in intervals
                    ]
                ):
                    accepted = True

            if not accepted:
                violations.append(field)
        return violations

    def valid_ticket(self, ticket):
        """ Return true if a ticket is valid. """
        return not self.validate_ticket(ticket)

    def get_interval_names(self):
        """ Return the interval names. """
        return list(self.intervals.keys())


def separate_lines(lines):
    """ Separate lines into intervals, your ticket and other tickets. """

    your_ticket = lines.index("your ticket:")
    nearby_tickets = lines.index("nearby tickets:")

    return (
        lines[0 : your_ticket - 1],
        list(map(int, lines[your_ticket + 1].split(","))),
        [
            list(map(int, line.split(",")))
            for line in lines[nearby_tickets + 1 :]
        ],
    )


def validate_tickets(intervals, tickets):
    """ Validate the tickets using intervals. """

    validator = Validator()
    for interval in intervals:
        validator.add_string_interval(interval)

    violation_sum = 0
    valid_tickets = []
    for ticket in tickets:
        violations = validator.validate_ticket(ticket)
        violation_sum += sum(violations)
        if not violations:
            valid_tickets.append(ticket)

    return violation_sum, valid_tickets


def identify_fields(intervals, tickets, your_ticket):
    """ Identify the fields for each column. """

    candidates = {}
    for column in range(len(tickets[0])):
        ticket = [fields[column] for fields in tickets]

        for interval in intervals:
            validator = Validator()
            validator.add_string_interval(interval)

            if validator.valid_ticket(ticket):
                # Take the first index since there is only one interval
                if column in candidates:
                    candidates[column].extend(validator.get_interval_names())
                else:
                    candidates[column] = validator.get_interval_names()

    assignments = {}
    for index, candidate in sorted(candidates.items(), key=lambda x: len(x[1])):
        candidate = list(
            set(candidate) - set([x for _, x in assignments.items()])
        )
        assignments[index] = candidate[0]

    product = 1
    for key, value in assignments.items():
        if "departure" in value:
            print(value)
            product *= your_ticket[key]

    return product


if __name__ == "__main__":
    file_in = argv[1]
    with open(file_in, "r") as fh:
        lines = [line.rstrip() for line in fh.readlines()]

    intervals, your_ticket, nearby_tickets = separate_lines(lines)

    error_rate, valid_tickets = validate_tickets(intervals, nearby_tickets)
    print("[Task 1] Ticket scanning error rate: {}".format(error_rate))

    product = identify_fields(intervals, valid_tickets, your_ticket)
    print("[Task 2] Product is: {}".format(product))
