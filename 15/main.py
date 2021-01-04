""" Solution to the 15th AOC of 2020. """


from collections import deque
from sys import argv


def play_game(numbers, turns):
    """
    Play the game using provided initial numbers.
    Return the 2020th number.
    """

    # Let board be a dict of a played number and the two last time it came up
    turn = 1
    board = {}

    # Play the initial numbers
    for number in numbers:
        if number in board:
            board[number].append(turn)
        else:
            board[number] = deque([None, turn], maxlen=2)
        turn += 1


    # Play the game
    number = numbers[-1]
    while turn <= turns:
        if number in board:
            if all(board[number]):
                number = board[number][1] - board[number][0]
                if number in board:
                    board[number].append(turn)
                else:
                    board[number] = deque([None, turn], maxlen=2)
            else:
                number = 0
                if number in board:
                    board[number].append(turn)
                else:
                    board[number] = deque([None, turn], maxlen=2)

        else:
            number = 0
            if number in board:
                board[number].append(turn)
            else:
                board[number] = deque([None, turn], maxlen=2)

        turn += 1

    return number


if __name__ == "__main__":
    file_in = argv[1]
    with open(file_in, 'r') as fh:
        line = fh.readline().rstrip()
    init_numbers = list(map(int, line.split(",")))

    ans = play_game(init_numbers, 2020)
    print("[Task 1] 2020th number is: {}".format(ans))

    ans = play_game(init_numbers, 30000000)
    print("[Task 2] 2020th number is: {}".format(ans))
