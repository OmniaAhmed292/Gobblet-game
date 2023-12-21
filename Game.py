'''
Game class should be responsible for:

* Maintaining state of pieces on board and in reserves
* Executing player moves while enforcing rules
* Validating move legality
* Checking win conditions
* Providing available moves for current player
'''
import math

from Pile import Pile
from Player import Player
from Postion import Postion


class Game:
    player: list[Player]
    grid: list[list[Pile]]
    best_move: tuple[Postion, Postion, int]

    def __init__(self, player1_name, player2_name) -> None:
        self.player = [Player(player1_name, 0), Player(player2_name, 1)]
        self.grid = [
            [Pile(-1), Pile(-1), Pile(-1), Pile(-1)],
            [Pile(-1), Pile(-1), Pile(-1), Pile(-1)],
            [Pile(-1), Pile(-1), Pile(-1), Pile(-1)],
            [Pile(-1), Pile(-1), Pile(-1), Pile(-1)]
        ]
        self.best_move = None

    def print_grid(self) -> None:
        for row in self.grid:
            for cell in row:
                print(cell.rocks[-1].size if cell.rocks else '#', end=' ')
            print("\n")
        print("\n")

    def is_able_to_win(self, to_grid: Postion) -> bool:
        cnt = 0

        # Check for a winning condition in the row
        for i in range(4):
            if self.grid[to_grid.x][i].rocks and self.grid[to_grid.x][i].rocks[-1].id == \
                    self.grid[to_grid.x][to_grid.y].rocks[-1].id:
                cnt += 1

        if cnt == 3:
            return True

        # Reset counter for column check
        cnt = 0

        # Check for a winning condition in the column
        for i in range(4):
            if self.grid[i][to_grid.y].rocks and self.grid[i][to_grid.y].rocks[-1].id == \
                    self.grid[to_grid.x][to_grid.y].rocks[-1].id:
                cnt += 1

        if cnt == 3:
            return True

        cnt = 0
        diff = to_grid.y - to_grid.x
        # if the differnce between x and y == 0 then its the middle diagonal and we check grid[i][i]
        # if the differnce between x and y == 1 then its above the middle diagonal and we check grid[i][i+1]
        # if the differnce between x and y == -1 then its below the middle diagonal and we check grid[i+1][i]
        # using dx and dy to simplify
        if diff == 0:
            dx = 0
            dy = 0
        if diff == 1:
            dx = 1
            dy = 0
        if diff == -1:
            dx = 0
            dy = 1
        # if its not the middle diagonal we need to check only 3 cells
        if(diff==0 or diff==1 or diff==-1):
            for i in range(4 - abs(diff)):
                if self.grid[i + dx][i + dy].rocks and self.grid[to_grid.x][to_grid.y].rocks[-1].id == \
                        self.grid[i + dx][i + dy].rocks[-1].id:
                    cnt += 1

            if cnt == 3:
                return True

        cnt = 0
        dist = to_grid.y + to_grid.x
        # if the sum of x and y == 3 then its the middile anti-diagonal and we check grid[i][3-i]
        # if the sum of x and y == 2 then its above the middile anti-diagonal and we check grid[i][2-i]
        # if the sum of x and y == 4 then its below the middile anti-diagonal and we check grid[i+1][3-i]
        # using dx and dy to simplify
        if dist == 3:
            dx = 0
            dy = 3
            diff = 0
        if dist == 2:
            dx = 0
            dy = 2
            diff = 1
        if dist == 4:
            dx = 1
            dy = 3
            diff = 1
        # if its not the middle diagonal we need to check only 3 cells
        for i in range(4 - abs(diff)):
            if self.grid[i + dx][dy - i].rocks and self.grid[to_grid.x][to_grid.y].rocks[-1].id == \
                    self.grid[i + dx][dy - i].rocks[-1].id:
                cnt += 1

        if cnt == 3:
            return True

    def is_valid(self, player_id, to_grid: Postion, from_grid: Postion = None, from_pile: int = None) -> bool:
        if from_grid != None and from_pile != None:
            return False
            # raise Exception("You can either play from the grid or your piles, not both.")
        if from_grid == None and from_pile == None:
            return False
            # raise Exception("You should play from either the grid or your piles at least.")

        if from_grid and from_grid.x == to_grid.x and from_grid.y == to_grid.y:
            return False
            # raise Exception("You cannot play on the same cell.")

        if from_grid and self.grid[from_grid.x][from_grid.y].rocks and self.grid[from_grid.x][from_grid.y].rocks[
            -1].id != player_id:
            return False
            # raise Exception("You cannot play from another player's rocks.")

        if from_grid and not self.grid[from_grid.x][from_grid.y].rocks:
            return False
            # raise Exception("You cannot play from an empty cell.")

        if from_grid and self.grid[to_grid.x][to_grid.y].rocks and self.grid[from_grid.x][from_grid.y].rocks[-1].size <= self.grid[to_grid.x][to_grid.y].rocks[-1].size:
            return False
            # raise Exception("You cannot play from a smaller rock to a larger one.")

        if from_pile!= None and self.grid[to_grid.x][to_grid.y].rocks and self.player[player_id].piles[from_pile].rocks and self.player[player_id].piles[from_pile].rocks[-1].size <= self.grid[to_grid.x][to_grid.y].rocks[-1].size:
            return False
            # raise Exception("You cannot play from a smaller rock to a larger one.")
        if from_pile!=None and not self.player[player_id].piles[from_pile].rocks:
            return False
            #raise Exception("can not remove from empty space")

        if self.grid[to_grid.x][to_grid.y].rocks and self.grid[to_grid.x][to_grid.y].rocks[
            -1].id != player_id and not self.is_able_to_win(to_grid):
            return False
            # raise Exception("You cannot play on another player's rock unless they have 3 in a row")
        return True
    def do_turn(self, player_id, to_grid: Postion, from_grid: Postion = None, from_pile: int = None) -> None:
        self.is_valid(player_id, to_grid, from_grid, from_pile)
        if from_pile != None:
            self.grid[to_grid.x][to_grid.y].push(self.player[player_id].piles[from_pile].pop())
            # self.grid[to_grid.x][to_grid.y].rocks[-1].pile_no = from_pile
        elif from_grid != None:
            self.grid[to_grid.x][to_grid.y].push(self.grid[from_grid.x][from_grid.y].pop())

    def undo_turn(self, player_id, from_grid: Postion, to_grid: Postion = None, to_pile: int = None) -> None:
        if to_pile != None:
            self.player[player_id].piles[to_pile].push(self.grid[from_grid.x][from_grid.y].pop())
        elif to_grid != None:
            self.grid[to_grid.x][to_grid.y].push(self.grid[from_grid.x][from_grid.y].pop())

    def check_win(self) -> tuple[bool, int]:  # return -1 if no one win yet
        cnt = 0
        for i in range(4):
            for j in range(4):
                if self.grid[i][j].rocks and self.grid[0][j].rocks and self.grid[i][j].rocks[-1].id == \
                        self.grid[0][j].rocks[-1].id:
                    cnt += 1
                if cnt == 4:
                    return True, self.grid[0][j].rocks[-1].id
            cnt = 0

        for i in range(4):
            for j in range(4):
                if self.grid[j][i].rocks and self.grid[j][0].rocks and self.grid[j][i].rocks[-1].id == \
                        self.grid[j][0].rocks[-1].id:
                    cnt += 1
                if cnt == 4:
                    return True, self.grid[j][0].rocks[-1].id
            cnt = 0

        if all(self.grid[i][i].rocks and self.grid[i][i].rocks[-1].id == self.grid[0][0].rocks[-1].id for i in
               range(4)):
            return True, self.grid[0][0].rocks[-1].id

            # Check anti-diagonal
        if all(self.grid[i][3 - i].rocks and self.grid[i][3 - i].rocks[-1].id == self.grid[0][3].rocks[-1].id for i in
               range(4)):
            return True, self.grid[0][3].rocks[-1].id
        return False, -1


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
    sz=0
    p_no=0
    f,t=0,0
    best_score = -999
    move = None
    for to_grid, from_grid, from_pile in possible_move(game, player_id):
            game.do_turn(player_id, to_grid, from_grid, from_pile)
            score = min_max(game, False, player_id, default_depth)
            game.undo_turn(player_id, to_grid, from_grid, from_pile)
            if score > best_score:
                best_score = score
                # move = (to_grid, from_grid, from_pile)

                if from_pile!=None:
                    sz=game.player[player_id].piles[from_pile].rocks[-1].size
                    p_no=from_pile
                    t=to_grid
                elif from_grid!=None:
                    sz=game.grid[from_grid.x][from_grid.y].rocks[-1].size
                    p_no=game.grid[from_grid.x][from_grid.y].rocks[-1].pile_no
                    f=from_grid

                move = (to_grid,from_grid,from_pile,p_no,sz)



    return move



