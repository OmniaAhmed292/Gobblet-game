'''
Game class should be responsible for: 

* Maintaining state of pieces on board and in reserves
* Executing player moves while enforcing rules
* Validating move legality
* Checking win conditions
* Providing available moves for current player
'''
class Game:

    def __init__(self):
        self.board = [[None for _ in range(4)] for _ in range(4)]
        self.white_pieces = generate_pieces("white") 
        self.black_pieces = generate_pieces("black")
        self.white_reserves = get_reserves(self.white_pieces)
        self.black_reserves = get_reserves(self.black_pieces)
        self.current_player = "white"
        
    def execute_move(self, move):
        # Execute the move 
        piece, start, end = move
        
        # Remove piece from reserves if first move
        if start is None:
            self.remove_from_reserves(piece, self.current_player)
            
        # Move piece on the board 
        self.move_piece(start, end)
        
        # Switch players
        if self.current_player == "white":
            self.current_player = "black"
        else:
            self.current_player = "white"
            
    def validate_move(self, move):
        # Validate move based on rules
        # Return True if valid, False if invalid
        
    def check_win(self, player):
        # Check if 4 pieces in a row
        # Return True if win, False otherwise
        
    def get_possible_moves(self):
        # Return list of legal moves for current player
        
# Helper functions

    def remove_from_reserves(self, piece, player):
        # Remove piece from player reserves
    
    def move_piece(self, start, end):
        # Handle move of piece start -> end
        
    def get_reserves(self, pieces):
        # Get remaining reserve p