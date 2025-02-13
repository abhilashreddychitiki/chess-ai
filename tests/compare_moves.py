import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chess
import stockfish
from src.chess_ai.chess_ai import ModernChessAI
from src.chess_ai.config import PATHS  # Import PATHS from config

def compare_moves():
    stockfish_engine = stockfish.Stockfish(path=PATHS['stockfish'])  # Use path from config
    board = chess.Board()
    ai = ModernChessAI()

    # Compare moves in different positions
    positions = [
        board.fen(),  # Starting position
        "r1bqkb1r/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 2 4",  # Mid-game
        "8/8/8/4k3/4P3/4K3/8/8 w - - 0 1"  # Endgame
    ]

    for pos in positions:
        board.set_fen(pos)
        
        ai_move = ai.get_best_move(board, time_limit=1.0)
        stockfish_engine.set_fen_position(pos)
        stockfish_move = stockfish_engine.get_best_move()

        print(f"\nPosition: {pos}")
        print(f"🤖 AI Move: {ai_move}")
        print(f"♟️ Stockfish Move: {stockfish_move}")
        print(f"Match: {'✅' if ai_move == stockfish_move else '❌'}")

if __name__ == "__main__":
    compare_moves()
