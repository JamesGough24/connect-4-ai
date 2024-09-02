import numpy as np
import pygame
import sys
import math
import random

ROW_COUNT = 6
COL_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)

def create_board():
    board = np.zeros((ROW_COUNT,COL_COUNT))
    return board

def make_selection(board, player):
    col = int(input(f"Player {player} Make Your Selection (0-6): "))
    while not is_valid_location(board, col):
        col = int(input(f"That move is Invalid. \nPlayer {player} Make Your Selection (0-6): "))
    return col

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    if col > (COL_COUNT - 1) or col < 0:
        return False
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
        
def make_move(board, col, player):
    if is_valid_location(board, col):
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, player)
        return (row, col)

def print_board(board):
    print(np.flip(board, 0))

def current_player(turn):
    if turn % 2 == 0:
        return 1
    else:
        return 2

def game_over(piece):
    print(f"Congratulations, Player {piece} wins!")
    
def winning_graphics(screen, turn, width, myfont):
    pygame.draw.rect(screen, (0,0,0), (0,0, width, SQUARESIZE))
    curr_player = current_player(turn)
    if curr_player == 1:
        label = myfont.render(f"Player {curr_player} Wins!", True, (255,0,0))
    else:
        label = myfont.render(f"Player {curr_player} Wins!", True, (255,255,0))
    screen.blit(label, (40,10))
    pygame.display.update()


def winning_move(board, turn, move):
    piece = current_player(turn)

    row = move[0]
    col = move[1]

    if horiz_win(board, piece, row, col) or vert_win(board, piece, row, col) or neg_diag_win(board, piece, row, col) or pos_diag_win(board, piece, row, col):
        return True
    
    else:
        return False

def horiz_win(board, piece, row, col):
    seq_left = 0
    seq_right = 0

    for step_left in range(1, col + 1):
        if board[row][col - step_left] == piece:
            seq_left += 1
        else:
            break
    
    for step_right in range(1, COL_COUNT - col):
        if board[row][col + step_right] == piece:
            seq_right += 1
        else:
            break
    
    horiz_seq = 1 + seq_left + seq_right

    if horiz_seq >= 4:
        return True
    else:
        False

def vert_win(board, piece, row, col):
    seq_up = 0
    seq_down = 0

    for step_up in range(1, ROW_COUNT - row):
        if board[row + step_up][col] == piece:
            seq_up += 1
        else:
            break
    
    for step_down in range(1, row + 1):
        if board[row - step_down][col] == piece:
            seq_down += 1
        else:
            break
    
    vert_seq = 1 + seq_up + seq_down

    if vert_seq >= 4:
        return True
    else:
        False

def neg_diag_win(board, piece, row, col):
    seq_left_side = 0
    seq_right_side = 0

    steps_left = min(ROW_COUNT - 1 - row, col)
    steps_right = min(row, COL_COUNT - 1 - col)

    for step_left in range(1, steps_left + 1):
        if board[row + step_left][col - step_left] == piece:
            seq_left_side += 1
        else:
            break
    
    for step_right in range(1, steps_right + 1):
        if board[row - step_right][col + step_right] == piece:
            seq_right_side += 1
        else:
            break
    
    neg_diag_seq = 1 + seq_left_side + seq_right_side

    if neg_diag_seq >= 4:
        return True
    else:
        False

def pos_diag_win(board, piece, row, col):
    seq_left_side = 0
    seq_right_side = 0

    steps_left = min(row, col)
    steps_right = min(ROW_COUNT - 1 - row, COL_COUNT - 1 - col)

    for step_left in range(1, steps_left + 1):
        if board[row - step_left][col - step_left] == piece:
            seq_left_side += 1
        else:
            break
    
    for step_right in range(1, steps_right + 1):
        if board[row + step_right][col + step_right] == piece:
            seq_right_side += 1
        else:
            break
    
    pos_diag_seq = 1 + seq_left_side + seq_right_side

    if pos_diag_seq >= 4:
        return True
    else:
        False

