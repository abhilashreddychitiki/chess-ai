import chess
from src.chess_ai.chess_ai import ModernChessAI

def test_ai_moves():
    """
    Test AI move generation in different game phases.
    Verifies that moves are legal and reasonable.
    """
    ai = ModernChessAI()
    
    # Test opening position
    board = chess.Board()
    best_move = ai.get_best_move(board, time_limit=0.5)
    assert best_move is not None, "AI should return a valid move"
    assert best_move in board.legal_moves, "AI must return a legal move"
    
    # Test mid-game position
    mid_game_fen = "r1bqkb1r/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 2 4"
    board.set_fen(mid_game_fen)
    best_move = ai.get_best_move(board, time_limit=0.5)
    assert best_move is not None, "AI should return a valid move"
    assert best_move in board.legal_moves, "AI must return a legal move"

def test_ai_components():
    ai = ModernChessAI(use_mcts=True, use_rl=True)
    
    # Test MCTS
    board = chess.Board()
    mcts_move = ai.get_best_move(board, time_limit=1.0)
    assert mcts_move in board.legal_moves, "MCTS should return a legal move"
    
    # Test RL
    ai_rl_only = ModernChessAI(use_mcts=False, use_rl=True)
    rl_move = ai_rl_only.get_best_move(board, time_limit=0.1)
    assert rl_move in board.legal_moves, "RL should return a legal move"
    print("RL move:", rl_move)

if __name__ == "__main__":
    test_ai_moves()
    test_ai_components()
    print("✅ All AI tests passed!") 