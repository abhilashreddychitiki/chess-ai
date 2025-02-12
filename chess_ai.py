import chess
import chess.polyglot
import random

# Load Polyglot Opening Book
def get_opening_move(board, book_path="books/Perfect2023.bin"):  # Updated path to match your book
    """ Returns an opening book move if available. """
    try:
        with chess.polyglot.open_reader(book_path) as reader:
            for entry in reader.find_all(board):
                return entry.move
    except:
        return None  # If no book move found, return None

def evaluate_position(board):
    if board.is_checkmate():
        return -10000 if board.turn else 10000
    if board.is_stalemate() or board.is_insufficient_material():
        return 0
    
    # Piece values
    piece_values = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 20000
    }
    
    score = 0
    
    # Material and basic position evaluation
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            value = piece_values[piece.piece_type]
            if piece.color:
                score += value
            else:
                score -= value
    
    # Control of center
    central_squares = [chess.E4, chess.E5, chess.D4, chess.D5]
    for square in central_squares:
        if board.is_attacked_by(chess.WHITE, square):
            score += 10
        if board.is_attacked_by(chess.BLACK, square):
            score -= 10
    
    return score

def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_position(board)
    
    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def find_best_move(board, depth=3):
    opening_move = get_opening_move(board)
    if opening_move:
        return opening_move  # Use book move if available

    # Otherwise, use Minimax
    best_move = None
    best_value = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    for move in board.legal_moves:
        board.push(move)
        move_value = minimax(board, depth - 1, alpha, beta, False)
        board.pop()

        if move_value > best_value:
            best_value = move_value
            best_move = move

        alpha = max(alpha, best_value)

    return best_move

class ChessAI:
    """Simple chess AI that makes random legal moves"""
    
    def __init__(self):
        pass

    def get_best_move(self, board):
        """Returns a random legal move from the current position"""
        legal_moves = list(board.legal_moves)
        return random.choice(legal_moves) if legal_moves else None