def evaluate_window(window, piece):
    score = 0

    opp_piece = 1
    if piece == 1:
        opp_piece = 2

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    elif window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 10

    return score

def score_position(board, piece):
    score = 0

    # Favour Center
    center_array = [int(i) for i in list(board[:,COL_COUNT//2])]
    center_count = center_array.count(2)
    score += center_count * 3

    # Score Horizontal    
    for row in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[row,:])]

        for col in range(COL_COUNT - 3):
            window = row_array[col:col+4]
            score += evaluate_window(window, piece)
    
    # Score Vertical
    for col in range(COL_COUNT):
        col_array = [int(i) for i in list(board[:,col])]

        for row in range(ROW_COUNT - 3):
            window = col_array[row:row+4]
            score += evaluate_window(window, piece)

    # Score Positive Diagonal
    for row in range(ROW_COUNT - 3):
        for col in range(COL_COUNT - 3):
            window = [board[row+i][col+i] for i in range(4)]
            score += evaluate_window(window, piece)
    
    # Score Negative Diagonal
    for row in range(ROW_COUNT - 3):
        for col in range(COL_COUNT - 3):
            window = [board[row+3-i][col+i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

def winning_position(board, turn):
    # Score Horizontal    
    for row in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[row,:])]

        for col in range(COL_COUNT - 3):
            window = row_array[col:col+4]
            if window.count(turn) == 4:
                return True
    
    # Score Vertical
    for col in range(COL_COUNT):
        col_array = [int(i) for i in list(board[:,col])]

        for row in range(ROW_COUNT - 3):
            window = col_array[row:row+4]
            if window.count(turn) == 4:
                return True

    # Score Positive Diagonal
    for row in range(ROW_COUNT - 3):
        for col in range(COL_COUNT - 3):
            window = [board[row+i][col+i] for i in range(4)]
            if window.count(turn) == 4:
                return True
    
    # Score Negative Diagonal
    for row in range(ROW_COUNT - 3):
        for col in range(COL_COUNT - 3):
            window = [board[row+3-i][col+i] for i in range(4)]
            if window.count(turn) == 4:
                return True

def is_terminal_node(board):
    return winning_position(board, 1) or winning_position(board, 2) or len(get_valid_locations(board)) == 0

# def minimax(board, depth, maximizingPlayer):
#     valid_locations = get_valid_locations(board)
#     is_terminal = is_terminal_node(board)

#     if depth == 0 or is_terminal:
#         if is_terminal:
#             if winning_position(board, 2):
#                 return (None, 100000000)
#             elif winning_position(board, 1):
#                 return (None, -10000000)
#             else:
#                 return (None, 0)
#         else:
#             return (0, score_position(board, 2))

#     if maximizingPlayer:
#         value = -math.inf
#         column = random.choice(valid_locations)
#         for col in valid_locations:
#             row = get_next_open_row(board, col)
#             board_copy = board.copy()
#             drop_piece(board_copy, row, col, 2)
#             new_score = minimax(board_copy, depth-1, False)[1]
#             if new_score > value:
#                 value = new_score
#                 column = col
#         return column, value

#     else:
#         value = math.inf
#         column = random.choice(valid_locations)
#         for col in valid_locations:
#             row = get_next_open_row(board, col)
#             board_copy = board.copy()
#             drop_piece(board_copy, row, col, 1)
#             new_score = minimax(board_copy, depth-1, True)[1]
#             if new_score < value:
#                 value = new_score
#                 column = col
#         return column, value

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_position(board, 2):
                return (None, 100000000)
            elif winning_position(board, 1):
                return (None, -10000000)
            else:
                return (None, 0)
        else:
            return (0, score_position(board, 2))

    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            board_copy = board.copy()
            drop_piece(board_copy, row, col, 2)
            new_score = minimax(board_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(value, alpha)
            if alpha >= beta:
                break
        return column, value

    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            board_copy = board.copy()
            drop_piece(board_copy, row, col, 1)
            new_score = minimax(board_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(value, beta)
            if alpha >= beta:
                break
        return column, value


def get_valid_locations(board):
    valid_locations = []

    for col in range(COL_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    
    return valid_locations

def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)

    best_score = -1000000
    best_col = random.randint(0, COL_COUNT - 1)

    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    
    return best_col


def draw_board(board, screen, SQUARESIZE, height):
    for col in range(COL_COUNT):
        for row in range(ROW_COUNT):
            pygame.draw.rect(screen, (0,0,255), (col*SQUARESIZE, row*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, (0,0,0), (int(col*SQUARESIZE+SQUARESIZE/2), int(row*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    for col in range(COL_COUNT):
        for row in range(ROW_COUNT):
            if board[row][col] == 1:
                pygame.draw.circle(screen, (255,0,0), (int(col*SQUARESIZE+SQUARESIZE/2), height - int(row*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, (255,255,0), (int(col*SQUARESIZE+SQUARESIZE/2), height - int(row*SQUARESIZE+SQUARESIZE/2)), RADIUS)

    pygame.display.update()
    pygame.display.set_caption("Connect 4")

def draw_turn_selection_buttons(screen):
    myfont = pygame.font.SysFont("Arial", 60)
    text = myfont.render("Choose who goes first!", 1, (255,255,255))
    screen.blit(text, (int(SQUARESIZE*2/5),int(SQUARESIZE*3/2)))

    player_button = Button((255,0,0), SQUARESIZE, int(SQUARESIZE*ROW_COUNT/2), int(SQUARESIZE*2), SQUARESIZE, "Player")
    ai_button = Button((255,255,0), int(SQUARESIZE*(ROW_COUNT-2)), int(SQUARESIZE*ROW_COUNT/2), int(SQUARESIZE*2), SQUARESIZE, "AI")

    pygame.display.update()

    return player_button, ai_button

def draw_difficulty_selection_buttons(screen):
    myfont = pygame.font.SysFont("Arial", 60)
    text = myfont.render("Choose the AI Difficulty!", 1, (255,255,255))
    screen.blit(text,(30,70))

    easy_button = Button((0,255,0), int(SQUARESIZE*5/2 - 10), int(SQUARESIZE*2), int(SQUARESIZE*2 + 20), SQUARESIZE, "Easy")
    medium_button = Button((255,255,0), int(SQUARESIZE*5/2 - 10), int(SQUARESIZE*7/2), int(SQUARESIZE*2 + 20), SQUARESIZE, "Medium")
    hard_button = Button((255,0,0), int(SQUARESIZE*5/2 - 10), int(SQUARESIZE*5), int(SQUARESIZE*2 + 20), SQUARESIZE, "Hard")

    pygame.display.update()

    return easy_button, medium_button, hard_button

class Button():
    def __init__(self, colour, x, y, width, height, text):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height), 0)

        font = pygame.font.SysFont('Arial', 60)
        text = font.render(self.text, 1, (0,0,0))
        screen.blit(text, (int(self.x + self.width/2 - text.get_width()/2), int(self.y + self.height/2 - text.get_height()/2)))

    def isTouching(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False
    
def main():
    board = create_board()

    game_over = False

    pygame.init()

    width = COL_COUNT * SQUARESIZE
    height = (ROW_COUNT+1) * SQUARESIZE

    size = (width, height)
    
    screen = pygame.display.set_mode(size)

    myfont = pygame.font.SysFont("Arial", 75)

    # Choose who goes first
    turn_chosen = False
    turn = -1

    player_button, ai_button = draw_turn_selection_buttons(screen)
    
    while not turn_chosen:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_button.isTouching(pos):
                    turn = 0
                    turn_chosen = True
                if ai_button.isTouching(pos):
                    turn = 1
                    turn_chosen = True
            
        pos = pygame.mouse.get_pos()

        if player_button.isTouching(pos):
            player_button.colour = (255,255,255)
        else:
            player_button.colour = (255,0,0)

        if ai_button.isTouching(pos):
            ai_button.colour = (255,255,255)
        else:
            ai_button.colour = (255,255,0)
            
        player_button.draw(screen)
        ai_button.draw(screen)

        pygame.display.update()

    # Choose AI Difficulty

    difficulty_chosen = False
    difficulty = -1

    pygame.Surface.fill(screen, (0,0,0))

    easy_button, medium_button, hard_button = draw_difficulty_selection_buttons(screen)
    
    while not difficulty_chosen:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.isTouching(pos):
                    print("Easy AI Chosen")
                    difficulty = 1
                    difficulty_chosen = True
                    pygame.draw.rect(screen, (0,0,0), (0,0, width, SQUARESIZE))


                if medium_button.isTouching(pos):
                    print("Medium AI Chosen")
                    difficulty = 2
                    difficulty_chosen = True
                    pygame.draw.rect(screen, (0,0,0), (0,0, width, SQUARESIZE))


                if hard_button.isTouching(pos):
                    print("Hard AI Chosen")
                    difficulty = 4
                    difficulty_chosen = True
                    pygame.draw.rect(screen, (0,0,0), (0,0, width, SQUARESIZE))


        pos = pygame.mouse.get_pos()

        if easy_button.isTouching(pos):
            easy_button.colour = (255,255,255)
        else:
            easy_button.colour = (0,255,0)

        if medium_button.isTouching(pos):
            medium_button.colour = (255,255,255)
        else:
            medium_button.colour = (255,255,0)
        
        if hard_button.isTouching(pos):
            hard_button.colour = (255,255,255)
        else:
            hard_button.colour = (255,0,0)
            
        easy_button.draw(screen)
        medium_button.draw(screen)
        hard_button.draw(screen)

        pygame.display.update()
    
    depth = difficulty

    # Prepare board and start game

    print_board(board)
    draw_board(board, screen, SQUARESIZE, height)
    pygame.display.update()

    hello = 3

    while not game_over:
        if turn % 2 == 0:
            player_move_done = False
            while not player_move_done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                    if event.type == pygame.MOUSEMOTION:
                        pygame.draw.rect(screen, (0,0,0), (0,0, width, SQUARESIZE))
                        posx = event.pos[0]
                        pygame.draw.circle(screen, (255,0,0), (posx, int(SQUARESIZE/2)), RADIUS)
                        pygame.display.update()
                
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        col = -1
                        while not is_valid_location(board, col):
                            posx = event.pos[0]
                            col = int(math.floor(posx/SQUARESIZE))
                        move = make_move(board, col, 1)
                        pygame.draw.circle(screen, (255,255,0), (posx, int(SQUARESIZE/2)), RADIUS)
                        player_move_done = True
        
        else:
            col, minimax_score = minimax(board, depth, -math.inf, math.inf, True)
            if difficulty == 1:
                if random.random() >= 0.65:
                    col = random.choice(get_valid_locations(board))
                    print(f"Turn: {turn}, Col: {col}")
            
            if difficulty == 2:
                if random.random() >= 0.8:
                    col = random.choice(get_valid_locations(board))
                    print(f"Turn: {turn}, Col: {col}")
            
            if difficulty == 4:
                if random.random() >= 0.9:
                    col = random.choice(get_valid_locations(board))
                    print(f"Turn: {turn}, Col: {col}")

            move = make_move(board, col, 2)
            pygame.time.wait(500)
            pygame.draw.circle(screen, (255, 255, 0), (col * SQUARESIZE + SQUARESIZE / 2, int(SQUARESIZE / 2)), RADIUS)

        pygame.draw.rect(screen, (0,0,0), (0,0, width, SQUARESIZE))
        print_board(board)
        draw_board(board, screen, SQUARESIZE, height)

        game_over = winning_move(board, turn, move)

        if game_over:
            winning_graphics(screen, turn, width, myfont)
            pygame.time.wait(3000)

        turn += 1

main()

