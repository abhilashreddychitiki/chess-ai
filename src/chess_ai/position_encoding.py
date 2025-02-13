import chess
import numpy as np

def encode_piece_position(board):
    """Encode piece positions into a binary tensor"""
    pieces = [chess.PAWN, chess.KNIGHT, chess.BISHOP, 
             chess.ROOK, chess.QUEEN, chess.KING]
    encoding = np.zeros((8, 8, 12), dtype=np.float32)
    
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            rank = chess.square_rank(square)
            file = chess.square_file(square)
            piece_idx = pieces.index(piece.piece_type)
            if not piece.color:  # If black
                piece_idx += 6
            encoding[rank, file, piece_idx] = 1
    
    return encoding

def encode_attack_maps(board):
    """Encode attack maps for both colors"""
    attack_map = np.zeros((8, 8, 2), dtype=np.float32)
    
    for square in chess.SQUARES:
        rank = chess.square_rank(square)
        file = chess.square_file(square)
        if board.is_attacked_by(chess.WHITE, square):
            attack_map[rank, file, 0] = 1
        if board.is_attacked_by(chess.BLACK, square):
            attack_map[rank, file, 1] = 1
    
    return attack_map

def encode_mobility(board):
    """Encode piece mobility"""
    mobility_map = np.zeros((8, 8), dtype=np.float32)
    
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            rank = chess.square_rank(square)
            file = chess.square_file(square)
            # Count legal moves for the piece
            board_copy = board.copy()
            mobility = sum(1 for move in board_copy.legal_moves 
                         if move.from_square == square)
            mobility_map[rank, file] = mobility
    
    return mobility_map

def encode_position(board):
    """Combine all encodings into one feature tensor"""
    piece_encoding = encode_piece_position(board)
    attack_encoding = encode_attack_maps(board)
    mobility_encoding = encode_mobility(board)
    
    # Combine all features
    return np.concatenate([
        piece_encoding,
        attack_encoding,
        mobility_encoding[:,:,np.newaxis]
    ], axis=2) 