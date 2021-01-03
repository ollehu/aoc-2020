""" Solution to the 12th of 2020's AOC. """

import numpy as np

from enum import Enum
from sys import argv


class Heading(Enum):
    """ Enum for headings -> normalized vector in that direction. """

    N = [0, 1]
    E = [1, 0]
    S = [0, -1]
    W = [-1, 0]


class Ship:
    """ Ship class for tracking direction, position and movement. """

    def __init__(self, use_wp=False, wp_x=0, wp_y=0):
        """
        Initialize the ship in the default position (0, 0) facing east.
        The waypoint's position is relative to the ship.
        """

        self.pos = np.array([0, 0])
        self.heading = np.array(Heading.E.value, dtype="i")
        self.use_wp = use_wp
        if self.use_wp:
            self.wp_pos = np.array([wp_x, wp_y])

    def forward(self, distance):
        """ Move forward 'distance' number of coordinates. """

        if self.use_wp:
            self.pos += distance * self.wp_pos
        else:
            self.pos += distance * self.heading

    def steer_port(self, degrees):
        """
        Steer to port, degrees is assumed to be a positive right angle.

        If self.use_wp, then instead move the wp relative to the ship.
        """

        if degrees % 90 or degrees < 0:
            raise ValueError("Invalid port turn provided.")

        rot_matrix = self.calc_rotation_matrix(degrees)

        if self.use_wp:
            self.wp_pos = np.matmul(rot_matrix, self.wp_pos)
            # Resolve numerical issues.
            self.wp_pos = self.wp_pos.round().astype("i")
        else:
            self.heading = np.matmul(rot_matrix, self.heading)
            # Resolve numerical issues.
            self.heading = self.heading.round().astype("i")
        return 0

    def steer_starboard(self, degrees):
        """
        Steer to port, degrees is assumed to be a positive right angle.

        If self.use_wp, then instead move the wp relative to the ship.
        """

        if degrees % 90 or degrees < 0:
            raise ValueError("Invalid starboard turn provided.")

        rot_matrix = self.calc_rotation_matrix(-degrees)

        if self.use_wp:
            self.wp_pos = np.matmul(rot_matrix, self.wp_pos)
            # Resolve numerical issues.
            self.wp_pos = self.wp_pos.round().astype("i")
        else:
            self.heading = np.matmul(rot_matrix, self.heading)
            # Resolve numerical issues.
            self.heading = self.heading.round().astype("i")
        return 0

    def compass_move(self, heading, distance):
        """
        Move a distance in a compass heading (not changing the boat's
        heading).
        """

        if self.use_wp:
            self.wp_pos += np.array(heading, dtype="i") * distance
        else:
            self.pos += np.array(heading, dtype="i") * distance

    def move(self, action, amount):
        """ Move according to the rules provided. """

        if action == "N":
            self.compass_move(Heading.N.value, amount)
        elif action == "E":
            self.compass_move(Heading.E.value, amount)
        elif action == "S":
            self.compass_move(Heading.S.value, amount)
        elif action == "W":
            self.compass_move(Heading.W.value, amount)
        elif action == "L":
            self.steer_port(amount)
        elif action == "R":
            self.steer_starboard(amount)
        elif action == "F":
            self.forward(amount)
        else:
            raise KeyError("Action mapping not found.")

    def get_position(self):
        """ Return the position. """

        return self.pos

    def get_heading(self):
        """ Return the heading. """

        return self.heading

    @classmethod
    def calc_rotation_matrix(cls, degrees):
        """
        Return a rotation matrix by rotating 'degrees' number of degrees
        clockwise.
        """

        rad = np.deg2rad(degrees)
        return np.array(
            [[np.cos(rad), -np.sin(rad)], [np.sin(rad), np.cos(rad)]]
        )


def parse_instructions(lines):
    """ Parse the strings into instructions (character, amount). """

    instructions = []
    for line in lines:
        try:
            instructions.append((line[0], int(line[1:])))
        except ValueError:
            print("Could not parse line {}".format(line))
            exit(1)

    return instructions


def execute_instructions(instructions, use_wp=False, wp_x=0, wp_y=0):
    """
    Execute the instructions and return the Manhattan distance from (0, 0).
    """

    ship = Ship(use_wp=use_wp, wp_x=wp_x, wp_y=wp_y)
    for instruction in instructions:
        ship.move(instruction[0], instruction[1])

    pos = ship.get_position()

    return np.sum(np.abs(pos))


if __name__ == "__main__":
    file_in = argv[1]
    with open(file_in, "r") as fh:
        lines = fh.readlines()
    lines = [line.strip("\n") for line in lines]

    instructions = parse_instructions(lines)

    distance = execute_instructions(instructions)
    print("[Task 1] The Manhattan distance is: {}".format(distance))

    distance = execute_instructions(instructions, use_wp=True, wp_x=10, wp_y=1)
    print("[Task 2] The Manhattan distance is: {}".format(distance))
