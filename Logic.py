from Game import Game
from Position import Position
import math
import random
import time

# Global variable to store memoized results
memoization_cache = {}
MAX_TIME_SECONDS = 60
# Call this function to get possible moves once per turn
def possible_move(game, player_id):
    available_sizes = set()
    available_piles = []

    for j in range(3):
        if game.player[player_id].piles[j].rocks and (
                not game.player[player_id].piles[j].rocks[-1].size in available_sizes):
            available_sizes.add(game.player[player_id].piles[j].rocks[-1].size)
            available_piles.append(j)

    moves = []
    for available_pile in available_piles:
        for j in range(4):
            for k in range(4):
                if game.is_valid(player_id, Position(j, k), None, available_pile):
                    moves.append((Position(j, k), None, available_pile))

    for i in range(4):
        for j in range(4):
            if game.grid[i][j].rocks and game.grid[i][j].rocks[-1].id == player_id:
                for k in range(4):
                    for l in range(4):
                        if game.is_valid(player_id, Position(k, l), Position(i, j), None):
                            moves.append((Position(k, l), Position(i, j), None))

    return moves


def best_move(game: Game, is_max: bool, player_id: int) -> tuple[Position, Position, int, int, int]:
    sz = 0
    p_no = 0
    f, t = 0, 0
    best_score = -math.inf
    move = None
    for to_grid, from_grid, from_pile in possible_move(game, player_id):
        game.do_turn(player_id, to_grid, from_grid, from_pile)
        score = iterative_deepening(game, is_max, player_id, to_grid, from_grid, from_pile, 1)
        game.undo_turn(player_id, to_grid, from_grid, from_pile)
        if score > best_score:
            best_score = score
            # move = (to_grid, from_grid, from_pile)

            if from_pile != None:
                sz = game.player[player_id].piles[from_pile].rocks[-1].size
                p_no = from_pile
                t = to_grid
            elif from_grid != None:
                sz = game.grid[from_grid.x][from_grid.y].rocks[-1].size
                p_no = game.grid[from_grid.x][from_grid.y].rocks[-1].pile_no
                f = from_grid

            move = (to_grid, from_grid, from_pile, p_no, sz)

    return move


def min_max(game: Game, is_max_player, player_id, to_grid, from_grid, from_pile, depth=10) -> int:
    is_game_ended, winner_id = game.check_win()
    if is_game_ended:
        return 1 if winner_id == player_id else -1
    # TODO check for draw and return 0
    if depth == 0:
        # eval = evaluation_function(
        #     game, player_id, to_grid, from_grid, from_pile)
        evaluation = -math.inf
        for to_grid, from_grid, from_pile in possible_move(game, player_id):
            evaluation = max(evaluation, evaluation_function(
                game, player_id, to_grid, from_grid, from_pile))
        return evaluation * (1 if is_max_player else -1)
    if is_max_player:
        max_val = -math.inf
        for to_grid, from_grid, from_pile in possible_move(game, player_id):
            game.do_turn(player_id, to_grid, from_grid, from_pile)
            eval = min_max(game, not is_max_player, player_id, to_grid,
                           from_grid, from_pile, depth - 1)
            max_val = max(eval, max_val)
            game.undo_turn(player_id, to_grid, from_grid, from_pile)
        print(f'max_val = {max_val}')
        return max_val

    else:
        min_val = math.inf
        for to_grid, from_grid, from_pile in possible_move(game, 1 - player_id):
            game.do_turn(1-player_id, to_grid, from_grid, from_pile)
            eval = min_max(game, not is_max_player, player_id, to_grid,
                           from_grid, from_pile, depth - 1)
            min_val = min(min_val, eval)
            game.undo_turn(1-player_id, to_grid, from_grid, from_pile)
        print(
            f'min_val = {min_val}')
        return min_val

def alpha_beta(game: Game, is_max_player, player_id, to_grid, from_grid, from_pile, depth=10, alpha=-math.inf, beta=math.inf) -> int:
    is_game_ended, winner_id = game.check_win()
    if is_game_ended:
        return 1 if winner_id == player_id else -1
    # TODO check for draw and return 0
    if depth == 0:
        evaluation = -math.inf
        for to_grid, from_grid, from_pile in possible_move(game, player_id):
            evaluation = max(evaluation, evaluation_function(
                game, player_id, to_grid, from_grid, from_pile))
        return evaluation * (1 if is_max_player else -1)
    
    if is_max_player:
        max_val = -math.inf
        for to_grid, from_grid, from_pile in possible_move(game, player_id):
            game.do_turn(player_id, to_grid, from_grid, from_pile)
            eval = alpha_beta(game, not is_max_player, player_id, to_grid,
                           from_grid, from_pile, depth - 1, alpha, beta)
            max_val = max(eval, max_val)
            alpha = max(alpha, max_val)
            game.undo_turn(player_id, to_grid, from_grid, from_pile)
            if beta <= alpha:
                break  # Beta cut-off
        return max_val

    else:
        min_val = math.inf
        for to_grid, from_grid, from_pile in possible_move(game, 1 - player_id):
            game.do_turn(1 - player_id, to_grid, from_grid, from_pile)
            eval = alpha_beta(game, not is_max_player, player_id, to_grid,
                           from_grid, from_pile, depth - 1, alpha, beta)
            min_val = min(eval, min_val)
            beta = min(beta, min_val)
            game.undo_turn(1 - player_id, to_grid, from_grid, from_pile)
            if beta <= alpha:
                break  # Alpha cut-off
        return min_val

