# Gomuku (Five in a Row) Project - ESC180 Project
# Work done by Mani Majd and Eric Huang

import random

def is_empty(board: list) -> bool:
    for row in board:
        row_set = set(row)
        if len(row_set) != 1 or ' ' not in row_set:
            return False
    return True

def is_full(board: list) -> bool:
    for row in board:
        for column in row:
            if column == ' ':
                return False
    return True
    
def is_bounded(board: list, y_end: int, x_end: int, length: int, d_y: int, d_x: int) -> str:
    stone = board[y_end][x_end]
    left_y_end, left_x_end = y_end - (d_y * (length - 1)), x_end - (d_x * (length - 1))
    left_bounded, right_bounded = False, False
    if d_y == 0 and d_x == 1:
        left_bounded = (left_x_end <= 0 or board[left_y_end][left_x_end - 1] not in [stone, ' '])
        right_bounded = (x_end >= 7 or board[y_end][x_end + 1] not in [stone, ' '])
    elif d_y == 1 and d_x == 0:
        # in this case left_bounded implies top_bounded, and right_bounded implies bottom_bounded
        left_bounded = (left_y_end <= 0 or board[left_y_end - 1][left_x_end] not in [stone, ' '])
        right_bounded = (y_end >= 7 or board[y_end + 1][x_end] not in [stone, ' '])
    elif d_y == 1 and d_x == 1:
        left_bounded = ((left_x_end <= 0 or left_y_end <= 0) or (board[left_y_end - 1][left_x_end - 1] not in [stone, ' ']))
        right_bounded = ((y_end >= 7 or x_end >= 7) or (board[y_end + 1][x_end + 1] not in [stone, ' ']))
    elif d_y == 1 and d_x == -1:
        # left and right flip here
        left_bounded = ((left_x_end >= 7 or left_y_end <= 0) or (board[left_y_end - 1][left_x_end + 1] not in [stone, ' ']))
        right_bounded = ((x_end <= 0 or y_end >= 7) or (board[y_end + 1][x_end - 1] not in [stone, ' ']))
    return "SEMIOPEN" if left_bounded != right_bounded else ("CLOSED" if left_bounded and right_bounded else "OPEN")

def is_full_sequence(board: list, y_start: int, x_start: int, y_end: int, x_end: int, d_y: int, d_x: int, col: str) -> bool:
    left_in_bound = 0 <= y_start - d_y <= 7 and 0 <= x_start - d_x <= 7
    left_full = (not left_in_bound) or board[y_start - d_y][x_start - d_x] != col
    right_in_bound = 0 <= y_end + d_y <= 7 and 0 <= x_end + d_x <= 7
    right_full = (not right_in_bound) or board[y_end + d_y][x_end + d_x] != col
    return (left_full and right_full)

def detect_row(board: list, col: str, y_start: int, x_start: int, length: int, d_y: int, d_x: int) -> tuple:
    if d_y == 1 and d_x == 1 and (y_start == 7 or x_start == 7):
        y_start, x_start = (7 - x_start, 0) if y_start == 7 else (0, 7 - y_start)
    elif d_y == 1 and d_x == -1 and (y_start == 7 or x_start == 0):
        x_start, y_start = y_start, x_start
    elif d_y == 0 and d_x == 1 and x_start == 7:
        x_start = 0
    elif d_y == 1 and d_x == 0 and y_start == 7:
        y_start = 0
    open_seq_count, semi_open_seq_count = 0, 0
    y_end, x_end = 1, 1
    i = 0
    while 0 <= x_end < 8 and 0 <= y_end < 8:
        y_end = (y_start + (i + length - 1) * d_y)
        x_end = (x_start + (i + length - 1) * d_x)
        if y_end >= 8 or y_end < 0 or x_end >= 8 or x_end < 0:
            break
        for j in range(length):
            y = (y_start + (i + j) * d_y)
            x = (x_start + (i + j) * d_x)
            if board[y][x] != col: # sequence is "broken"
                break
        else:
            if board[y_end][x_end] == col and is_full_sequence(board, y_start + i * d_y, x_start + i * d_x, y_end, x_end, d_y, d_x, col):
                r = is_bounded(board, y_end, x_end, length, d_y, d_x)
                if r == "SEMIOPEN":
                    semi_open_seq_count += 1
                elif r == "OPEN":
                    open_seq_count += 1
        i += 1
    return open_seq_count, semi_open_seq_count
    
