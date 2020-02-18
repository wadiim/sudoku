from sudoku import is_valid
import unittest

class IsValidTest(unittest.TestCase):

    def setUp(self):
        self.board = [[None for i in range(9)] for j in range(9)]

    def test_empty_board(self):
        self.assertTrue(is_valid(num = 2, pos = (1, 6), board = self.board))

    def test_horizontal_conflict(self):
        self.board[2][2] = 7
        self.assertFalse(is_valid(num = 7, pos = (8, 2), board = self.board))

    def test_vertical_conflict(self):
        self.board[1][3] = 5
        self.assertFalse(is_valid(num = 5, pos = (1, 6), board = self.board))

    def test_box_conflict(self):
        self.board[1][1] = 3
        self.assertFalse(is_valid(num = 3, pos = (2, 2), board = self.board))

    def test_num_in_another_box(self):
        self.board[0][0] = 1
        self.assertTrue(is_valid(num = 1, pos = (5, 6), board = self.board))
