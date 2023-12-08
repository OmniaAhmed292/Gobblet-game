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
from Postion import Postion


class Game:
  player: list[Player]
  grid: list[list[Pile]]

  def __init__(self, player1_name, player2_name) -> None:
    self.player = [Player(player1_name, 0), Player(player2_name, 1)]
    self.grid = [
        [Pile(),Pile(),Pile(),Pile()],
        [Pile(),Pile(),Pile(),Pile()],
        [Pile(),Pile(),Pile(),Pile()],
        [Pile(),Pile(),Pile(),Pile()]
        ]

  def print_grid(self) -> None:
    for row in self.grid:
      for cell in row:
        print(cell.rocks[-1].size if cell.rocks else '#', end=' ')
      print("\n")
    print("\n")

  def is_valid(self, player_id, to_grid, from_grid=None, from_pile=None):
      if from_grid and from_pile:
          raise Exception("You can either play from the grid or your piles, not both.")
      if not from_grid and not from_pile:
          raise Exception("You should play from either the grid or your piles at least.")

      if from_grid and self.grid[from_grid.x][from_grid.y].rocks and self.grid[to_grid.x][to_grid.y].rocks[
          -1].id != player_id:
          raise Exception("You cannot play from another player's rocks.")

      if self.grid[to_grid.x][to_grid.y].rocks and self.grid[to_grid.x][to_grid.y].rocks[-1].id != player_id:
          
          cnt = 0

          # Check for a winning condition in the row
          for i in range(4):
              if self.grid[to_grid.x][i].rocks and self.grid[to_grid.x][i].rocks[-1].id == self.grid[to_grid.x][to_grid.y].rocks[-1].id:
                  cnt += 1

          if cnt == 3:
              return

          # Reset counter for column check
          cnt = 0

          # Check for a winning condition in the column
          for i in range(4):
              if self.grid[i][to_grid.y].rocks and self.grid[i][to_grid.y].rocks[-1].id == self.grid[to_grid.x][to_grid.y].rocks[-1].id:
                  cnt += 1

          if cnt == 3:
              return

          if (
                  (to_grid.x + 2 < 4 and to_grid.y + 2 < 4
                   and self.grid[to_grid.x + 1][to_grid.y + 1].rocks
                   and self.grid[to_grid.x + 2][to_grid.y + 2].rocks
                   and self.grid[to_grid.x + 1][to_grid.y + 1].rocks[-1].id != player_id
                   and self.grid[to_grid.x + 2][to_grid.y + 2].rocks[-1].id != player_id)
                  or
                  (to_grid.x - 2 >= 0 and to_grid.y - 2 >= 0
                   and self.grid[to_grid.x - 1][to_grid.y - 1].rocks
                   and self.grid[to_grid.x - 2][to_grid.y - 2].rocks
                   and self.grid[to_grid.x - 1][to_grid.y - 1].rocks[-1].id != player_id
                   and self.grid[to_grid.x - 2][to_grid.y - 2].rocks[-1].id != player_id)
                  or
                  (to_grid.x + 2 < 4 and to_grid.y - 2 >= 0
                   and self.grid[to_grid.x + 1][to_grid.y - 1].rocks
                   and self.grid[to_grid.x + 2][to_grid.y - 2].rocks
                   and self.grid[to_grid.x + 1][to_grid.y - 1].rocks[-1].id != player_id
                   and self.grid[to_grid.x + 2][to_grid.y - 2].rocks[-1].id != player_id)
                  or
                  (to_grid.x - 2 >= 0 and to_grid.y + 2 < 4
                   and self.grid[to_grid.x - 1][to_grid.y + 1].rocks
                   and self.grid[to_grid.x - 2][to_grid.y + 2].rocks
                   and self.grid[to_grid.x - 1][to_grid.y + 1].rocks[-1].id != player_id
                   and self.grid[to_grid.x - 2][to_grid.y + 2].rocks[-1].id != player_id)
          ):
              return
          else:
              raise Exception("You cannot play on another player's rock unless they have 3 in a row")

  def do_turn(self, player_id, to_grid: Postion, from_grid: Postion = None, from_pile: int = None) -> None:
    self.is_valid(player_id, to_grid, from_grid, from_pile)
    if from_pile:
      self.grid[to_grid.x][to_grid.y].push(self.player[player_id].piles[from_pile].pop())
    elif from_grid:
      self.grid[to_grid.x][to_grid.y].push(self.grid[from_grid.x][from_grid.y].pop())

  def check_win(self):
      cnt = 0
      for i in range(4):
          for j in range(4):
              if self.grid[i][j].rocks and self.grid[0][j].rocks and self.grid[i][j].rocks[-1].id == self.grid[0][j].rocks[-1].id:
                  cnt += 1
              if cnt == 4:
                  return self.grid[0][j].rocks[-1].id
      cnt = 0
      for i in range(4):
            for j in range(4):
                if self.grid[j][i].rocks and self.grid[0][j].rocks and self.grid[j][i].rocks[-1].id == self.grid[0][j].rocks[-1].id:
                    cnt += 1
                if cnt == 4:
                    return self.grid[i][0].rocks[-1].id

      if all(self.grid[i][i].rocks and self.grid[i][i].rocks[-1].id == self.grid[0][0].rocks[-1].id for i in range(4)):
          return self.grid[0][0].rocks[-1].id

          # Check anti-diagonal
      if all(self.grid[i][3 - i].rocks and self.grid[i][3 - i].rocks[-1].id == self.grid[0][3].rocks[-1].id for i in range(4)):
          return self.grid[0][3].rocks[-1].id


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