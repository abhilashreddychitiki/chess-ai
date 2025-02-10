import chess

def evaluate_board(board):
    """
    Simple evaluation function that calculates material balance.
    """
    piece_values = {
        chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
        chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0
    }

    score = 0
    for piece_type in piece_values:
        score += len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
        score -= len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]

    return score

def minimax(board, depth, maximizing_player):
    """
    Minimax algorithm for move selection.
    """
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, False)
            board.pop()
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, True)
            board.pop()
            min_eval = min(min_eval, eval)
        return min_eval

def find_best_move(board, depth=3):
    """
    Finds the best move using Minimax.
    """
    best_move = None
    best_value = float('-inf')

    for move in board.legal_moves:
        board.push(move)
        move_value = minimax(board, depth - 1, False)
        board.pop()

        if move_value > best_value:
            best_value = move_value
            best_move = move

    return best_move
    if best_move is None:
        return None
    return best_move
