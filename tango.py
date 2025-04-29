import sys
from collections import defaultdict

SIZE = 6
SUN = 'S'
MOON = 'M'
SUNSYMBOL = '☼'
MOONSYMBOL = '☽'


def get_column(board, column_number):
    return [board[row_number][column_number] for row_number in range(SIZE)]


def get_row(board, row_number):
    return [board[row_number][column_number] for column_number in range(SIZE)]


# def set_column(board, column_number, column):
#     new_board = copy.deepcopy(board)
#     for row_number in range(SIZE):
#         new_board[row_number][column_number] = column[row_number]
#     return new_board
#
#
# def set_row(board, row_number, row):
#     new_board = copy.deepcopy(board)
#     for column_number in range(SIZE):
#         new_board[row_number][column_number] = row[column_number]
#     return new_board


def check_board(board, restrictions):
    def check_consecutive(name, func, num):
        string = ''.join(func(board, num))
        return 'SSS' not in string and 'MMM' not in string

    def check_too_many(name, func, num):
        check_list = func(board, num)
        return check_list.count(SUN) <= 3 and check_list.count(MOON) <= 3

    def check_restrictions():
        def get_restriction_cell(cell):
            x, y = (cell)
            ch = board[y][x]
            return ch

        for cell1 in restrictions:
            for cell2 in restrictions[cell1]:
                ch1 = get_restriction_cell(cell1)
                ch2 = get_restriction_cell(cell2)
                if ch1 == ' ' or ch2 == ' ':
                    continue

                restriction_type = restrictions[cell1][cell2]
                if restriction_type == 'x' and ch1 == ch2:
                    return False
                if restriction_type == '=' and ch1 != ch2:
                    return False

        return True

    if not check_restrictions():
        return False

    for n in range(SIZE):
        if not check_consecutive('column', get_column, n) \
                or not check_consecutive('row', get_row, n) \
                or not check_too_many('column', get_column, n) \
                or not check_too_many('row', get_row, n):
            return False

    return True


def parse_input(lines):
    board = [[' ' for _ in range(SIZE)] for _ in range(6)]
    restrictions = defaultdict(dict)

    for lineIndex in range(SIZE):
        border_chars = list(lines[lineIndex * 2])
        line_chars = list(lines[lineIndex * 2 + 1])

        for colIndex in range(SIZE):
            top_border = border_chars[colIndex * 2 + 1]
            left_border = line_chars[colIndex * 2]
            char = line_chars[colIndex * 2 + 1]

            if char not in ' MS':
                raise ValueError(f'[{colIndex},{lineIndex}] {char} invalid value')
            if left_border not in '|x=':
                raise ValueError(f'[{colIndex},{lineIndex}] {left_border} left invalid value')
            if top_border not in '-x=':
                raise ValueError(f'[{colIndex},{lineIndex}] {top_border} top invalid value')

            board[lineIndex][colIndex] = char

            if left_border in 'x=' and colIndex > 0:
                index1 = (colIndex - 1, lineIndex)
                index2 = (colIndex, lineIndex)
                restrictions[index1][index2] = left_border

            if top_border in 'x=' and lineIndex > 0:
                index1 = (colIndex, lineIndex - 1)
                index2 = (colIndex, lineIndex)
                if not restrictions.get(index1):
                    restrictions[index1] = dict()
                restrictions[index1][index2] = top_border

    return board, restrictions


def read_input(filename):
    try:
        with open(filename) as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        print(f'File not found {filename}')
        return None, None

    return parse_input(lines)


def solve_board(board, restrictions, cell_index):
    # print(cell_index)
    # print_board(board)

    if cell_index >= SIZE * SIZE:
        return board

    row_index = cell_index // SIZE
    col_index = cell_index % SIZE

    def try_solution(symbol):
        board[row_index][col_index] = symbol
        if check_board(board, restrictions):
            solved_board = solve_board(board, restrictions, cell_index + 1)
            if solved_board:
                return solved_board
        board[row_index][col_index] = ' '
        return None

    ch = board[row_index][col_index]
    if ch != ' ':
        return solve_board(board, restrictions, cell_index + 1)

    return try_solution(SUN) or try_solution(MOON)


def print_board(board):
    for line in [''.join(row) for row in board]:
        print(line.replace(SUN, SUNSYMBOL).replace(MOON, MOONSYMBOL))


def tango(filename):
    board, restrictions = read_input(filename)
    if board and restrictions:
        return solve_board(board, restrictions, 0)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'{sys.argv[0]} [filename]')
        exit(1)
    solved_board = tango(sys.argv[1])
    if solved_board:
        print_board(solved_board)
