from math import inf
import socket
import random


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
    ip = 'www.dagertech.net'
    port = 3800
    connection = (ip, port)

    s = socket.socket()

    print(f"Connecting to {ip}:{port}...", end="", flush=True)

    # Open connection
    s.connect(connection)
    s.settimeout(1)
    
    ### Start
    ### CharPrompt
    try:
        print(s.recv(1024).decode(), end="")
        print(s.recv(1024).decode(), end="")
    except socket.timeout:
        pass

    player = ''
    opp = ''
    x_o = random.randint(0, 2)
    if (x_o == 0):
        player = 'x'
        opp = 'o'
        isX = True
    else:
        player = 'o'
        opp = 'x'
        isX = False

    s.send(str.encode(player))
    print(player)
    
    # Prepares variables
    message = ' '
    end = False
    message_stack = []
    board = ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e']
    cont_counter = 0
 
    while (not end):

        # If the list of messages is empty, receive, else move on
        if (not message_stack):
            s.settimeout(1)
            try:
                message = s.recv(64).decode()
            except socket.timeout:
                pass
        
        # Splits the message into lines to be added to a stack
        if (message is not None):
            message_split = message.split('\n')
            message_stack.extend(message_split)
        
        # Resets receiver variables for next server receive and parse
        message = None
        message_split = None

        # Try to pop a line off the stack
        # If a line can't be popped more than 5 times, something is wrong
        try:
            message_line = message_stack.pop(0)
            while (message_line is ''):
                message_line = message_stack.pop(0)
        except IndexError:
            if (cont_counter > 4):
                message_line = 'No longer receiving messages'
                pass
            cont_counter += 1
            continue

        ##### BEGIN STATE CHECK

        ### Format Print 9CHRBOARD
        if (len(message_line) == 9 and 'Tie' not in message_line):
            board = list(message_line.lower()) 

            for i in range(0, 9):
                if (board[i] in '123456789'):
                    board[i] = 'e'

            print_board(board)
        
        ### ClientMove
        elif ('Client' in message_line):
            print(message_line, end = ' ')

            if (''.join(board) in 'eeeeeeeee'):
                possible_moves = [0]
                move = 4
            else:
                move = minimax(board, 100, -inf, inf, isX)[1]

            board[move] = player
            s.send(str.encode(str(move + 1)))
            print(move + 1)
        
        ### SvrMove
        elif ('Server' in message_line):
            print(message_line)
            message_line = list(message_line)
            pos = int(message_line[-1])
            board[pos - 1] = opp

        ### Winner
        elif ('Win' in message_line or 'Tie' in message_line):
            print(message_line)

        ### Final
        elif ('Disconnecting' in message_line):
            print(message_line)
            end = True

        ### ERROR
        elif ('Error' in message_line):
            print(message_line)
            s.close()
            exit()
        
        ## CLIENT ERROR
        else:
            print("CLIENT SIDE ERROR MESSAGE: ", list(message_line))
            print(message_stack)
            s.close()
            exit()
        
        # Reset message_line for future use
        message_line = None

    # Close connection
    s.close()

main()
