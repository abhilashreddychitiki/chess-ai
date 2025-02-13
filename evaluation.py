"""
Chess position evaluation functions.
Implements material counting, piece-square tables, and positional evaluation.
"""

import chess
import numpy as np
from src.chess_ai.position_encoding import encode_position

# Piece values
PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

# Position tables for piece-square evaluation
PAWN_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5, -5,-10,  0,  0,-10, -5,  5,
    5, 10, 10,-20,-20, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0
]

def evaluate_material(board):
    """
    Calculates material balance of the position.
    
    Args:
        board (chess.Board): Current board position
        
    Returns:
        int: Material balance score (positive favors white)
    """
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            value = PIECE_VALUES[piece.piece_type]
            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value
    return score

def evaluate_piece_position(board):
    """Evaluate piece positions using piece-square tables"""
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None and piece.piece_type == chess.PAWN:
            if piece.color == chess.WHITE:
                score += PAWN_TABLE[square]
            else:
                score -= PAWN_TABLE[63 - square]
    return score

def evaluate_center_control(board):
    """Evaluate control of the center squares"""
    central_squares = [chess.E4, chess.E5, chess.D4, chess.D5]
    score = 0
    for square in central_squares:
        if board.is_attacked_by(chess.WHITE, square):
            score += 10
        if board.is_attacked_by(chess.BLACK, square):
            score -= 10
    return score

def evaluate_board(board):
    """Enhanced evaluation function using new position encoding"""
    if board.is_checkmate():
        return -10000 if board.turn else 10000
    if board.is_stalemate() or board.is_insufficient_material():
        return 0
    
    # Get position encoding
    features = encode_position(board)
    
    # Basic material and position evaluation
    material_score = evaluate_material(board)
    position_score = evaluate_piece_position(board)
    
    # Enhanced evaluation using mobility and attack maps
    mobility_score = np.sum(features[:,:,-1]) * 0.1
    attack_score = (np.sum(features[:,:,-3]) - np.sum(features[:,:,-2])) * 5
    
    return material_score + position_score + mobility_score + attack_score