def detect_rows(board: list, col: str, length: int) -> tuple:
    open_seq_count, semi_open_seq_count = 0, 0

    for direction_comb in [(0, 1), (1, 0), (1, 1), (1, -1)]:
        for start in range(8):
            d_y, d_x = direction_comb
            if direction_comb == (0, 1):
                open_seq_inc, semi_open_seq_inc = detect_row(board, col, start, 0, length, d_y, d_x)
            elif direction_comb == (1, 0):
                open_seq_inc, semi_open_seq_inc = detect_row(board, col, 0, start, length, d_y, d_x)
            elif direction_comb == (1, 1):
                open_seq_inc, semi_open_seq_inc = detect_row(board, col, start, 0, length, d_y, d_x)
                if start != 0:
                    temp_inc, temp_inc_semi = detect_row(board, col, 0, start, length, d_y, d_x)
                    open_seq_inc += temp_inc
                    semi_open_seq_inc += temp_inc_semi
            elif direction_comb == (1, -1):
                open_seq_inc, semi_open_seq_inc = detect_row(board, col, start, 7, length, d_y, d_x)
                if start != 7:
                    temp_inc, temp_inc_semi = detect_row(board, col, 0, start, length, d_y, d_x)
                    open_seq_inc += temp_inc
                    semi_open_seq_inc += temp_inc_semi

            open_seq_count += open_seq_inc
            semi_open_seq_count += semi_open_seq_inc

    return open_seq_count, semi_open_seq_count

def search_max(board: list) -> tuple:
    move_y, move_x = 0, 0
    max_score = float("-inf")
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == ' ':
                board[y][x] = 'b'
                sc = score(board)
                if sc > max_score:
                    max_score = sc
                    move_y = y
                    move_x = x
                board[y][x] = ' ' # restore
    return move_y, move_x
    
def score(board):
    MAX_SCORE = 100000
    
    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}
    
    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
        
    
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE
        
    return (-10000 * (open_w[4] + semi_open_w[4])+ 
            500  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -100  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            10   * semi_open_b[3]                +  
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])
    
def is_win(board: list) -> str:
    if is_full(board):
        return "Draw"
    for col in ['b', 'w']:
        for direction_comb in [(0, 1), (1, 0), (1, 1), (1, -1)]:
            for y_start in range(8):
                for x_start in range(8):
                    if board[y_start][x_start] == col:
                        num_in_row = 1
                        curr_y, curr_x = y_start, x_start
                        d_y, d_x = direction_comb
                        while True:
                            curr_y += d_y
                            curr_x += d_x
                            if (not (0 <= curr_y < 8 and 0 <= curr_x < 8)) or board[curr_y][curr_x] != col:
                                break
                            num_in_row += 1
                        if num_in_row == 5 and is_full_sequence(board, y_start, x_start, curr_y - d_y, curr_x - d_x, d_y, d_x, col):
                            return "Black won" if col == 'b' else "White won"
    return "Continue playing"

def print_board(board):
    
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"
    
    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1]) 
    
        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    
    print(s)
    
def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board
                
def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))

def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    
    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)
            
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col        
        y += d_y
        x += d_x

def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    
    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    
    y = 3; x = 5; d_x = -1; d_y = 1; length = 2
    
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #     
    
    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);
    
    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #        
    #        
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0


if __name__ == '__main__':
    # play_gomoku(8)
    board = [
        ['w', ' ', ' ', ' ', 'b', ' ', ' ', 'w'],
        [' ', 'b', ' ', 'b', ' ', ' ', ' ', ' '],
        [' ', ' ', 'w', ' ', ' ', ' ', ' ', ' '],
        [' ', 'b', ' ', ' ', ' ', 'w', 'b', ' '],
        [' ', ' ', 'b', ' ', ' ', 'w', ' ', ' '],
        ['w', ' ', 'w', 'b', 'b', 'b', 'b', 'b'],
        [' ', ' ', ' ', ' ', ' ', 'b', ' ', ' '],
        [' ', 'b', 'w', 'w', ' ', ' ', 'w', 'b']
    ]
    print(is_win(board))
