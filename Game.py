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
  
    
  """
    Initializes a new instance of the Game class.
    Args:
      player1_name (str): The name of the first player.
      player2_name (str): The name of the second player.
    """
  def __init__(self, player1_name, player2_name) -> None:
    self.player = [Player(player1_name, 0), Player(player2_name, 1)]
    self.grid = [
        [Pile(),Pile(),Pile(),Pile()],
        [Pile(),Pile(),Pile(),Pile()],
        [Pile(),Pile(),Pile(),Pile()],
        [Pile(),Pile(),Pile(),Pile()]
        ]

  """
    Prints the current state of the game board.
  """
  def print_grid(self) -> None:
    for row in self.grid:
      for cell in row:
        print(cell.rocks[-1].size if cell.rocks else '#', end=' ')
      print("\n")
    print("\n")

  """
    Checks if the move is valid.
    Args:
        player_id (int): The ID of the player making the move.
        to_grid (Postion): The position to which the move is being made.
        from_grid (Postion, optional): The position from which the move is being made. Defaults to None.
        from_pile (int, optional): The pile from which the move is being made. Defaults to None.
  """
  def is_valid(self, player_id, to_grid, from_grid=None, from_pile=None):
      

      if from_grid and from_pile:
          raise Exception("You can either play from the grid or your piles, not both.")
      if not from_grid and not from_pile:
          raise Exception("You should play from either the grid or your piles at least.")

      if from_grid and self.grid[from_grid.x][from_grid.y].rocks and self.grid[to_grid.x][to_grid.y].rocks[
          -1].id != player_id:
          raise Exception("You cannot play from another player's rocks.")

    
      if self.grid[to_grid.x][to_grid.y].rocks and self.grid[to_grid.x][to_grid.y].rocks[-1].id != player_id: #if the space is occupied by another player's rock
          
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

          # Check diagonal
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

  """
    Checks if Valid then executes a move and updates the game state.
    Args:
        player_id (int): The ID of the player making the move.
        to_grid (Postion): The position to which the move is being made.
        from_grid (Postion, optional): The position from which the move is being made. Defaults to None.
        from_pile (int, optional): The pile from which the move is being made. Defaults to None.
  """
  def do_turn(self, player_id, to_grid: Postion, from_grid: Postion = None, from_pile: int = None) -> None:
    self.is_valid(player_id, to_grid, from_grid, from_pile)
    if from_pile:
      self.grid[to_grid.x][to_grid.y].push(self.player[player_id].piles[from_pile].pop())
    elif from_grid:
      self.grid[to_grid.x][to_grid.y].push(self.grid[from_grid.x][from_grid.y].pop())

  """
  Checks if the current state of the game if it is a win
  Returns:
      True if three repetitions are found, False otherwise.
  """
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

  def has_legalMoves(self):
        """
        Checks if any legal move is available for the current player.

        Returns:
            True if a legal move is available, False otherwise.
        """
        for to_grid_x in range(4):
            for to_grid_y in range(4):
                # Check if placing a new rock is legal
                if not self.grid[to_grid_x][to_grid_y].rocks:
                    # Check if placing a new rock is legal
                    if self.is_valid(self.current_player.player_id, Postion(to_grid_x, to_grid_y)):
                        return True

                for from_pile_index in range(3):
                    if not self.player[self.current_player.player_id].piles[from_pile_index].is_empty():
                        # Check if playing from a pile is legal
                        if self.is_valid(self.current_player.player_id, Postion(to_grid_x, to_grid_y), from_pile=from_pile_index):
                            return True

                for from_grid_x in range(4):
                    for from_grid_y in range(4):
                        if self.grid[from_grid_x][from_grid_y].rocks and self.grid[from_grid_x][from_grid_y].rocks[-1].id == self.current_player.player_id:
                            # Check if moving a rock from the grid is legal
                            if self.is_valid(self.current_player.player_id, Postion(to_grid_x, to_grid_y), Postion(from_grid_x, from_grid_y)):
                                return True
        return False

  """
    Checks if the current state of the game has three repetitions of identical moves.
    Returns:
        True if three repetitions are found, False otherwise.
  """
  def check_tie(self): 
    #All spaces are filled and it's been three moves with no winner
    if self.check_three_repetitions():
        return True
    #No more valid moves can be made
    if not self.has_legalMoves():
        if(self.check_win() == None):
            return True
        

    return False

#def possible_moves(self, player_id):
''' def check_three_repetitions(self):
    """
    Checks if the current state of the game has three repetitions of identical moves.

    Returns:
        True if three repetitions are found, False otherwise.
    """

    # Keep track of the game history
    game_history = []

    # Check for three consecutive identical entries in the history
    for i in range(len(game_history) - 2):
        if game_history[i] == game_history[i + 1] and game_history[i + 1] == game_history[i + 2]:
            return True

    return False'''