def iterative_deepening(game: Game, is_max_player, player_id, to_grid, from_grid, from_pile, max_depth=10, alpha=-math.inf, beta=math.inf) -> int:
    # print("HELLO DEEP!")
    start_time = time.time()
    best_move = None
    for depth in range(1,max_depth+1):
        current_time = time.time()
        if current_time - start_time > MAX_TIME_SECONDS:
            print("Time limit exceeded!")
            break
        if  not best_move == None and best_move >= 70:
            print("Best move exceeds 70!")
            break
        move = alpha_beta(game, is_max_player, player_id, to_grid, from_grid, from_pile, depth, alpha, beta)
        if best_move is None or best_move<move:
            best_move = move

    return best_move

    

def evaluation_function(game: Game, player_id, to_grid: Position, from_grid: Position = None, from_pile: int = None) -> int:
    sum_row, sum_col, sum_diag, sum_anti_diag = 0, 0, 0, 0

    # Precompute frequently used values
    possible_moves = possible_move(game, player_id)
    grid_size = len(game.grid)

    # Avoid redundant validity checks by storing validated moves
    validated_moves = set()

    # Check if the result is already memoized
    key = (game, player_id, to_grid, from_grid, from_pile)
    if key in memoization_cache:
        return memoization_cache[key]

    # Handling Positive effect on Row states
    for i in range(4):
        gobblet_count = 0
        empty_count = 0
        for j in range(4):
            if game.grid[i][j].rocks and game.grid[i][j].rocks[-1].id == player_id:
                gobblet_count += 1
            elif game.is_valid(player_id, Position(i, j), from_grid, from_pile) == True:
                empty_count += 1
        if gobblet_count == 1 and empty_count == 3:
            sum_row += 1
        elif gobblet_count == 2 and empty_count == 2:
            sum_row += 10
        elif gobblet_count == 3 and empty_count == 1:
            sum_row += 100
        elif gobblet_count == 4 and empty_count == 0:
            sum_row += math.inf

    # Handling Negative effect on Row states
    for i in range(4):
        gobblet_count = 0
        empty_count = 0
        for j in range(4):
            if game.grid[i][j].rocks and game.grid[i][j].rocks[-1].id is not player_id and game.is_valid(player_id, Position(i, j), from_grid, from_pile) == False:
                gobblet_count += 1
            elif game.is_valid(player_id, Position(i, j), from_grid, from_pile) == True:
                empty_count += 1
        if gobblet_count == 1 and empty_count == 3:
            sum_row -= 1
        elif gobblet_count == 2 and empty_count == 2:
            sum_row -= 10
        elif gobblet_count == 3 and empty_count == 1:
            sum_row -= 100
        elif gobblet_count == 4 and empty_count == 0:
            sum_row -= math.inf

    for i in range(4):
        gobblet_count = 0
        empty_count = 0
        for j in range(4):
            if game.grid[j][i].rocks and game.grid[j][i].rocks[-1].id == player_id:
                gobblet_count += 1
            elif game.is_valid(player_id, Position(j, i), from_grid, from_pile) == True:
                empty_count += 1
        if gobblet_count == 1 and empty_count == 3:
            sum_col += 1
        elif gobblet_count == 2 and empty_count == 2:
            sum_col += 10
        elif gobblet_count == 3 and empty_count == 1:
            sum_col += 100
        elif gobblet_count == 4 and empty_count == 0:
            sum_col += math.inf

    for i in range(4):
        gobblet_count = 0
        empty_count = 0
        for j in range(4):
            if game.grid[j][i].rocks and game.grid[j][i].rocks[-1].id is not player_id and game.is_valid(player_id, Position(j, i), from_grid, from_pile) == False:
                gobblet_count += 1
            elif game.is_valid(player_id, Position(i, j), from_grid, from_pile) == True:
                empty_count += 1
        if gobblet_count == 1 and empty_count == 3:
            sum_col -= 1
        elif gobblet_count == 2 and empty_count == 2:
            sum_col -= 10
        elif gobblet_count == 3 and empty_count == 1:
            sum_col -= 100
        elif gobblet_count == 4 and empty_count == 0:
            sum_col -= math.inf

    # Handling Diagonal states
    pos_diag_gobblet_count = 0
    pos_diag_empty_count = 0
    for i in range(4):
        cell = game.grid[i][i]
        if cell.rocks and cell.rocks[-1].id == player_id:
            pos_diag_gobblet_count += 1
        elif game.is_valid(player_id, Position(i, i), from_grid, from_pile) == True:
            pos_diag_empty_count += 1
    if pos_diag_gobblet_count == 1 and pos_diag_empty_count == 3:
        sum_diag += 1
    elif pos_diag_gobblet_count == 2 and pos_diag_empty_count == 2:
        sum_diag += 10
    elif pos_diag_gobblet_count == 3 and pos_diag_empty_count == 1:
        sum_diag += 100
    elif pos_diag_gobblet_count == 4 and pos_diag_empty_count == 0:
        sum_diag += math.inf

    neg_diag_gobblet_count = 0
    neg_diag_empty_count = 0
    for i in range(4):
        cell = game.grid[i][i]
        if cell.rocks and cell.rocks[-1].id is not player_id and game.is_valid(player_id, Position(i, i), from_grid, from_pile) == False:
            neg_diag_gobblet_count += 1
        elif game.is_valid(player_id, Position(i, i), from_grid, from_pile) == True:
            neg_diag_empty_count += 1
    if neg_diag_gobblet_count == 1 and neg_diag_empty_count == 3:
        sum_diag -= 1
    elif neg_diag_gobblet_count == 2 and neg_diag_empty_count == 2:
        sum_diag -= 10
    elif neg_diag_gobblet_count == 3 and neg_diag_empty_count == 1:
        sum_diag -= 100
    elif neg_diag_gobblet_count == 4 and neg_diag_empty_count == 0:
        sum_diag -= math.inf

    pos_anti_diag_gobblet_count = 0
    pos_anti_diag_empty_count = 0
    # Handling anti Diagonal states
    for i in range(len(game.grid)):
        cell = game.grid[i][len(game.grid) - 1 - i]
        if cell.rocks and cell.rocks[-1].id == player_id:
            pos_anti_diag_gobblet_count += 1
        elif game.is_valid(player_id, Position(i, len(game.grid) - 1 - i), from_grid, from_pile) == True:
            pos_anti_diag_empty_count += 1
    if pos_anti_diag_gobblet_count == 1 and pos_anti_diag_empty_count == 3:
        sum_anti_diag += 1
    elif pos_anti_diag_gobblet_count == 2 and pos_anti_diag_empty_count == 2:
        sum_anti_diag += 10
    elif pos_anti_diag_gobblet_count == 3 and pos_anti_diag_empty_count == 1:
        sum_anti_diag += 100
    elif pos_anti_diag_gobblet_count == 4 and pos_anti_diag_empty_count == 0:
        sum_anti_diag += math.inf

    neg_anti_diag_gobblet_count = 0
    neg_anti_diag_empty_count = 0
    for i in range(len(game.grid)):
        cell = game.grid[i][len(game.grid) - 1 - i]
        if cell.rocks and cell.rocks[-1].id is not player_id and game.is_valid(player_id, Position(i, len(game.grid) - 1 - i), from_grid, from_pile) == False:
            neg_anti_diag_gobblet_count += 1
        elif game.is_valid(player_id, Position(i, len(game.grid) - 1 - i), from_grid, from_pile) == True:
            neg_anti_diag_empty_count += 1
    if neg_anti_diag_gobblet_count == 1 and neg_anti_diag_empty_count == 3:
        sum_anti_diag -= 1
    elif neg_anti_diag_gobblet_count == 2 and neg_anti_diag_empty_count == 2:
        sum_anti_diag -= 10
    elif neg_anti_diag_gobblet_count == 3 and neg_anti_diag_empty_count == 1:
        sum_anti_diag -= 100
    elif neg_anti_diag_gobblet_count == 4 and neg_anti_diag_empty_count == 0:
        sum_anti_diag -= math.inf

    total_weight = sum_row + sum_col + sum_diag + sum_anti_diag

    # Memoize the result before returning
    memoization_cache[key] = total_weight
    return total_weight


def Random_move(game: Game, player_id) -> tuple[Position, Position, int, int, int]:
    random_move = random.choice(possible_move(game, player_id))
    to_grid, from_grid, from_pile = random_move

    sz = 0
    p_no = 0

    if from_pile is not None:
        sz = game.player[player_id].piles[from_pile].rocks[-1].size
        p_no = from_pile
    elif from_grid is not None:
        sz = game.grid[from_grid.x][from_grid.y].rocks[-1].size
        p_no = game.grid[from_grid.x][from_grid.y].rocks[-1].pile_no

    return to_grid, from_grid, from_pile, p_no, sz
