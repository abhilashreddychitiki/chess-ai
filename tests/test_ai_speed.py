import chess
import time
from src.chess_ai.chess_ai import ModernChessAI

def test_ai_speed():
    board = chess.Board()
    ai = ModernChessAI()

    start_time = time.time()
    best_move = ai.get_best_move(board, time_limit=1.0)
    end_time = time.time()

    print(f"⏱️ AI found move {best_move} in {end_time - start_time:.2f} seconds")
    
    # Test different time limits
    for time_limit in [0.1, 0.5, 2.0]:
        start_time = time.time()
        move = ai.get_best_move(board, time_limit=time_limit)
        elapsed = time.time() - start_time
        print(f"Time limit: {time_limit}s - Move found: {move} in {elapsed:.2f}s")
        assert elapsed <= time_limit * 1.2, f"Move took too long for {time_limit}s limit"

if __name__ == "__main__":
    test_ai_speed()
