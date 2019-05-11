from math import inf
import os


def choose_move(board, depth, isX):
    if (isX):
        score_val = -inf
    else:
        score_val = inf
    move = minimax(board, depth, -inf, inf, isX)

    return move[1]


def generate_moves(board):
    next_moves = []

    if(check_win(board, 'x') or check_win(board, 'o')):
        return next_moves

    for i in range(0, 9):
        if (board[i] == 'e'):
            next_moves.append(i)

    return next_moves


def minimax(board, depth, alpha, beta, isX):
    best_move = -1
    if (isX):
        player = 'x'
        utility = -inf
    else:
        player = 'o'
        utility = inf

    if (depth == 0 or check_win(board, isX)):
        return heuristic(board), best_move
    
    for move in generate_moves(board):
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
    board = ['e','e','e','e','e','e','e','e','e']
    print("Tic Tac Toe by Ron")
    player = ' '

    while (player not in 'xXoO'):
        player = input("X/O? ")

        if (player not in 'xXoO'):
            print("Please choose and try again: x/o/X/O")

        player = player.lower()

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

    while((not check_win(board, player) and not check_win(board, opp)) and ('e' in ''.join(board))):
        move = input("Player move [1 - 9]? ")
        try:
            move = int(move)
            move = move - 1
        except(ValueError or TypeError):
            print("invalid input")
            exit()

        if (board[move] == 'e' and move in range(0, 9)):
            board[move] = player
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Player move:   ", move + 1)
            move = minimax(board, 100, -inf, inf, not isX)[1]
            board[move] = opp
            print("Opponent move: ", move + 1)
            print_board(board)
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Player invalid move: ", move + 1)
            print_board(board)
            print("Invalid move, try again [1 - 9]? ")

    if (check_win(board, player)):
        print("You won! Congrats!")
    elif(check_win(board, opp)):
        print("You failed and skyneTTT took over the world")
    else:
        print("You tied, you're only as good as the AI")
        

main()