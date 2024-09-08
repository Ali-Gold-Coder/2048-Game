import copy
import pygame
import random
import sys


# Initializing pygame
pygame.init()

#constants
SIZE = 4
CELL_SIZE = 100
GRID_SIZE = SIZE * CELL_SIZE
WINDOW_SIZE = GRID_SIZE + 2 * CELL_SIZE
BACKGROUND_COLOR = (187 , 173 , 160)
CELL_COLOR = (205 , 193 , 180)
CELL_EMPTY_COLOR = (205 , 193 , 180)
FONT_COLOR = (119 , 110 , 101)
FONT = pygame.font.SysFont("arial", 40)

# Color mapping for numbers
COLOR_MAPPING = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 117, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 124, 95),
    128: (237, 207, 114),
    256: (237, 207, 114),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

#initializing game board
def initialize_board():
    board = [[0] * SIZE for _ in range(SIZE)]
    add_new_tile(board)
    add_new_tile(board)
    return board

#adding new tile to the board
def add_new_tile(board):
    empty_cells = [(i , j) for i in range(SIZE) for j in range(SIZE) if board[i][j] == 0]
    if empty_cells:
        i , j = random.choice(empty_cells)
        board[i][j] = 2 if random.random() < 0.9 else 4

#slide and combine logic
def slide_and_combine(row):
    new_row = [i for i in row if i != 0]
    for i in range(len(new_row) - 1):
        if new_row[i] == new_row[i + 1]:
            new_row[i] *= 2
            new_row[i + 1 ] = 0

    new_row = [i for i in new_row if i != 0]
    return new_row + [0] * (SIZE - len(new_row))


#Apply move to the board
def apply_move(board , direction):
    if direction == 'w':
        for j in range(SIZE):
            column = slide_and_combine([board[i][j] for i in range(SIZE)])
            for i in range(SIZE):
                board[i][j] = column[i]

    elif direction == 's':
        for j in range(SIZE):
            column = slide_and_combine([board[i][j] for i in range(SIZE -1, -1, -1)])
            for i in range(SIZE):
                board[SIZE - 1 - i][j] = column[i]

    elif direction == 'a':
        for i in range(SIZE):
            board[i] = slide_and_combine(board[i])

    elif direction == 'd':
        for i in range(SIZE):
            board[i] = slide_and_combine(board[i][::-1])[::-1]



# Game over check

def is_game_over(board):
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == 0 or \
                    (i < SIZE - 1 and board[i][j] == board[i + 1][j] ) or \
                    (j < SIZE - 1 and board[i][j] == board[i][j + 1]):
                return False
    return True


# The board drawn with animation
def draw_board(board, screen, animations):
    screen.fill(BACKGROUND_COLOR)

    # Drawing grid lines
    for i in range(SIZE + 1):
        pygame.draw.line(screen, (0, 0, 0), (CELL_SIZE, i * CELL_SIZE + CELL_SIZE), (GRID_SIZE + CELL_SIZE, i * CELL_SIZE + CELL_SIZE), 6)
        pygame.draw.line(screen, (0, 0, 0), (i * CELL_SIZE + CELL_SIZE, CELL_SIZE), (i * CELL_SIZE + CELL_SIZE, GRID_SIZE + CELL_SIZE), 6)

    for i in range(SIZE):
        for j in range(SIZE):
            value = board[i][j]
            rect = pygame.Rect(j * CELL_SIZE + CELL_SIZE + 3, i * CELL_SIZE + CELL_SIZE + 3, CELL_SIZE - 6, CELL_SIZE - 6)
            cell_color = COLOR_MAPPING.get(value, CELL_EMPTY_COLOR)
            pygame.draw.rect(screen, cell_color, rect)
            if value:
                if(i , j) in animations:
                    #Animate numbers towards their positions
                    current_x, current_y = animations[(i , j)]
                    target_x, target_y = j * CELL_SIZE + CELL_SIZE + 3, i * CELL_SIZE + CELL_SIZE + 3
                    delta_x = (target_x - current_x) // 5
                    delta_y = (target_y - current_y) // 5
                    current_x += delta_x
                    current_y += delta_y
                    animations[(i, j)] = (current_x, current_y)
                    text = FONT.render(str(value),True,FONT_COLOR)
                    text_rect = text.get_rect(center=(current_x + (CELL_SIZE - 6) // 2, current_y + (CELL_SIZE - 6) // 2))
                    screen.blit(text , text_rect)
                else:
                    text = FONT.render(str(value), True , FONT_COLOR)
                    text_rect = text.get_rect(center = rect.center)
                    screen.blit(text, text_rect)



#
def evaluate(board):
    return sum(sum(row) for row in board)

def get_empty_cells(board):
    return [(i, j) for i in range (SIZE) for j in range (SIZE) if board[i][j] == 0]

def get_possible_moves(board):
    return ['w', 's', 'a', 'd']

def make_move(board, move):
    new_board = copy.deepcopy(board)
    apply_move(new_board, move)
    return new_board

def expectimax(board, depth, player_turn=True):
    if depth == 0 or is_game_over(board):
        return evaluate(board)

    if player_turn:
        max_score = float('-inf')
        for move in get_possible_moves(board):
            new_board = make_move(board, move)
            score = expectimax(new_board, depth - 1, False)
            max_score = max(max_score, score)
        return max_score
    else:
        empty_cells = get_empty_cells(board)
        if not empty_cells:
            return evaluate(board)
        expected_score = 0
        for cell in empty_cells:
            for tile_value in [2, 4]:
                new_board = copy.deepcopy(board)
                new_board[cell[0]][cell[1]] = tile_value
                probability = 0.9 if tile_value == 2 else 0.1
                score = expectimax(new_board, depth - 1, True)
                expected_score += probability * score
        return expected_score / len(empty_cells)

def get_best_move(board, depth):

    best_move = None
    max_score = float('-inf')
    for move in get_possible_moves(board):
        new_board = make_move(board, move)
        score = expectimax(new_board, depth - 1 , False)
        if score > max_score:
            max_score = score
            best_move = move
    return best_move


def main():
    board = initialize_board()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("2048 Game")
    clock = pygame.time.Clock()
    animations = {}  # dictionary to store animation states

    while True:
        draw_board(board, screen, animations)
        pygame.display.flip()

        # Check for user input to quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # AI Move
        best_move = get_best_move(board, 6)  # You can adjust the depth here
        if best_move:
            apply_move(board, best_move)
            add_new_tile(board)
            animations.clear()  # clears animations after move
            if is_game_over(board):
                print("Game Over")
                pygame.quit()
                sys.exit()

        clock.tick(10)

if __name__ == "__main__":
    main()