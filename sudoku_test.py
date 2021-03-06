#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sudoku import (is_valid, find_next_position, find_empty_cell,
    solve_sudoku, board_to_str, row_to_pretty_str, board_to_pretty_str)
import unittest, copy

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
        self.board[8][8] = 3
        self.assertFalse(is_valid(num = 3, pos = (6, 6), board = self.board))

    def test_num_in_another_box(self):
        self.board[0][0] = 1
        self.assertTrue(is_valid(num = 1, pos = (5, 6), board = self.board))

class NextPositionTest(unittest.TestCase):

    def setUp(self):
        self.board = [[None for i in range(9)] for j in range(9)]

    def test_inner_pos(self):
        self.assertEqual(find_next_position(self.board, 2, 2), (3, 2))

    def test_outer_pos(self):
        self.assertEqual(find_next_position(self.board, 8, 4), (0, 5))

class FindEmptyCellTest(unittest.TestCase):

    def test_empty_board(self):
        board = [[None for i in range(9)] for j in range(9)]
        self.assertEqual(find_empty_cell(board), (0, 0))

    def test_nonempty_board(self):
        board = [[2 for i in range(9)] for j in range(9)]
        board[5][4] = None
        self.assertEqual(find_empty_cell(board, start_pos = (1, 4)), (5, 4))

    def test_board_without_gaps(self):
        board = [[2 for i in range(9)] for j in range(9)]
        self.assertEqual(find_empty_cell(board), (0, 9))

class SolveSudokuTest(unittest.TestCase):

    solution = [[8, 2, 7, 1, 5, 4, 3, 9, 6],
                [9, 6, 5, 3, 2, 7, 1, 4, 8],
                [3, 4, 1, 6, 8, 9, 7, 5, 2],
                [5, 9, 3, 4, 6, 8, 2, 7, 1],
                [4, 7, 2, 5, 1, 3, 6, 8, 9],
                [6, 1, 8, 9, 7, 2, 4, 3, 5],
                [7, 8, 6, 2, 3, 5, 9, 1, 4],
                [1, 5, 4, 7, 9, 6, 8, 2, 3],
                [2, 3, 9, 8, 4, 1, 5, 6, 7]]

    def setUp(self):
        self.board = copy.deepcopy(SolveSudokuTest.solution)

    def test_single_gap(self):
        self.board[4][7] = None
        solve_sudoku(self.board)
        self.assertListEqual(self.board, SolveSudokuTest.solution)

    def test_multiple_gaps(self):
        self.board[1][3] = None
        self.board[5][2] = None
        self.board[7][6] = None
        self.board[4][8] = None
        solve_sudoku(self.board)
        self.assertListEqual(self.board, SolveSudokuTest.solution)

    def test_empty_board(self):
        self.board = [[None for i in range(9)] for j in range(9)]
        self.assertTrue(solve_sudoku(self.board))

class BoardToStrTest(unittest.TestCase):

    def test_empty_board(self):
        self.empty = [[None for i in range(9)] for j in range(9)]
        self.assertEqual(board_to_str(self.empty), (' '*9 + '\n')*8 + ' '*9)

    def test_nonempty_board(self):
        self.board = [[2 for i in range(9)] for j in range(9)]
        self.assertEqual(board_to_str(self.board), ('2'*9 + '\n')*8 + '2'*9)

class RowToPrettyStrTest(unittest.TestCase):

    def test_empty_row(self):
        self.empty = [None for i in range(9)]
        self.assertEqual(row_to_pretty_str(self.empty),
            '┃   │   │   ┃   │   │   ┃   │   │   ┃')

    def test_nonempty_row(self):
        self.row = [2 for i in range(9)]
        self.assertEqual(row_to_pretty_str(self.row),
            '┃ 2 │ 2 │ 2 ┃ 2 │ 2 │ 2 ┃ 2 │ 2 │ 2 ┃')

class BoardToPrettyStrTest(unittest.TestCase):

    def test_conversion(self):
        board = [[8, 2, 7, 1, 5, None, 3, 9, 6],
                 [9, None, 5, 3, 2, 7, 1, 4, 8],
                 [3, 4, 1, 6, 8, 9, 7, 5, None],
                 [None, 9, 3, 4, 6, 8, 2, 7, 1],
                 [4, 7, 2, 5, 1, 3, None, 8, 9],
                 [6, 1, 8, 9, 7, 2, 4, None, 5],
                 [7, 8, 6, 2, None, 5, 9, 1, 4],
                 [1, 5, None, 7, 9, 6, 8, 2, 3],
                 [2, 3, 9, 8, 4, 1, 5, 6, None]]
        solution = ('┏━━━┯━━━┯━━━┳━━━┯━━━┯━━━┳━━━┯━━━┯━━━┓\n'
                    '┃ 8 │ 2 │ 7 ┃ 1 │ 5 │   ┃ 3 │ 9 │ 6 ┃\n'
                    '┠───┼───┼───╂───┼───┼───╂───┼───┼───┨\n'
                    '┃ 9 │   │ 5 ┃ 3 │ 2 │ 7 ┃ 1 │ 4 │ 8 ┃\n'
                    '┠───┼───┼───╂───┼───┼───╂───┼───┼───┨\n'
                    '┃ 3 │ 4 │ 1 ┃ 6 │ 8 │ 9 ┃ 7 │ 5 │   ┃\n'
                    '┣━━━┿━━━┿━━━╋━━━┿━━━┿━━━╋━━━┿━━━┿━━━┫\n'
                    '┃   │ 9 │ 3 ┃ 4 │ 6 │ 8 ┃ 2 │ 7 │ 1 ┃\n'
                    '┠───┼───┼───╂───┼───┼───╂───┼───┼───┨\n'
                    '┃ 4 │ 7 │ 2 ┃ 5 │ 1 │ 3 ┃   │ 8 │ 9 ┃\n'
                    '┠───┼───┼───╂───┼───┼───╂───┼───┼───┨\n'
                    '┃ 6 │ 1 │ 8 ┃ 9 │ 7 │ 2 ┃ 4 │   │ 5 ┃\n'
                    '┣━━━┿━━━┿━━━╋━━━┿━━━┿━━━╋━━━┿━━━┿━━━┫\n'
                    '┃ 7 │ 8 │ 6 ┃ 2 │   │ 5 ┃ 9 │ 1 │ 4 ┃\n'
                    '┠───┼───┼───╂───┼───┼───╂───┼───┼───┨\n'
                    '┃ 1 │ 5 │   ┃ 7 │ 9 │ 6 ┃ 8 │ 2 │ 3 ┃\n'
                    '┠───┼───┼───╂───┼───┼───╂───┼───┼───┨\n'
                    '┃ 2 │ 3 │ 9 ┃ 8 │ 4 │ 1 ┃ 5 │ 6 │   ┃\n'
                    '┗━━━┷━━━┷━━━┻━━━┷━━━┷━━━┻━━━┷━━━┷━━━┛')
        self.assertEqual(board_to_pretty_str(board), solution)

if __name__ == '__main__':
    unittest.main()
