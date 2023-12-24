class Move:
    """
    This module contains the Move class, which is used to represent a move in the game.
    Attributes:
        player_id (int): The ID of the player making the move.
        to_grid (Position): The position to which the move is being made.
        from_grid (Position, optional): The position from which the move is being made. Defaults to None.
        from_pile (int, optional): The pile from which the move is being made. Defaults to None.
    
    methods:
        __init__(self, player_id: int, to_grid: Position, from_grid: Position = None, from_pile: int = None) -> None:
            Initializes a new Move object.
        __eq__(self, other: Move) -> bool:
            redifining the equality operator for Move class.
    """
    
    def __init__(self, player_id, to_grid, from_grid=None, from_pile=None):
        """
        Initializes a new Move object. 
        raises exceptions if the move is from both pile and grid or neither of them.
        Args:
            player_id (int): The ID of the player making the move.
            to_grid (Position): The position to which the move is being made.
            from_grid (Position, optional): The position from which the move is being made. Defaults to None.
            from_pile (int, optional): The pile from which the move is being made. Defaults to None.
        """
        from InvalidMoveException import MoveFromBothGridAndPileException, MoveFromNeitherGridNorPileException, MoveToNonePositionException

        self.player_id = player_id
        self.to_grid = to_grid

        #check if there's a destination
        if to_grid is None:
            raise MoveToNonePositionException("Move destination cannot be None.")

        #check if move is from both pile or grid
        if from_grid != None and from_pile != None:
            raise MoveFromBothGridAndPileException("You can either play from the grid or your piles, not both.")
        if from_grid == None and from_pile == None:
            raise MoveFromNeitherGridNorPileException("You should play from either the grid or your piles at least.")
        
        self.from_grid = from_grid
        self.from_pile = from_pile


    def __eq__(self, other):
        """
        redifining the equality operator for Move class.
        Args:
            other (Move): The move to compare to.
        returns:
            bool: True if the moves are equal, False otherwise.
        """
        if isinstance(other, Move):
            return (self.player_id == other.player_id and
                    self.to_grid == other.to_grid and
                    self.from_grid == other.from_grid and
                    self.from_pile == other.from_pile)
        return False