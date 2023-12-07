'''
Game class should be responsible for:

* Maintaining state of pieces on board and in reserves
* Executing player moves while enforcing rules
* Validating move legality
* Checking win conditions
* Providing available moves for current player
'''
import Pile
import Player
import Postion


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

  def is_valid(self, player, to_grid: Postion, from_grid: Postion = None, from_pile: int = None) -> None:
    if from_grid and from_pile:
      raise Exception("you either play from the grid or your piles")
    if not from_grid and not from_pile:
      raise Exception("you should be at least play from the grid or your piles")

    if from_grid and self.grid[from_grid.x][from_grid.y].rocks and self.grid[to_grid.x][to_grid.y].rocks[-1].id != player:
      raise Exception("you can not play from another player rocks")

    if self.grid[to_grid.x][to_grid.y].rocks and self.grid[to_grid.x][to_grid.y].rocks[-1].id != player:
      # TODO check case if 3 in row else
      raise Exception("you can not play on another player rock unless he had 3 in a row")

  def do_turn(self, player, to_grid: Postion, from_grid: Postion = None, from_pile: int = None) -> None:
    self.is_valid(player, to_grid, from_grid, from_pile)
    if from_pile:
      self.grid[to_grid.x][to_grid.y].push(self.player[player].piles[from_pile].pop())
    elif from_grid:
      self.grid[to_grid.x][to_grid.y].push(self.grid[from_grid.x][from_grid.y].pop())


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
#     def check_win(self, player):
#         # Check if 4 pieces in a row
#         # Return True if win, False otherwise
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