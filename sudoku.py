#!/usr/bin/env python

import sys, random, argparse

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
        # Put them in the cell randomly
        board[x][y] = random.choice(values)
        # Try to fill the other gaps
        if solve_sudoku(board, find_empty_cell(board, (x, y))): return True
        # Remove values which do not lead to a solution
        values.pop(0)
    board[x][y] = None
    return False

def generate_sudoku(gaps = 22):
    board = [[None for i in range(9)] for j in range(9)]
    solve_sudoku(board)
    while gaps:
        # Find random position
        x = random.randint(0, 8)
        y = random.randint(0, 8)
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

def parse_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s', '--solve', action = 'store_true',
        help = 'solve sudoku')
    group.add_argument('-g', '--generate', type = int, dest = 'GAPS',
        help = 'generate sudoku with GAPS gaps',
        default = random.randint(32, 64))
    return parser.parse_args()

def main():
    args = parse_args()
    if args.solve:
        data = ''
        try:
            while True: data += input()
        except EOFError:
            if len(data) != 81:
                sys.stderr.write('Incorrect input')
                sys.exit(2)
            board = [[int(i) if i != ' ' else None for i in data[9*j:9*j + 9]]
                for j in range(9)]
            if not solve_sudoku(board):
                sys.stderr.write('Solving sudoku failed')
                sys.exit(1)
            print_board(board)
    else:
        print_board(generate_sudoku(args.GAPS))

if __name__ == '__main__':
	main()
