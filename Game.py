from Pile import Pile
from Player import Player
from Position import Position
from Move import Move
from InvalidMoveException import *

class Game:
    """
    The Game class represents a game of Gobblet Gobblers. and is resoponsible for
    * Maintaining state of pieces on board and in reserves
    * Executing player moves while enforcing rules
    * Validating move legality
    * Checking win conditions
    * Providing available moves for current player

    Attributes:
        player (list[Player]): A list of the two players in the game.
        grid (list[list[Pile]]): A 4x4 grid representing the game board.
        move_history (list[Move]): A list of all moves made in the game.
        possible_moves (list[Move]): A list of all possible moves for the current player.

    Methods:
        print_grid(): Prints the current state of the game board.
        is_valid(move: Move): Checks if a move is valid.
        do_turn(move: Move): Executes a move.
        check_win(): Checks if the current state of the game is a win.
        has_legalMoves(): Checks if any legal move is available for the current player.
        check_three_repetitions(): Checks if the current state of the game has three cycles of repeated moves.
        check_tie(): Checks if the current state of the game is a tie.
        generate_possible_moves(player_id): Generates a list of all possible moves for a player.
    """
  
    player: list[Player]
    grid: list[list[Pile]]
    move_history: list[Move]
    possible_moves: list[Move]
    

    
    def __init__(self, player1_name, player2_name) -> None:
        """
            Initializes a new instance of the Game class.
            Args:
            player1_name (str): The name of the first player.
            player2_name (str): The name of the second player.
        """
        self.player = [Player(player1_name, 0), Player(player2_name, 1)]
        self.grid = [
            [Pile(),Pile(),Pile(),Pile()],
            [Pile(),Pile(),Pile(),Pile()],
            [Pile(),Pile(),Pile(),Pile()],
            [Pile(),Pile(),Pile(),Pile()]
            ]
        self.move_history = []  # Changed from self.game_history = []
        self.possible_moves = []

    
    def print_grid(self) -> None:
      """
      Prints the current state of the game board.
      """
      for row in self.grid:
        for cell in row:
          print(cell.rocks[-1].size if cell.rocks else '#', end=' ')
        print("\n")
      print("\n")

    
    def is_valid(self, move: Move) -> bool:
        """
            Checks if the move is valid.
            Args:
                move (Move): The move to check.
        """

        if move.from_grid and self.grid[move.from_grid.x][move.from_grid.y].rocks and self.grid[move.from_grid.x][move.from_grid.y].rocks[-1].id != move.player_id:
            raise MoveFromAnotherPlayerException("You cannot play from another player's rocks.")

        if move.from_grid and not self.grid[move.from_grid.x][move.from_grid.y].rocks:
            raise MoveFromEmptyGridException("You cannot play from an empty cell.")
        
        if move.from_grid and move.from_grid.x == move.to_grid.x and move.from_grid.y == move.to_grid.y:
            raise MoveToSamePositionException("You cannot play on the same cell.")
        
        if move.from_grid and self.grid[move.to_grid.x][move.to_grid.y].rocks and self.grid[move.from_grid.x][move.from_grid.y].rocks[-1].size <= self.grid[move.to_grid.x][move.to_grid.y].rocks[-1].size:
            raise MoveToSmallerRockException("You cannot play a smaller rock on top of a larger one.")
        
        if move.from_pile!= None and self.player[move.player_id].piles[move.from_pile].rocks and self.grid[move.to_grid.x][move.to_grid.y].rocks and self.player[move.player_id].piles[move.from_pile].rocks[-1].size <= self.grid[move.to_grid.x][move.to_grid.y].rocks[-1].size:
            raise MoveToSmallerRockException("You cannot play a smaller rock on top of a larger one.")
       

        if self.grid[move.to_grid.x][move.to_grid.y].rocks and self.grid[move.to_grid.x][move.to_grid.y].rocks[-1].id != move.player_id and not self.is_able_to_win(move.to_grid):
            raise MoveWithNo3RocksException("You cannot play on another player's rock unless they have 3 in a row")
        return True


    def do_turn(self, move: Move) -> None:
        """
            Executes the given move.
            Args:
                move (Move): The move to execute.
        """
        #TODO if you are using true or false instead of exceptions, you can use the following code to catch errors
       
        self.is_valid(move)
         
        self.move_history.append(move)
        if move.from_pile != None:
          self.grid[move.to_grid.x][move.to_grid.y].push(self.player[move.player_id].piles[move.from_pile].pop())
        elif move.from_grid:
          self.grid[move.to_grid.x][move.to_grid.y].push(self.grid[move.from_grid.x][move.from_grid.y].pop())
        
        # Reset the possible moves list after a move has been made
        self.possible_moves = None

    def check_win(self):
        """
        Checks if the current state of the game if it is a win
        Returns:
            The ID of the player who won the game if there is a winner, None otherwise
        """
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


    def has_legalMoves(self, player_id):
        """
        Checks if any legal move is available for the current player.
        Returns:
            True if a legal move is available, False otherwise.
        """ 

        if self.possible_moves is None:
            self.possible_moves = self.generate_possible_moves(player_id)
        if len(self.possible_moves) > 0:
            return True
        return False


    def check_three_repetitions(self):
        """
        Checks if the current state of the game has three cycles of repeated moves.

        Returns:
            True if three repetitions are found, False otherwise.
        """
        # Check if it's still early in the game
        if len(self.move_history) < 6:
            return False
        # Check for three consecutive identical entries in the history
        if self.move_history[-1] == self.move_history[-4] and self.move_history[-2] == self.move_history[-5] and self.move_history[-3] == self.move_history[-6]:
            return True
        return False


    def check_tie(self): 
        """
          Checks if the current state of the game has three repetitions of identical moves.
          Returns:
              True if three repetitions are found, False otherwise.
        """
        #it's been three cycling moves with no winner or there are no legal moves left
        if self.check_three_repetitions() or (not self.has_legalMoves()):
            return True
        return False

    def generate_possible_moves(self, player_id) -> list[Move]:
        """
        Generates a list of all possible moves for the given player.
        Args:
            player_id (int): The ID of the player to generate moves for.
        Returns:
            A list of all possible moves for the given player.
        """
        # Check if the list of possible moves has already been generated
        if self.possible_moves:
            return self.possible_moves
        
        # Initialize possible_moves as an empty list
        self.possible_moves = []

        #check all combinations of moves to grid
        for to_grid_x in range(4):
            for to_grid_y in range(4):

                #check all combinations of moves from piles
                for from_pile_index in range(3):
                    # Check if playing from a pile is legal
                    try:
                        move = Move(player_id, Position(to_grid_x, to_grid_y), None, from_pile=from_pile_index)
                        self.is_valid(move)
                        self.possible_moves.append(move)
                    except:
                    #if not pass
                        pass
                #check all combinations of moves from grid
                for from_grid_x in range(4):
                    for from_grid_y in range(4):
                        # Check if moving a rock from the grid is legal
                        try:
                            move = Move(player_id, Position(to_grid_x, to_grid_y), Position(from_grid_x, from_grid_y), None)
                            self.is_valid(move)
                            self.possible_moves.append(move)
                        except:
                            pass
                        
                            
        return self.possible_moves
