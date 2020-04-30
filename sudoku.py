#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, random, argparse

if sys.version[0] == '2': input = raw_input

BOARD_SIZE = 81
BOARD_WIDTH = 9
BOX_WIDTH = 3
DEFAULT_RANDOM_INTERVAL = (32, 64)

def is_valid(num, pos, board):
    x, y = pos
    # Check horizontally and vertically
    for i in range(BOARD_WIDTH):
        if board[x][i] == num: return False
        if board[i][y] == num: return False
    # Find top-left corner of the box containing pos
    dx, dy = x // BOX_WIDTH, y // BOX_WIDTH
    # Check box containing pos
    for i in range(BOX_WIDTH*dx, BOX_WIDTH*dx + BOX_WIDTH):
        for j in range(BOX_WIDTH*dy, BOX_WIDTH*dy + BOX_WIDTH):
            if board[i][j] == num: return False
    return True

def next_position(board, x, y):
    return (x + 1, y) if x + 1 < BOARD_WIDTH else (0, y + 1)

def find_empty_cell(board, start_pos = (0, 0)):
    x, y = start_pos
    while x < BOARD_WIDTH and y < BOARD_WIDTH and board[x][y] != None:
        x, y = next_position(board, x, y)
    return x, y

def solve_sudoku(board, pos = (0, 0)):
    x, y = find_empty_cell(board, pos)
    # If all gaps have been filled, return True
    if x >= BOARD_WIDTH or y >= BOARD_WIDTH: return True
    # Find all valid values
    values = [v for v in range(1, BOARD_WIDTH + 1)
        if is_valid(v, (x, y), board)]
    while len(values) > 0:
        # Put them in the cell randomly
        board[x][y] = random.choice(values)
        # Try to fill the other gaps
        if solve_sudoku(board, find_empty_cell(board, (x, y))): return True
        # Remove values which do not lead to a solution
        values.remove(board[x][y])
    board[x][y] = None
    return False

def generate_sudoku(gaps):
    board = [[None for i in range(BOARD_WIDTH)] for j in range(BOARD_WIDTH)]
    solve_sudoku(board)
    while gaps:
        # Find random position
        x = random.randint(0, BOARD_WIDTH - 1)
        y = random.randint(0, BOARD_WIDTH - 1)
        # If the value at that position has already been deleted,
        # find another one
        if board[x][y] == None: continue
        # Otherwise, delete the value
        board[x][y] = None
        gaps -= 1
    return board

def print_board(board):
    print('\n'.join([''.join([str(i) if i else ' ' for i in row])
        for row in board]))

def create_board_row(row_values):
    return '┃' + '┃'.join('│'.join(
        ' {} '.format(row_values[i + j*BOX_WIDTH]
        if row_values[i + j*BOX_WIDTH] else ' ')
        for i in range(BOX_WIDTH))
        for j in range(BOX_WIDTH)) + '┃'

def pretty_print_board(board):
    sudoku = ['┏━━━┯━━━┯━━━┳━━━┯━━━┯━━━┳━━━┯━━━┯━━━┓', None,
              '┠───┼───┼───╂───┼───┼───╂───┼───┼───┨', None,
              '┠───┼───┼───╂───┼───┼───╂───┼───┼───┨', None,
              '┣━━━┿━━━┿━━━╋━━━┿━━━┿━━━╋━━━┿━━━┿━━━┫', None,
              '┠───┼───┼───╂───┼───┼───╂───┼───┼───┨', None,
              '┠───┼───┼───╂───┼───┼───╂───┼───┼───┨', None,
              '┣━━━┿━━━┿━━━╋━━━┿━━━┿━━━╋━━━┿━━━┿━━━┫', None,
              '┠───┼───┼───╂───┼───┼───╂───┼───┼───┨', None,
              '┠───┼───┼───╂───┼───┼───╂───┼───┼───┨', None,
              '┗━━━┷━━━┷━━━┻━━━┷━━━┷━━━┻━━━┷━━━┷━━━┛']

    for i in range(9): sudoku[2*i+1] = create_board_row(board[i])
    print('\n'.join(sudoku))

def parse_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s', '--solve', action = 'store_true',
        help = 'solve sudoku')
    group.add_argument('-g', '--generate', type = int, dest = 'GAPS',
        help = 'generate sudoku with GAPS gaps',
        default = random.randint(*DEFAULT_RANDOM_INTERVAL))
    parser.add_argument("--pretty", help = 'pretty-print the results',
        action="store_true")
    return parser.parse_args()

def main():
    args = parse_args()
    if args.solve:
        data = ''
        try:
            while True: data += input()
        except EOFError:
            data_len = len(data)
            if data_len < BOARD_SIZE: data += ' ' * (BOARD_SIZE - data_len)
            elif data_len > BOARD_SIZE: data = data[:BOARD_SIZE]
            board = [[int(i) if i != ' ' else None
                for i in data[BOARD_WIDTH*j:BOARD_WIDTH*j + BOARD_WIDTH]]
                for j in range(BOARD_WIDTH)]
            if not solve_sudoku(board):
                sys.stderr.write('Solving sudoku failed')
                sys.exit(1)
            if args.pretty: pretty_print_board(board)
            else: print_board(board)
    else:
        if args.pretty: pretty_print_board(generate_sudoku(args.GAPS))
        else: print_board(generate_sudoku(args.GAPS))

if __name__ == '__main__':
	main()
