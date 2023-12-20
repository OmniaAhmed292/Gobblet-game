import unittest
from Game import Game
from Move import Move
from Position import Position
from Rock import Rock
from InvalidMoveException import *

"""
    Tests for the is valid function.
"""
class TestIsValid(unittest.TestCase):

    def setUp(self):
        self.game = Game("Player1", "Player2")
    
    def tearDown(self):
        del self.game

    
    """
        Tests for the is_valid method.
    """
    def test_move_from_both_grid_and_pile(self):
        with self.assertRaises(MoveFromBothGridAndPileException):
            move = Move(0, Position(0, 0), Position(1, 1), 0)
            self.game.is_valid(move)

    def test_move_from_neither_grid_nor_pile(self):
        with self.assertRaises(MoveFromNeitherGridNorPileException):
            move = Move(0, Position(0, 0), None, None)
            self.game.is_valid(move)

    def test_move_from_another_player(self):
        self.game.grid[0][0].push(Rock(1, 1))
        with self.assertRaises(MoveFromAnotherPlayerException):
            move = Move(0, Position(0, 0), Position(0, 0))
            self.game.is_valid(move)

    def test_move_from_empty_grid(self):
        with self.assertRaises(MoveFromEmptyGridException):
            move = Move(0, Position(0, 0), Position(1, 1))
            self.game.is_valid(move)

    def test_move_to_smaller_rock(self):
        self.game.grid[0][0].push(Rock(1, 0))
        self.game.grid[1][1].push(Rock(2, 1))
        with self.assertRaises(MoveToSmallerRockException):
            move = Move(0, Position(1, 1), Position(0, 0))
            self.game.is_valid(move)

    def test_move_to_same_position(self):
        self.game.grid[0][0].push(Rock(1, 0))
        with self.assertRaises(MoveToSamePositionException):
            move = Move(0, Position(0, 0), Position(0, 0))
            self.game.is_valid(move)

    def test_move_with_no_3_rocks(self):
        self.game.grid[0][0].push(Rock(1, 1))
        with self.assertRaises(MoveWithNo3RocksException):
            move = Move(0, Position(0, 0), None, 0)
            self.game.is_valid(move)
    
    def test_move_to_none(self):
        with self.assertRaises(MoveToNonePositionException):
            move = Move(0, None, None)
            self.game.is_valid(move)
            
    def test_valid_move(self):
        move = Move(0, Position(0, 0), None, 0)
        self.assertTrue(self.game.is_valid(move))

class TestDoTurn(unittest.TestCase):
    def setUp(self):
        self.game = Game("Player1", "Player2")
        
    def test_do_turn_from_pile(self):
        # Test a valid move
        move = Move(0, Position(0, 0), None, 0)
        self.game.do_turn(move)

        # Assert that the move was executed correctly
        assert self.game.grid[0][0].rocks[-1].id == move.player_id

    def test_do_turn_invalid_move(self):
        # Test an invalid move

        with self.assertRaises(Exception):
            move = Move(1, Position(0, 0), Position(1, 1), 0)
            self.game.do_turn(move)

    def test_do_turn_from_grid(self):
        # Test a move from the grid
        move = Move(0, Position(0, 0), Position(1, 1), None)

        self.game.grid[1][1].push(Rock(1, 0))
        self.game.do_turn(move)

        # Assert that the move was executed correctly
        assert self.game.grid[0][0].rocks[-1].id == move.player_id

class TestCheckWin(unittest.TestCase):
    def setUp(self):
        self.game = Game("Player1", "Player2")

    def test_no_winner(self):
        self.assertIsNone(self.game.check_win())

    def test_player1_wins_row(self):
        for i in range(4):
            self.game.grid[0][i].push(Rock(1, 0))
        self.assertEqual(self.game.check_win(), 0)

    def test_player2_wins_column(self):
        for i in range(4):
            self.game.grid[i][0].push(Rock(1, 1))
        self.assertEqual(self.game.check_win(), 1)

    def test_player1_wins_diagonal(self):
        for i in range(4):
            self.game.grid[i][i].push(Rock(1, 0))
        self.assertEqual(self.game.check_win(), 0)

    def test_player2_wins_reverse_diagonal(self):
        for i in range(4):
            self.game.grid[i][3-i].push(Rock(1, 1))
        self.assertEqual(self.game.check_win(), 1)
    
    def test_variable_size(self):
        for i in range(4):
            self.game.grid[0][i].push(Rock(i+1, 0))
        self.assertEqual(self.game.check_win(), 0)
    
    
    


 

##    def test_check_three_repetitions(self):
        # Test the check_three_repetitions method
        # Add your test cases here
##        pass

##    def test_check_tie(self):
        # Test the check_tie method
        # Add your test cases here
##        pass

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)