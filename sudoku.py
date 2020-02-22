#!/usr/bin/env python

import sys, random, argparse

if sys.version[0] == '2': input = raw_input

BOARD_SIZE = 81
BOARD_WIDTH = 9
BOX_WIDTH = 3
DEFAULT_RANDOM_INTERVAL = (32, 64)

# Box drawing characters
LIGHT_HORIZONTAL = u"\u2500"
HEAVY_HORIZONTAL = u"\u2501"
LIGHT_VERTICAL = u"\u2502"
HEAVY_VERTICAL = u"\u2503"
LIGHT_DOWN_AND_RIGHT = u"\u250C"
HEAVY_DOWN_AND_RIGHT = u"\u250F"
LIGHT_DOWN_AND_LEFT = u"\u2510"
HEAVY_DOWN_AND_LEFT = u"\u2513"
LIGHT_UP_AND_RIGHT = u"\u2514"
HEAVY_UP_AND_RIGHT = u"\u2517"
LIGHT_UP_AND_LEFT = u"\u2518"
HEAVY_UP_AND_LEFT = u"\u251B"
LIGHT_VERTICAL_AND_RIGHT = u"\u251C"
VERTICAL_HEAVY_AND_RIGHT_LIGHT = u"\u2520"
HEAVY_VERTICAL_AND_RIGHT = u"\u2523"
LIGHT_VERTICAL_AND_LEFT = u"\u2524"
VERTICAL_HEAVY_AND_LEFT_LIGHT = u"\u2528"
HEAVY_VERTICAL_AND_LEFT = u"\u252B"
LIGHT_DOWN_AND_HORIZONTAL = u"\u252C"
DOWN_LIGHT_AND_HORIZONTAL_HEAVY = u"\u252F"
HEAVY_DOWN_AND_HORIZONTAL = u"\u2533"
LIGHT_UP_AND_HORIZONTAL = u"\u2534"
UP_LIGHT_AND_HORIZONTAL_HEAVY = u"\u2537"
HEAVY_UP_AND_HORIZONTAL = u"\u253B"
LIGHT_VERTICAL_AND_HORIZONTAL = u"\u253C"
VERTICAL_LIGHT_AND_HORIZONTAL_HEAVY = u"\u253F"
VERTICAL_HEAVY_AND_HORIZONTAL_LIGHT = u"\u2542"
HEAVY_VERTICAL_AND_HORIZONTAL = u"\u254B"

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
    return HEAVY_VERTICAL + HEAVY_VERTICAL.join(LIGHT_VERTICAL.join(
        ' {} '.format(row_values[i + j*BOX_WIDTH]
        if row_values[i + j*BOX_WIDTH] else ' ')
        for i in range(BOX_WIDTH))
        for j in range(BOX_WIDTH)) + HEAVY_VERTICAL

def create_board_line(left_outer_intersection,
                      major_intersection,
                      minor_intersection,
                      horizontal,
                      right_outer_intersection):
    return left_outer_intersection + major_intersection.join(
        minor_intersection.join([BOX_WIDTH*horizontal
        for i in range(BOX_WIDTH)])
        for j in range(BOX_WIDTH)) + right_outer_intersection

def create_top_border():
    return create_board_line(HEAVY_DOWN_AND_RIGHT,
                             HEAVY_DOWN_AND_HORIZONTAL,
                             DOWN_LIGHT_AND_HORIZONTAL_HEAVY,
                             HEAVY_HORIZONTAL,
                             HEAVY_DOWN_AND_LEFT)

def create_bottom_border():
    return create_board_line(HEAVY_UP_AND_RIGHT,
                             HEAVY_UP_AND_HORIZONTAL,
                             UP_LIGHT_AND_HORIZONTAL_HEAVY,
                             HEAVY_HORIZONTAL,
                             HEAVY_UP_AND_LEFT)

def create_light_inner_border():
    return create_board_line(VERTICAL_HEAVY_AND_RIGHT_LIGHT,
                             VERTICAL_HEAVY_AND_HORIZONTAL_LIGHT,
                             LIGHT_VERTICAL_AND_HORIZONTAL,
                             LIGHT_HORIZONTAL,
                             VERTICAL_HEAVY_AND_LEFT_LIGHT)

def create_heavy_inner_border():
    return create_board_line(HEAVY_VERTICAL_AND_RIGHT,
                             HEAVY_VERTICAL_AND_HORIZONTAL,
                             VERTICAL_LIGHT_AND_HORIZONTAL_HEAVY,
                             HEAVY_HORIZONTAL,
                             HEAVY_VERTICAL_AND_LEFT)

def pretty_print_board(board):
    print(create_top_border())
    for i in range(2):
        for j in range(2):
            print(create_board_row(board[i*BOX_WIDTH + j]))
            print(create_light_inner_border())
        print(create_board_row(board[i*BOX_WIDTH + 2]))
        print(create_heavy_inner_border())
    for i in range(6, 8):
        print(create_board_row(board[i]))
        print(create_light_inner_border())
    print(create_board_row(board[-1]))
    print(create_bottom_border())

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
