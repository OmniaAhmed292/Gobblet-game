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
from InvalidMoveException import *

class Game:
  
    player: list[Player]
    grid: list[list[Pile]]
    game_history: list[list[list[Pile]]]
    

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
      self.game_history = []

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
          to_grid (Position): The position to which the move is being made.
          from_grid (Position, optional): The position from which the move is being made. Defaults to None.
          from_pile (int, optional): The pile from which the move is being made. Defaults to None.
    """
    def is_valid(self, player_id, to_grid: Position, from_grid: Position = None, from_pile: int = None) -> bool:
        if from_grid != None and from_pile != None:
            raise MoveFromBothGridAndPileException("You can either play from the grid or your piles, not both.")

        if from_grid == None and from_pile == None:
            raise MoveFromNeitherGridNorPileException("You should play from either the grid or your piles at least.")

        if from_grid and self.grid[from_grid.x][from_grid.y].rocks and self.grid[from_grid.x][from_grid.y].rocks[-1].id != player_id:
            raise MoveFromAnotherPlayerException("You cannot play from another player's rocks.")

        if from_grid and not self.grid[from_grid.x][from_grid.y].rocks:
            raise MoveFromEmptyGridException("You cannot play from an empty cell.")
        
        if from_grid and from_grid.x==to_grid.x and from_grid.y==to_grid.y:
            raise MoveToSamePositionException("You cannot play on the same cell.")
        
        if from_grid and self.grid[to_grid.x][to_grid.y].rocks and self.grid[from_grid.x][from_grid.y].rocks[-1].size <= self.grid[to_grid.x][to_grid.y].rocks[-1].size:
            raise MoveToSmallerRockException("You cannot play a smaller rock on top of a larger one.")
        
        if from_pile!= None and self.player[player_id].piles[from_pile].rocks and self.grid[to_grid.x][to_grid.y].rocks and self.player[player_id].piles[from_pile].rocks[-1].size <= self.grid[to_grid.x][to_grid.y].rocks[-1].size:
            raise MoveToSmallerRockException("You cannot play a smaller rock on top of a larger one.")
       

        if self.grid[to_grid.x][to_grid.y].rocks and self.grid[to_grid.x][to_grid.y].rocks[-1].id != player_id and not self.is_able_to_win(to_grid):
            raise MoveWithNo3RocksException("You cannot play on another player's rock unless they have 3 in a row")
        return True

    """
        Checks if Valid then executes a move and updates the game state while adding older state to history.
        raises an exception if the move is invalid.
        Args:
            player_id (int): The ID of the player making the move.
            to_grid (Position): The position to which the move is being made.
            from_grid (Position, optional): The position from which the move is being made. Defaults to None.
            from_pile (int, optional): The pile from which the move is being made. Defaults to None.
    """
    def do_turn(self, player_id, to_grid: Position, from_grid: Position = None, from_pile: int = None) -> None:
        #TODO if you are using true or false instead of exceptions, you can use the following code to catch errors

       
        self.is_valid(player_id, to_grid, from_grid, from_pile)
         

        self.game_history.append(self.grid)
        if from_pile != None:
          self.grid[to_grid.x][to_grid.y].push(self.player[player_id].piles[from_pile].pop())
        elif from_grid:
          self.grid[to_grid.x][to_grid.y].push(self.grid[from_grid.x][from_grid.y].pop())

    """
    Checks if the current state of the game if it is a win
    Returns:
        The ID of the player who won the game if there is a winner, None otherwise
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

    """
    Checks if any legal move is available for the current player.
    Returns:
        True if a legal move is available, False otherwise.
    """
    def has_legalMoves(self):
        for to_grid_x in range(4):
            for to_grid_y in range(4):
                # Check if placing a new rock is legal
                if not self.grid[to_grid_x][to_grid_y].rocks:
                    # Check if placing a new rock is legal
                    if self.is_valid(self.current_player.player_id, Position(to_grid_x, to_grid_y)):
                        return True

                for from_pile_index in range(3):
                    if not self.player[self.current_player.player_id].piles[from_pile_index].is_empty():
                        # Check if playing from a pile is legal
                        if self.is_valid(self.current_player.player_id, Position(to_grid_x, to_grid_y), from_pile=from_pile_index):
                            return True

                for from_grid_x in range(4):
                    for from_grid_y in range(4):
                        if self.grid[from_grid_x][from_grid_y].rocks and self.grid[from_grid_x][from_grid_y].rocks[-1].id == self.current_player.player_id:
                            # Check if moving a rock from the grid is legal
                            if self.is_valid(self.current_player.player_id, Position(to_grid_x, to_grid_y), Position(from_grid_x, from_grid_y)):
                                return True
        return False

    """
    Checks if the current state of the game has three repetitions of identical moves.

    Returns:
        True if three repetitions are found, False otherwise.
    """
    def check_three_repetitions(self):
        # Check if it's still early in the game
        if len(self.game_history) < 6:
            return False
        # Check for three consecutive identical entries in the history
        if self.game_history[-1] == self.game_history[-4] and self.game_history[-2] == self.game_history[-5] and self.game_history[-3] == self.game_history[-6]:
            return True
        return False

    """
      Checks if the current state of the game has three repetitions of identical moves.
      Returns:
          True if three repetitions are found, False otherwise.
    """
    def check_tie(self): 
        #it's been three cycling moves with no winner or there are no legal moves left
        if self.check_three_repetitions() or (not self.has_legalMoves()):
            return True
        return False

    #def possible_moves(self, player_id):
