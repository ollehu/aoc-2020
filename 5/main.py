""" Solution to the fifth AOC problem of 2020. """

import sys


N_ROW_CHARS = 7
N_COL_CHARS = 3

ROW_UPPER = 127
COL_UPPER = 7

def parse_lines(lines):
    """ Parse the lines and print the largest seat ID. """

    # Seat IDs are by definition positive
    maximum_seat_id = 0
    seat_ids = []

    for line in lines:
        row_chars = line[:N_ROW_CHARS]
        columns_chars = line[-N_COL_CHARS:]

        row = find_position(row_chars, 0, ROW_UPPER)
        column = find_position(columns_chars, 0, COL_UPPER)
        seat_id = row * 8 + column
        seat_ids.append(seat_id)

        # Update maximum seat ID
        maximum_seat_id = max([maximum_seat_id, seat_id])

        print('{}: row {}, column {}, seat ID {}'.format(line, row, column,
                                                         seat_id))

    print('Maximum seat ID: {}'.format(maximum_seat_id))

    missing_seats = list(set(range(ROW_UPPER * 8 + COL_UPPER + 1)) - \
            set(seat_ids))
    missing_seats = [seat for seat in missing_seats if (seat + 1) in \
                     seat_ids and (seat - 1) in seat_ids]

    print('Missing ID(s): {}'.format(', '.join(map(str, missing_seats))))


def find_position(chars, lower, upper):
    """ Recusrively determine the position for a passenger. """

    if lower == upper:
        return lower
    elif chars[0] in ['F', 'L']:
        return find_position(chars[1:], lower, (upper - lower) // 2 + lower)
    elif chars[0] in ['B', 'R']:
        return find_position(chars[1:], upper - (upper - lower) // 2, upper)
    else:
        print("Warning, unidentified character.")
        raise ValueError


if __name__ == '__main__':
    file_in = sys.argv[1]
    with open(file_in, 'r') as fh:
        lines = fh.readlines()
    lines = [line.strip('\n') for line in lines]
    parse_lines(lines)
