#TODO write exceptions for invalid moves
class InvalidMoveException(Exception):
    def __init__(self, message):
        super().__init__(message)