def min_max(game: Game, is_max_player, player_id, depth=10) -> int:
    is_game_ended, winner_id = game.check_win()
    if is_game_ended:
        return 1 if winner_id == player_id else -1
    # TODO check for draw and return 0
    if depth == 0:
        evaluation = -999
        for to_grid, from_grid, from_pile in possible_move(game, int(is_max_player)):
            evaluation = max(evaluation, evaluation_function(game, int(is_max_player), to_grid, from_grid, from_pile))
        return evaluation*(1 if is_max_player else -1)
    if is_max_player:
        ret = -999
        for to_grid, from_grid, from_pile in possible_move(game, player_id):
            game.do_turn(player_id, to_grid, from_grid, from_pile)
            ret = max(ret, min_max(game, False, player_id, depth - 1))
            game.undo_turn(player_id, to_grid, from_grid, from_pile)


    else:
        ret = 999
        for to_grid, from_grid, from_pile in possible_move(game, 1 - player_id):
                game.do_turn(1-player_id, to_grid, from_grid, from_pile)
                ret = min(ret, min_max(game, True, player_id, depth - 1))
                game.undo_turn(1-player_id, to_grid, from_grid, from_pile)


    return ret

def evaluation_function(game: Game, player_id, to_grid: Postion, from_grid: Postion = None, from_pile: int = None) -> int:
    row = to_grid.x
    col = to_grid.y
    sum_row = 0
    sum_col = 0
    sum_diag = 0
    sum_anti_diag = 0
    sum=0
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

#     def __init__(self):
#         self.board = [[None for _ in range(4)] for _ in range(4)]
#         self.white_pieces = generate_pieces("white")
#         self.black_pieces = generate_pieces("black")
#         self.white_reserves = get_reserves(self.white_pieces)
#         self.black_reserves = get_reserves(self.black_pieces)
#         self.current_player = "white"
#
#     def execute_move(self, move):
#         # Execute the move
#         piece, start, end = move
#
#         # Remove piece from reserves if first move
#         if start is None:
#             self.remove_from_reserves(piece, self.current_player)
#
#         # Move piece on the board
#         self.move_piece(start, end)
#
#         # Switch players
#         if self.current_player == "white":
#             self.current_player = "black"
#         else:
#             self.current_player = "white"
#
#     def validate_move(self, move):
#         # Validate move based on rules
#         # Return True if valid, False if invalid
#

#     def get_possible_moves(self):
#         # Return list of legal moves for current player
#
# # Helper functions
#
#     def remove_from_reserves(self, piece, player):
#         # Remove piece from player reserves
#
#     def move_piece(self, start, end):
#         # Handle move of piece start -> end
#
#     def get_reserves(self, pieces):
#         # Get remaining reserve p
