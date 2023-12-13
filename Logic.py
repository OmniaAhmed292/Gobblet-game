player, opponent = 1,2

def is_moves_left(board):
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return True
    return False

def evaluate(b):
    for row in range(4):
        if all(b[row][col] == player for col in range(4)):
            return 10
        elif all(b[row][col] == opponent for col in range(4)):
            return -10

    for col in range(4):
        if all(b[row][col] == player for row in range(4)):
            return 10
        elif all(b[row][col] == opponent for row in range(4)):
            return -10

    if all(b[i][i] == player for i in range(4)):
        return 10
    elif all(b[i][i] == opponent for i in range(4)):
        return -10

    if all(b[i][3 - i] == player for i in range(4)):
        return 10
    elif all(b[i][3 - i] == opponent for i in range(4)):
        return -10

    return 0

def minimax(board, depth, is_max):
    score = evaluate(board)
    if depth > 3:
        return depth

    if score == 10:
        return score

    if score == -10:
        return score

    if not is_moves_left(board):
        return 0

    if is_max:
        best = -1000

        for i in range(4):
            for j in range(4):
                if board[i][j] == 0:
                    board[i][j] = player
                    best = max(best, minimax(board, depth + 1, not is_max))
                    board[i][j] = 0

        return best

    else:
        best = 1000

        for i in range(4):
            for j in range(4):
                if board[i][j] == 0:
                    board[i][j] = opponent
                    best = min(best, minimax(board, depth + 1, not is_max))
                    board[i][j] = 0

        return best

def find_best_move(board):
    best_val = -1000
    best_move = (-1, -1)

    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                board[i][j] = player
                move_val = minimax(board, 0, False)
                board[i][j] = 0

                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val

    print("The value of the best move is:", best_val)
    print()
    return best_move

# Example usage:
board_4x4 = [
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0]
]

best_move_4x4 = find_best_move(board_4x4)

print("The Optimal Move is:")
print("ROW:", best_move_4x4[0], " COL:", best_move_4x4[1])

