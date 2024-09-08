import copy

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

def expectimax(board, depth, player_turn = True):
    if depth == 0 or is_game_over(board):
        return evaluate(board)

    if player_turn:
        max_scire = float('-inf')
        for move in get_possible_moves(board):
            new_board = make_move(board, move)
            score = expectimax(new_board, depth - 1, False )
            max_score = max(max_score, score)
            return max_score
        else:
            empty_cells = get_empty_cells(board)
            if not empty_cells:
                return evaluate(board)
            expected_score = 0
            for cell in empty_cells:
                for title_value in [2 , 4]:
                    new_board = copy.deepcopy(board)
                    new_board[cell[0]][cell[1]] = tile_value
                    probability = 0.9 if title_value == 2 else 0.1
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