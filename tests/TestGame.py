import unittest
from Game import *
from Position import *
from InvalidMoveException import *
from Pile import *
from Rock import *
from Player import *

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game("Player1", "Player2")
    
    def tearDown(self):
        del self.game

    
    """
        Tests for the is_valid method.
    """
    def test_move_from_both_grid_and_pile(self):
        with self.assertRaises(MoveFromBothGridAndPileException):
            self.game.is_valid(0, Position(0, 0), Position(1, 1), 0)

    def test_move_from_neither_grid_nor_pile(self):
        with self.assertRaises(MoveFromNeitherGridNorPileException):
            self.game.is_valid(0, Position(0, 0))

    def test_move_from_another_player(self):
        self.game.grid[0][0].push(Rock(1, 1))
        with self.assertRaises(MoveFromAnotherPlayerException):
            self.game.is_valid(0, Position(0, 0), Position(0, 0))

    def test_move_from_empty_grid(self):
        with self.assertRaises(MoveFromEmptyGridException):
            self.game.is_valid(0, Position(0, 0), Position(1, 1))

    def test_move_to_smaller_rock(self):
        self.game.grid[0][0].push(Rock(1, 0))
        self.game.grid[1][1].push(Rock(2, 1))
        with self.assertRaises(MoveToSmallerRockException):
            self.game.is_valid(0, Position(1, 1), Position(0, 0))

    def test_move_to_same_position(self):
        self.game.grid[0][0].push(Rock(1, 0))
        with self.assertRaises(MoveToSamePositionException):
            self.game.is_valid(0, Position(0, 0), Position(0, 0))

    def test_move_with_no_3_rocks(self):
        self.game.grid[0][0].push(Rock(1, 0))
        with self.assertRaises(MoveWithNo3RocksException):
            self.game.is_valid(0, Position(1, 1), Position(0, 0))
            
    def test_valid_move(self):
        self.assertTrue(self.game.is_valid(0, Position(0, 0), None, 0))

    """
        Tests for the do_turn method.
    """
        
    def test_do_turn_from_pile(self):
        # Test a valid move
        player_id = 0
        to_grid = Position(0, 0)
        from_pile = 0
        from_grid = None

        self.game.do_turn(player_id, to_grid, from_grid, from_pile)

        # Assert that the move was executed correctly
        assert self.game.grid[0][0].rocks[-1].id == player_id

    def test_do_turn_invalid_move(self):
        # Test an invalid move
        player_id = 1
        to_grid = Position(0, 0)
        from_grid = Position(1, 1)
        from_pile = 0

        with self.assertRaises(Exception):
            self.game.do_turn(player_id, to_grid, from_grid, from_pile)

    def test_do_turn_from_grid(self):
        # Test a move from the grid
        player_id = 0
        to_grid = Position(0, 0)
        from_grid = Position(1, 1)
        from_pile = None

        self.game.grid[1][1].push(Rock(1, 0))
        self.game.do_turn(player_id, to_grid, from_grid, from_pile)

        # Assert that the move was executed correctly
        assert self.game.grid[0][0].rocks[-1].id == player_id

    """
        Tests for the check_win method.
    """
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

if __name__ == '__main__':
   unittest.main(argv=['first-arg-is-ignored'], exit=False)   
