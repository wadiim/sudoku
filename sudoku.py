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
