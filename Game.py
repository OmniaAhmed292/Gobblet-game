'''
Game class should be responsible for:

* Maintaining state of pieces on board and in reserves
* Executing player moves while enforcing rules
* Validating move legality
* Checking win conditions
* Providing available moves for current player
'''
from Pile import Pile
from Player import Player
from Position import Position


class Game:
    player: list[Player]
    grid: list[list[Pile]]
    best_move: tuple[Position, Position, int]

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

    def is_able_to_win(self, to_grid: Position) -> bool:
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
        if (diff == 0 or diff == 1 or diff == -1):
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

    def is_valid(self, player_id, to_grid: Position, from_grid: Position = None, from_pile: int = None) -> bool:
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

        if from_pile != None and self.grid[to_grid.x][to_grid.y].rocks and self.player[player_id].piles[from_pile].rocks and self.player[player_id].piles[from_pile].rocks[-1].size <= self.grid[to_grid.x][to_grid.y].rocks[-1].size:
            return False
            # raise Exception("You cannot play from a smaller rock to a larger one.")
        if from_pile != None and not self.player[player_id].piles[from_pile].rocks:
            return False
            # raise Exception("can not remove from empty space")

        if self.grid[to_grid.x][to_grid.y].rocks and self.grid[to_grid.x][to_grid.y].rocks[
                -1].id != player_id and not self.is_able_to_win(to_grid):
            return False
            # raise Exception("You cannot play on another player's rock unless they have 3 in a row")
        return True

    def do_turn(self, player_id, to_grid: Position, from_grid: Position = None, from_pile: int = None) -> None:
        self.is_valid(player_id, to_grid, from_grid, from_pile)
        self.player[player_id].turns += 1
        if from_pile != None:
            self.grid[to_grid.x][to_grid.y].push(
                self.player[player_id].piles[from_pile].pop())
            # self.grid[to_grid.x][to_grid.y].rocks[-1].pile_no = from_pile
        elif from_grid != None:
            self.grid[to_grid.x][to_grid.y].push(
                self.grid[from_grid.x][from_grid.y].pop())

    def undo_turn(self, player_id, from_grid: Position, to_grid: Position = None, to_pile: int = None) -> None:
        if to_pile != None:
            self.player[player_id].piles[to_pile].push(
                self.grid[from_grid.x][from_grid.y].pop())
        elif to_grid != None:
            self.grid[to_grid.x][to_grid.y].push(
                self.grid[from_grid.x][from_grid.y].pop())

    def check_win(self) -> tuple[bool, int]:  # return -1 if no one win yet
        # check all rows
        for i in range(4):
            cnt = 0
            if not self.grid[i][0].rocks:
                continue
            for j in range(4):
                if self.grid[i][j].rocks and self.grid[i][0].rocks[-1].id == self.grid[i][j].rocks[-1].id:
                    cnt += 1
                if cnt == 4:
                    return True, self.grid[i][0].rocks[-1].id

        cnt = 0

        # check all columns
        for i in range(4):
            cnt = 0
            if not self.grid[0][i].rocks:
                continue
            for j in range(4):
                if self.grid[j][i].rocks and self.grid[0][i].rocks[-1].id == self.grid[j][i].rocks[-1].id:
                    cnt += 1
                if cnt == 4:
                    return True, self.grid[0][i].rocks[-1].id

        cnt = 0

        if all(self.grid[i][i].rocks and self.grid[i][i].rocks[-1].id == self.grid[0][0].rocks[-1].id for i in
               range(4)):
            return True, self.grid[0][0].rocks[-1].id

            # Check anti-diagonal
        if all(self.grid[i][3 - i].rocks and self.grid[i][3 - i].rocks[-1].id == self.grid[0][3].rocks[-1].id for i in
               range(4)):
            return True, self.grid[0][3].rocks[-1].id
        return False, -1



