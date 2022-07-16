"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    count = 0

    # For each cell X = +1, O = -1
    for row in board:
        for cell in row:

            if cell == X:
                count += 1

            elif cell == O:
                count -= 1

    # If more Xs than Os.
    # X starts the game -> if 0 return X
    if count > 0:
        return O
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # Create set of possible actions
    possible_actions = set()

    # Loop for every cell
    for i in range(len(board)):
        for j in range(len(board[i])):

            # If cell is empty add action
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))

    # Return action list
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # Raise error when action is not possible
    if action not in actions(board):
        raise Exception("This move is not allowed!")

    # Copy board into cpy
    cpy = copy.deepcopy(board)

    # Alternative:
    # cpy = []
    # for row in board:
    #     r = []
    #     for cell in row:
    #         r.append(cell)
    #     cpy.append(r)

    # Set board cell -> symbol of current player
    cpy[action[0]][action[1]] = player(board)
    return cpy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Loop all X and Y possible wins
    for i in range(3):

        # If mutual cell is not empty
        if board[i][i] is not EMPTY:

            # Rows
            if board[i][0] == board[i][1] and board[i][2] == board[i][1]:
                return board[i][i]

            # Columns
            if board[0][i] == board[1][i] and board[2][i] == board[1][i]:
                return board[i][i]

    # Diagonals
    # If middle is not empty check diagonals
    if board[1][1] is not EMPTY:

        # Left-Top to Right-Bottom
        if board[0][0] == board[1][1] and board[2][2] == board[1][1]:
            return board[1][1]

        # Left-Bottom to Right-Top
        if board[0][2] == board[1][1] and board[2][0] == board[1][1]:
            return board[1][1]

    # No win
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # If someone has won
    if winner(board) is not None:
        return True

    # If any cell is empty
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False

    # Otherwise (Tie)
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    # Get winner
    v_winner = winner(board)

    # If X won
    if v_winner == X:
        return 1

    # If O won
    if v_winner == O:
        return -1

    # Tie or still playing
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # Just to be sure board is not terminal
    if terminal(board):
        return None

    # Return only best action
    return alpha_beta(board)[1]


def alpha_beta(state, alpha=-math.inf, beta=math.inf):
    """
    Alpha Beta Pruning recursive helper function.
    """

    # Return value when terminal
    if terminal(state):
        return [utility(state), None]

    # Create boolean variable to maximize or minimize
    maximize = True
    if player(state) == O:
        maximize = False

    optimal_action = None

    # If minimizing start from infinity else start from -infinity
    action_value = math.inf
    if maximize:
        action_value = -math.inf

    # For possible actions on the board state -> get deeper state and handle it
    for action in actions(state):

        # Run self with result of action and get value
        child = result(state, action)
        child_value = alpha_beta(child, alpha, beta)[0]

        # When Maximizing
        if maximize:
            alpha = max(alpha, child_value)

            # If child value is more than this value
            if child_value > action_value:
                action_value = child_value
                optimal_action = action

        # When Minimizing
        else:
            beta = min(beta, child_value)

            # If child value is less than this value
            if child_value < action_value:
                action_value = child_value
                optimal_action = action

        # Cut unimportant tree
        if alpha >= beta:
            break

    # Return value of action, and action
    return [action_value, optimal_action]