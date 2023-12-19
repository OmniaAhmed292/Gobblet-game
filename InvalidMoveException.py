"""
    This class is used to raise exceptions for invalid moves.
    The following exceptions are defined:
        - MoveFromBothGridAndPileException: The move is from both a grid and a pile.
        - MoveFromNeitherGridNorPileException: The move is from neither a grid nor a pile.
        - MoveFromAnotherPlayerException: The move another player's rocks.
        - MoveFromEmptyPileException: The move is from an empty pile.
        - MoveFromEmptyGridException: The move is from an empty grid.
        - MoveToSmallerRockException: The move is to a Position with a smaller rock.
        - MoveToSamePositionException: The move is to the same position.
        - MoveWithNo3RocksException: The move is on another's player's rock and they don't have 3 rocks in a row.
"""
class InvalidMoveException(Exception):
    def __init__(self, message):
        super().__init__(message)

class MoveFromBothGridAndPileException(InvalidMoveException):
    def __init__(self, message):
        super().__init__(message)

class MoveFromNeitherGridNorPileException(InvalidMoveException):
    def __init__(self, message):
        super().__init__(message)

class MoveFromAnotherPlayerException(InvalidMoveException):
    def __init__(self, message):
        super().__init__(message)

class MoveFromEmptyPileException(InvalidMoveException):
    def __init__(self, message):
        super().__init__(message)

class MoveFromEmptyGridException(InvalidMoveException):
    def __init__(self, message):
        super().__init__(message)

class MoveToSmallerRockException(InvalidMoveException):
    def __init__(self, message):
        super().__init__(message)

class MoveToSamePositionException(InvalidMoveException):
    def __init__(self, message):
        super().__init__(message)

class MoveWithNo3RocksException(InvalidMoveException):
    def __init__(self, message):
        super().__init__(message)



    

