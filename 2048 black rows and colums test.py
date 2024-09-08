
# DO NOT TOUCH THIS CODE. THIS IS THE ONLY VERSION THAT WORKS PROPERLY


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
            pygame.draw.rect(screen, CELL_COLOR if value else CELL_EMPTY_COLOR, rect)
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


#Main
def main():
    board = initialize_board()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("2048 Game")
    clock = pygame.time.Clock()
    animations = {} # dictionary to store animation states

    while True:
        draw_board(board, screen, animations)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_UP):
                    apply_move(board, 'w')
                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    apply_move(board, 's')
                elif event.key in (pygame.K_a, pygame.K_LEFT):
                    apply_move(board, 'a')
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    apply_move(board, 'd')
                add_new_tile(board)
                animations.clear() # clears animations after move
                if is_game_over(board):
                    print("Game Over")
                    pygame.quit()
                    sys.exit()
        clock.tick(10)

if __name__ == "__main__":
    main()