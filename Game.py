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
    best_move: tuple[Postion, Postion, int]

    

    
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
        return False
    
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
    
    def check_win(self) -> tuple[bool, int]:  
        """
        Checks if the current state of the game if it is a win
        Returns:
            The ID of the player who won the game if there is a winner, -1 if there's no winner
        """
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

    def undo_turn(self, player_id, from_grid: Postion, to_grid: Postion = None, to_pile: int = None) -> None:
        if to_pile != None:
            self.player[player_id].piles[to_pile].push(self.grid[from_grid.x][from_grid.y].pop())
        elif to_grid != None:
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
