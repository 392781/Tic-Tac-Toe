from math import inf
import os, time


def generate_moves(board):
    """
    Finds possible places to move
    
    Parameters
    ----------
    board : list
        a list length 9 containing 3x3 board positions as strings
        'x' denotes player
        'o' denotes opponent
        'e' denotes an empty space
        
    Returns
    -------
    list
        list of open spaces on the board
    """
    next_moves = []

    if(check_win(board, 'x') or check_win(board, 'o')):
        return next_moves

    for i in range(0, 9):
        if (board[i] == 'e'):
            next_moves.append(i)

    return next_moves


def minimax(board, depth, alpha, beta, isX):
    """
    Minimax algorithm with alpha-beta pruning.  
    Determines utility of a move made by the player (maximizing)
    by looking ahead to see which move the opponent will choose
    (minimizing) and then looking at the best move for the player 
    based off that move and so on and so on until 
    1. Search depth is exceeded
    2. Best/Winning move is found
    3. No more moves left to check
    
    Alpha-Beta pruning compares the maximizing parameter (alpha) 
    with the minimizing parameter (beta) to cut the search early
    
    
    Parameters
    ----------
    board : list
        a list length 9 containing 3x3 board positions as strings
        'x' denotes player
        'o' denotes opponent
        'e' denotes an empty space
    depth : int
        desired depth of the search tree
    alpha : float
        maximizing parameter, initially set to -inf
    beta : float
        minimizing parameter, initially set to inf
    isX : bool
        True if maximizing 'x'
        False if maximizing 'o'
        
    Returns
    -------
    int, int
        utility value used by minimax
        best position value for maximizing player
    """
    move_list = generate_moves(board)
    best_move = -1
    if (isX):
        player = 'x'
        utility = -inf
    else:
        player = 'o'
        utility = inf

    if (depth == 0 or not move_list or check_win(board, isX)):
        return heuristic(board), best_move
    
    for move in move_list:
        board[move] = player
        test_utility, pos = minimax(board, depth - 1, alpha, beta, not isX)
        board[move] = 'e'
        pos = move

        if(isX):
            if (test_utility > utility):
                best_move = pos
                utility = test_utility
            alpha = max(utility, alpha)
        else:
            if (test_utility < utility):
                best_move = pos
                utility = test_utility
            beta = min(utility, beta)
        
        if(alpha >= beta):
            break
    
    return utility, best_move


def heuristic(board):
    """
    Heuristic used to determine utility of board.
    Board is scored by the following:
    
    +100/-100 if 3 values are in a row
    +10/-10 if 2 values are in a row with an empty space
    +1/-1 if 1 value is found with 2 empty spaces
    
    Parameters
    ----------
    board : list
        a list length 9 containing 3x3 board positions as strings
        'x' denotes player
        'o' denotes opponent
        'e' denotes an empty space
    
    Returns
    -------
    int
        utility value of the board
    """
    score = 0
    _3row = ['xxx', 'ooo']
    _2row = ['xxe', 'exx', 'ooe', 'eoo']
    _1row = ['xee', 'exe', 'eex', 'oee', 'eoe', 'eeo']

    line_index = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                  [2, 5, 8], [1, 4, 7], [0, 3, 6],
                  [0, 4, 8], [2, 4, 6]]

    for line in line_index:
        tst_str = ''
        for i in line:
            tst_str += board[i]

        if (tst_str in _3row):
            if (tst_str.count('x') >= 1):
                score += 100
            else:
                score -= 100
        elif(tst_str in _2row):
            if (tst_str.count('x') >= 1):
                score += 10
            else:
                score -= 10
        elif(tst_str in _1row):
            if (tst_str.count('x') >= 1):
                score += 1
            else:
                score -= 1
    return score 
            

def check_win(board, player):
    """
    Checks whether the game is won by the current player
    
    Parameters
    ----------
    board : list
        a list length 9 containing 3x3 board positions as strings
        'x' denotes player
        'o' denotes opponent
        'e' denotes an empty space
    player : string
        'x' for player
        'o' for opponent
        
    Returns
    -------
    bool
        True if game is won, False if game is lost
    """
    test_board = board
    
    if (
        (board[0] == player and board[1] == player and board[2] == player) or
        (board[3] == player and board[4] == player and board[5] == player) or
        (board[6] == player and board[7] == player and board[8] == player) or        
        (board[0] == player and board[3] == player and board[6] == player) or        
        (board[1] == player and board[4] == player and board[7] == player) or
        (board[2] == player and board[5] == player and board[8] == player) or
        (board[0] == player and board[4] == player and board[8] == player) or
        (board[6] == player and board[4] == player and board[2] == player)
        ):
        return True
    else:
        return False


def print_board(board):
    """
    Helper method to pretty print the game board in the
    following format:
     1 | 2 | 3
    ---+---+---
     4 | 5 | 6
    ---+---+---
     7 | 8 | 9
       
    Parameters
    ----------
    board : list
        a list length 9 containing 3x3 board positions as strings
        'x' denotes player
        'o' denotes opponent
        'e' denotes an empty space
    """
    for i in range(0, 9):
        if(i == 8):
            string = '\n'
        elif (i % 3 == 2):
            string = '\n---+---+--- \n'
        else:
            string = '|'

        if (board[i] in 'xoXO'):
            print(f" {board[i]} ", end = string)
        else:
            print(f" {i+1} ", end = string)   


def main():
    # Initialize gameboard
    board = ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e']
    print("Tic Tac Toe by Ron")
    player = ' '

    # Let user choose which player they'd like to be
    while (player not in 'xXoO'):
        player = input("X/O? ")

        if (player not in 'xXoO'):
            print("Please choose and try again: x/o/X/O")

        player = player.lower()

    # Sets playing parameters and clears console
    if (player == 'x'):
        player = 'x'
        opp = 'o'
        isX = False
        os.system('cls' if os.name == 'nt' else 'clear')
        print_board(board)
    elif (player == 'o'):
        player = 'o'
        opp = 'x'
        isX = True
        board[4] = opp
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Opponent move: 4")
        print_board(board)
    else:
        exit()

    # Begin game until Win or Tie is found
    while((not check_win(board, player) and not check_win(board, opp)) and ('e' in ''.join(board))):
        # Player inputs a move on the board
        # If input is invalid, game exits (Could be handled better)
        move = input("Player move [1 - 9]? ")
        try:
            move = int(move)
            move = move - 1
        except(ValueError or TypeError):
            print("invalid input")
            exit()

        # Place the player move, clear console, find AI move, print board
        # Else, try getting a move again
        if (board[move] == 'e' and move in range(0, 9)):
            board[move] = player
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Player move:   ", move + 1)
            if ('e' in ''.join(board)):
                move = minimax(board, 100, -inf, inf, isX)[1]
                board[move] = opp
                print("Opponent move: ", move + 1)
            print_board(board)
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Player invalid move: ", move + 1)
            print_board(board)
            print("Invalid move, try again [1 - 9]? ")
    
    # Check who won the game
    if (check_win(board, player)):
        print("You won! Congrats!")
    elif(check_win(board, opp)):
        print("You failed and skyneTTT took over the world")
    else:
        print("You tied, you're only as good as the AI")
        
    # Exit after 3 seconds
    time.sleep(0.5)
    print("Exiting in...")
    for i in range(-3,0):
        time.sleep(1)
        i *= -1
        print(f"{i}...")

# Call main
main()
