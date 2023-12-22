from Logic import evaluate, is_moves_left, player, opponent
import math
import random

MAX_DEPTH = 3
WIN_SCORE = 10
LOSE_SCORE = -10


def alpha_beta_pruning(board, depth, alpha, beta, is_max):
    score = evaluate(board)
    
    if depth > MAX_DEPTH or score == WIN_SCORE or score == LOSE_SCORE:
        return score
    
    if not is_moves_left(board):
        return 0

    if is_max:
        best = -math.inf

        for i in range(4):
            for j in range(4):
                if board[i][j] == 0:
                    board[i][j] = player
                    val = alpha_beta_pruning(board, depth + 1, alpha, beta, not is_max)
                    best = max(best, val)
                    alpha = max(alpha, best) # Update alpha
                    board[i][j] = 0

                    if beta <= alpha:
                        break # Prune

        return best

    else:
        best = math.inf

        for i in range(4):
            for j in range(4):
                if board[i][j] == 0:
                    board[i][j] = opponent
                    val = alpha_beta_pruning(board, depth + 1, alpha, beta, not is_max)
                    best = min(best, val)
                    beta = min(beta, best)
                    board[i][j] = 0

                    if beta <= alpha:
                        break

        return best
    
def best_move(board):
    best_val = -math.inf
    best_move = (-1, -1)
    alpha = -math.inf
    beta = math.inf

    # Get a list of available moves
    available_moves = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]

    # Shuffle the list of available moves
    random.shuffle(available_moves)

    for move in available_moves:
        i, j = move
        board[i][j] = player
        move_val = alpha_beta_pruning(board, 0, alpha, beta, False)
        board[i][j] = 0

        if move_val > best_val:
            best_move = (i, j)
            best_val = move_val

    print("The value of the best move is:", best_val)
    return best_move

def is_tie(board):
    for row in board:
        for cell in row:
            if cell == 0:
                return False
    return True

def print_board(board):
    for row in board:
        print(row)

def get_opponent_move(board):
    try:
        print("Enter opponent's move (row and column, space-separated): ")
        move = input().split()
        row, col = map(int, move)
        if board[row][col] == 0:
            board[row][col] = opponent
        else:
            print("Invalid move. Cell already occupied. Try again.")
            get_opponent_move(board)
    except (ValueError, IndexError):
        print("Invalid input. Please enter two integers representing row and column.")
        get_opponent_move(board)


# Example usage:
if __name__ == "__main__":
    board_4x4 = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    print("Initial Board:")
    print_board(board_4x4)

    while True:
        best_move_4x4 = best_move(board_4x4)

        print("\nAfter the Optimal Move:")
        board_4x4[best_move_4x4[0]][best_move_4x4[1]] = player
        print_board(board_4x4)

        print("\nThe Optimal Move is:")
        print("ROW:", best_move_4x4[0], " COL:", best_move_4x4[1])

        if evaluate(board_4x4) == WIN_SCORE:
            print("Player wins!")
            break
        elif is_tie(board_4x4):
            print("It's a tie!")
            break

        get_opponent_move(board_4x4)
        print("\nAfter Opponent's Move:")
        print_board(board_4x4)

        if evaluate(board_4x4) == LOSE_SCORE:
            print("Opponent wins!")
            break
        elif is_tie(board_4x4):
            print("It's a tie!")
            break

