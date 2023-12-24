from Game import Game
from Postion import Postion
import math

def possible_move(self, player_id: int) -> list[tuple[Postion, Postion, int]]:  # to_grid, from_grid, from_pile

    available_sizes = set()
    available_piles = []
    idx = -1
    for j in range(3):
        if self.player[player_id].piles[j].rocks and (
                not self.player[player_id].piles[j].rocks[-1].size in available_sizes):
            available_sizes.add(self.player[player_id].piles[j].rocks[-1].size)
            available_piles.append(j)

    for element in available_sizes:
        idx += 1
        for j in range(4):
            for k in range(4):
                if(self.is_valid(player_id, Postion(j, k), None, available_piles[idx])):
                    yield Postion(j, k), None, available_piles[idx]


    for (i) in range(4):
        for (j) in range(4):
            if self.grid[i][j].rocks and self.grid[i][j].rocks[-1].id == player_id:
                for k in range(4):
                    for l in range(4):
                       if(self.is_valid(player_id, Postion(k, l), Postion(i, j), None)):
                           yield  Postion(k, l), Postion(i, j), None

def best_move(game: Game, player_id: int, default_depth=1) -> tuple[Postion, Postion, int,int, int]:
    best_move_size = 0
    best_move_pile_no = 0
    best_move_from_grid = 0
    best_move_to_grid = 0
    best_score = -math.inf
    selected_move = None

    for to_grid, from_grid, from_pile in possible_move(game, player_id):
        game.do_turn(player_id, to_grid, from_grid, from_pile)
        score = min_max(game, False, player_id, default_depth)
        game.undo_turn(player_id, to_grid, from_grid, from_pile)

        if score > best_score:
            best_score = score

            if from_pile is not None:
                best_move_size = game.player[player_id].piles[from_pile].rocks[-1].size
                best_move_pile_no = from_pile
                best_move_to_grid = to_grid
            elif from_grid is not None:
                best_move_size = game.grid[from_grid.x][from_grid.y].rocks[-1].size
                best_move_pile_no = game.grid[from_grid.x][from_grid.y].rocks[-1].pile_no
                best_move_from_grid = from_grid

            selected_move = (best_move_to_grid, best_move_from_grid, best_move_pile_no, best_move_size)

    return selected_move

def min_max(game: Game, is_max_player, player_id, depth=10) -> int:
    is_game_ended, winner_id = game.check_win()
    
    if is_game_ended:
        return 1 if winner_id == player_id else -1
    
    #TODO check for draw and return 0
    if depth == 0:
        evaluation = -999
        for to_grid, from_grid, from_pile in possible_move(game, int(is_max_player)):
            evaluation = max(evaluation, evaluation_function(game, int(is_max_player), to_grid, from_grid, from_pile))
        return evaluation*(1 if is_max_player else -1)
    
    if is_max_player:
        returned_value = -999
        for to_grid, from_grid, from_pile in possible_move(game, player_id):
            game.do_turn(player_id, to_grid, from_grid, from_pile)
            returned_value = max(returned_value, min_max(game, False, player_id, depth - 1))
            game.undo_turn(player_id, to_grid, from_grid, from_pile)

    else:
        returned_value = 999
        for to_grid, from_grid, from_pile in possible_move(game, 1 - player_id):
                game.do_turn(1-player_id, to_grid, from_grid, from_pile)
                returned_value = min(returned_value, min_max(game, True, player_id, depth - 1))
                game.undo_turn(1-player_id, to_grid, from_grid, from_pile)
    return returned_value

