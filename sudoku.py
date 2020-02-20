#!/usr/bin/env python

import sys

if sys.version[0] == '2': input = raw_input

def is_valid(num, pos, board):
    x, y = pos
    # Check horizontally and vertically
    for i in range(9):
        if board[x][i] == num: return False
        if board[i][y] == num: return False
    # Find top-left corner of the box containing pos
    dx, dy = x // 3, y // 3
    # Check box containing pos
    for i in range(3*dx, 3*dx + 3):
        for j in range(3*dy, 3*dy + 3):
            if board[i][j] == num: return False
    return True

def next_position(board, x, y):
    return (x + 1, y) if x + 1 < 9 else (0, y + 1)

def find_empty_cell(board, start_pos = (0, 0)):
    x, y = start_pos
    while x < 9 and y < 9 and board[x][y] != None:
        x, y = next_position(board, x, y)
    return x, y

def solve_sudoku(board, pos = (0, 0)):
    x, y = find_empty_cell(board, pos)
    # If all gaps have been filled, return True
    if x >= 9 or y >= 9: return True
    # Find all valid values
    values = [v for v in range(1, 10) if is_valid(v, (x, y), board)]
    while len(values) > 0:
        # Put them in the cell one by one
        board[x][y] = values[0]
        # Try to fill the other gaps
        if solve_sudoku(board, find_empty_cell(board, (x, y))): return True
        # Remove values which do not lead to a solution
        values.pop(0)
    return False
