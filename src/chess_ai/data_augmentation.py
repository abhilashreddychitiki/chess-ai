import chess
import numpy as np

def mirror_position(board):
    """Mirror the position horizontally"""
    fen_parts = board.fen().split()
    rows = fen_parts[0].split('/')
    mirrored_rows = [row[::-1] for row in rows]
    fen_parts[0] = '/'.join(mirrored_rows)
    new_board = chess.Board('/'.join(fen_parts))
    return new_board

def rotate_position(board, rotation):
    """Rotate the board by 90, 180, or 270 degrees"""
    piece_map = board.piece_map()
    rotated_map = {}
    
    for square, piece in piece_map.items():
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        
        if rotation == 90:
            new_file = rank
            new_rank = 7 - file
        elif rotation == 180:
            new_file = 7 - file
            new_rank = 7 - rank
        else:  # 270 degrees
            new_file = 7 - rank
            new_rank = file
            
        new_square = chess.square(new_file, new_rank)
        rotated_map[new_square] = piece
    
    new_board = chess.Board()
    new_board.clear()
    for square, piece in rotated_map.items():
        new_board.set_piece_at(square, piece)
    return new_board

def augment_position(board):
    """Generate augmented positions from a single position"""
    positions = [board]
    positions.append(mirror_position(board))
    
    for rotation in [90, 180, 270]:
        positions.append(rotate_position(board, rotation))
    
    return positions 