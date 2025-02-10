import chess

pawn_table = [
    0, 5, 5, 0, 5, 10, 50, 0,
    0, 10, -5, 0, 5, 15, 50, 0,
    0, 10, 10, 20, 30, 50, 50, 0,
    0, 10, 25, 35, 40, 50, 50, 0,
    0, 10, 25, 35, 40, 50, 50, 0,
    0, 10, 10, 20, 30, 50, 50, 0,
    0, 10, -5, 0, 5, 15, 50, 0,
    0, 5, 5, 0, 5, 10, 50, 0,
]

def evaluate_board(board):
    material_score = sum([
        len(board.pieces(chess.PAWN, chess.WHITE)) - len(board.pieces(chess.PAWN, chess.BLACK))
    ])

    return material_score
