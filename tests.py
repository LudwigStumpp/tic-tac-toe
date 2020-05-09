import unittest
from unittest.mock import patch
from io import StringIO

from TicTacToe.helpers import *
from TicTacToe.Board import Board, WrongConfigurationException, CantMakeMoveException, CantEvaluateException

class TestHelpers(unittest.TestCase):
    def test_unique_2d(self):
        array = [["a", "b"], ["b", "c"]]
        self.assertEqual(unique_2d(array), ["a", "b", "c"])

        array = [[], []]
        self.assertEqual(unique_2d(array), [])

class TestBoardClass(unittest.TestCase):
    def test_init(self):
        # num_winning > size
        self.assertRaises(WrongConfigurationException, Board, 3, 3, 4, "X", "O")
        
        # test board default placement
        board = Board(3, 2, 3, "X", "O")
        self.assertEqual(board.field, [[' ' for x in range(3)] for y in range(2)])

        # wrong size of preset board + wrong values
        preset = [["A", " ", " "],[" ", " ", " "]]
        self.assertRaises(WrongConfigurationException, Board, 3, 2, 3, "X", "O", preset)
        self.assertRaises(WrongConfigurationException, Board, 2, 3, 3, "X", "O", preset)
        
        # preset board works
        preset = [[" ", " ", " "],[" ", " ", " "]]
        Board(2, 3, 3, "X", "O", preset)

        # preset board works
        preset = [["X", " ", " "],[" ", " ", " "]]
        board = Board(2, 3, 3, "X", "O", preset)

    def test_valid_stone(self):
        board = Board(3, 2, 3, "X", "O")
        self.assertEqual(board.is_valid_stone(""), False)
        self.assertEqual(board.is_valid_stone(" "), True)
        self.assertEqual(board.is_valid_stone("X"), True)

    def test_empty(self):
        board = Board(3, 2, 3, "X", "O")
        self.assertEqual(board.is_empty(" "), True)
        self.assertEqual(board.is_empty("A"), False)

    def test_bord_show(self):
        preset = [["X", " ", " "],[" ", " ", " "]]
        board = Board(2, 3, 3, "X", "O", preset)
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            board.show_board()
            self.assertEqual(fakeOutput.getvalue().strip(), '|X| | |\n| | | |')

    def test_free_moves(self):
        preset = [["X", " ", " "],[" ", " ", " "]]
        board = Board(2, 3, 3, "X", "O", preset)
        self.assertEqual(board.get_free_moves(), [2, 3, 4, 5, 6])

    def test_get_row_col(self):
        board = Board(2, 3, 3, "X", "O")
        self.assertEqual(board.get_row_col_from_position(1), (0, 0))
        self.assertEqual(board.get_row_col_from_position(2), (0, 1))
        self.assertEqual(board.get_row_col_from_position(3), (0, 2))
        self.assertEqual(board.get_row_col_from_position(4), (1, 0))
        self.assertEqual(board.get_row_col_from_position(5), (1, 1))
        self.assertEqual(board.get_row_col_from_position(9), (2, 2))

    def test_set_move(self):
        preset = [["X", " ", " "],[" ", " ", " "]]
        board = Board(2, 3, 3, "X", "O", preset)
        self.assertRaises(CantMakeMoveException, board.set_move, 'K', 1)
        self.assertRaises(CantMakeMoveException, board.set_move, 'X', 1)
        board.set_move('X', 2)
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            board.show_board()
            self.assertEqual(fakeOutput.getvalue().strip(), '|X|X| |\n| | | |')
        board.set_move('O', 6)
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            board.show_board()
            self.assertEqual(fakeOutput.getvalue().strip(), '|X|X| |\n| | |O|')

    def test_is_win(self):
        preset = [["X", " ", " "],[" ", " ", " "]]
        board = Board(2, 3, 3, "X", "O", preset)
        self.assertRaises(CantEvaluateException, board.is_win, 'K')
        board.set_move('X', 3)
        self.assertEqual(board.is_win('X'), False)
        board.set_move('X', 2)
        self.assertEqual(board.is_win('X'), True)

        preset = preset = [["X", " ", " "],["X", " ", " "], ["X", " ", " "]]
        board = Board(3, 3, 3, "X", "O", preset)
        self.assertEqual(board.is_win('X'), True)

        preset = preset = [["X", " ", " "],["X", " ", " "], [" ", " ", " "]]
        board = Board(3, 3, 3, "X", "O", preset)
        self.assertEqual(board.is_win('X'), False)

        preset = preset = [["X", " ", " "],[" ", "X", " "], [" ", " ", "X"]]
        board = Board(3, 3, 3, "X", "O", preset)
        self.assertEqual(board.is_win('X'), True)

        preset = preset = [[" ", " ", " "],[" ", "X", " "], [" ", " ", "X"]]
        board = Board(3, 3, 3, "X", "O", preset)
        self.assertEqual(board.is_win('X'), False)

        preset = preset = [[" ", " ", "X"],[" ", "X", " "], ["X", " ", " "]]
        board = Board(3, 3, 3, "X", "O", preset)
        self.assertEqual(board.is_win('X'), True)

        preset = preset = [[" ", " ", "X"],[" ", "X", " "], [" ", " ", " "]]
        board = Board(3, 3, 3, "X", "O", preset)
        self.assertEqual(board.is_win('X'), False)

if __name__ == '__main__':
    unittest.main()