def evaluation_function(game: Game, player_id, to_grid: Postion, from_grid: Postion = None, from_pile: int = None) -> int:
    row = to_grid.x
    col = to_grid.y
    sum_row = 0
    sum_col = 0
    sum_diag = 0
    sum_anti_diag = 0
    sum = 0

    # Handling Positive effect on Row states
    for i in range(4):
        gobblet_count = 0
        empty_count = 0
        for cell in game.grid[i]:
            if cell.rocks and cell.rocks[-1].id == player_id:
                gobblet_count += 1
            elif not cell.rocks:
                empty_count += 1
        if gobblet_count == 1 and empty_count == 3:
            sum += 1
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
        for cell in game.grid[i]:
            if cell.rocks and cell.rocks[-1].id is not player_id:
                gobblet_count += 1
            elif not cell.rocks:
                empty_count += 1
        if gobblet_count == 1 and empty_count == 3:
            sum -= 1
        elif gobblet_count == 2 and empty_count == 2:
            sum_row -= 10
        elif gobblet_count == 3 and empty_count == 1:
            sum_row -= 100
        elif gobblet_count == 4 and empty_count == 0:
            sum_row -= math.inf

    for i in range(4):
        gobblet_count = 0
        empty_count = 0
        for cell in game.grid[i]:
            if cell.rocks and cell.rocks[-1].id == player_id:
                gobblet_count += 1
            elif not cell.rocks:
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
        for cell in game.grid[i]:
            if cell.rocks and cell.rocks[-1].id is not player_id:
                gobblet_count += 1
            elif not cell.rocks:
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
    for i in range(len(game.grid)):
        gobblet_count = 0
        empty_count = 0
        cell = game.grid[i][i]
        if cell.rocks and cell.rocks[-1].id == player_id:
            gobblet_count += 1
        elif not cell.rocks:
            empty_count += 1
        if gobblet_count == 1 and empty_count == 3:
            sum_diag += 1
        elif gobblet_count == 2 and empty_count == 2:
            sum_diag += 10
        elif gobblet_count == 3 and empty_count == 1:
            sum_diag += 100
        elif gobblet_count == 4 and empty_count == 0:
            sum_diag += math.inf

    for i in range(len(game.grid)):
        gobblet_count = 0
        empty_count = 0
        cell = game.grid[i][i]
        if cell.rocks and cell.rocks[-1].id is not player_id:
            gobblet_count += 1
        elif not cell.rocks:
            empty_count -= 1
        if gobblet_count == 1 and empty_count == 3:
            sum_diag -= 1
        elif gobblet_count == 2 and empty_count == 2:
            sum_diag -= 10
        elif gobblet_count == 3 and empty_count == 1:
            sum_diag -= 100
        elif gobblet_count == 4 and empty_count == 0:
            sum_diag -= math.inf

    # Handling anti Diagonal states
    for i in range(len(game.grid)):
        gobblet_count = 0
        empty_count = 0
        cell = game.grid[i][len(game.grid) - 1 - i]
        if cell.rocks and cell.rocks[-1].id == player_id:
            gobblet_count += 1
        elif not cell.rocks:
            empty_count += 1
        if gobblet_count == 1 and empty_count == 3:
            sum_anti_diag += 1
        elif gobblet_count == 2 and empty_count == 2:
            sum_anti_diag += 10
        elif gobblet_count == 3 and empty_count == 1:
            sum_anti_diag += 100
        elif gobblet_count == 4 and empty_count == 0:
            sum_anti_diag += 999

    for i in range(len(game.grid)):
        gobblet_count = 0
        empty_count = 0
        cell = game.grid[i][len(game.grid) - 1 - i]
        if cell.rocks and cell.rocks[-1].id is not player_id:
            gobblet_count += 1
        elif not cell.rocks:
            empty_count += 1
        if gobblet_count == 1 and empty_count == 3:
            sum_anti_diag -= 1
        elif gobblet_count == 2 and empty_count == 2:
            sum_anti_diag -= 10
        elif gobblet_count == 3 and empty_count == 1:
            sum_anti_diag -= 100
        elif gobblet_count == 4 and empty_count == 0:
            sum_anti_diag -= 999

    total_weight = sum_row + sum_col + sum_diag + sum_anti_diag

    return total_weight

'''
if __name__ == "__main__":
    game = Game("Player 1", "Player 2")
    player_id = 0

    while True:
        game.print_grid()
        print(f"\nPlayer {player_id}'s turn:")
        
        # Use your AI (min_max) or human input to make a move
        if player_id == 0:
            # AI's turn
            move = best_move(game, player_id)
        
    
        else:
            # Human's turn (you can replace this with your own input logic)
            try:
                #move_input = input("Enter your move (e.g., '0 0 1 0' to move a rock from pile 0 to grid (1,0)): ")
                #move_values = list(map(int, move_input.split()))
                #move = (Postion(move_values[0], move_values[1]), None, move_values[2])
                move = best_move(game, player_id)
                
            except ValueError:
                print("Invalid input. Please enter a valid move.")
                continue

        try:
            game.do_turn(player_id, move[0], move[1], move[2])
        except Exception as e:
            print(f"Invalid move: {e}")
            continue

        winner, winner_id = game.check_win()
        if winner:
            print(f"\nPlayer {winner_id} wins!")
            break

        # Switch to the other player
        player_id = 1 - player_id
'''