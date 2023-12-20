"""
    This class is used to raise exceptions for invalid moves.
    The following exceptions are defined:
        - MoveFromBothGridAndPileException: The move is from both a grid and a pile.
        - MoveFromNeitherGridNorPileException: The move is from neither a grid nor a pile.
        - MoveFromAnotherPlayerException: The move another player's rocks.
        - MoveFromEmptyPileException: The move is from an empty pile.
        - MoveFromEmptyGridException: The move is from an empty grid.
        - MoveToNonePositionException: The move is to None.
        - MoveToSmallerRockException: The move is to a Position with a smaller rock.
        - MoveToSamePositionException: The move is to the same position.
        - MoveWithNo3RocksException: The move is on another's player's rock and they don't have 3 rocks in a row.
"""
class InvalidMoveException(Exception):
    def __init__(self, message):
        super().__init__(message)

class MoveFromBothGridAndPileException(InvalidMoveException):
    """
    Exception raised when a move is attempted from both a grid and a pile.

    Attributes:
        message (str): explanation of the error
    """
    def __init__(self, message):
        super().__init__(message)


class MoveFromNeitherGridNorPileException(InvalidMoveException):
    """
    Exception raised when a move is attempted from neither a grid nor a pile.

    Attributes:
        message (str): explanation of the error
    """
    def __init__(self, message):
        super().__init__(message)


class MoveFromAnotherPlayerException(InvalidMoveException):
    """
    Exception raised when a move is attempted on another player's rocks.

    Attributes:
        message (str): explanation of the error
    """
    def __init__(self, message):
        super().__init__(message)

class MoveFromEmptyPileException(InvalidMoveException):
    """
    Exception raised when a move is attempted from an empty pile.

    Attributes:
        message (str): explanation of the error
    """
    def __init__(self, message):
        super().__init__(message)


class MoveFromEmptyGridException(InvalidMoveException):
    """
    Exception raised when a move is attempted from an empty grid.

    Attributes:
        message (str): explanation of the error
    """
    def __init__(self, message):
        super().__init__(message)


class MoveToNonePositionException(InvalidMoveException):
    """
    Exception raised when a move is attempted to a None position.

    Attributes:
        message (str): explanation of the error
    """
    def __init__(self, message):
        super().__init__(message)


class MoveToSmallerRockException(InvalidMoveException):
    """
    Exception raised when a move is attempted to a position with a smaller rock.

    Attributes:
        message (str): explanation of the error
    """
    def __init__(self, message):
        super().__init__(message)


class MoveToSamePositionException(InvalidMoveException):
    """
    Exception raised when a move is attempted to the same position.

    Attributes:
        message (str): explanation of the error
    """
    def __init__(self, message):
        super().__init__(message)


class MoveWithNo3RocksException(InvalidMoveException):
    """
    Exception raised when a move is attempted on another player's rock and they don't have 3 rocks in a row.

    Attributes:
        message (str): explanation of the error
    """
    def __init__(self, message):
        super().__init__(message)