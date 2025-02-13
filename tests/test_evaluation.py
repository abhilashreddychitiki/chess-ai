import chess
from evaluation import evaluate_board

def test_evaluate_board():
    board = chess.Board()
    print(f"Initial position evaluation: {evaluate_board(board)}")

    # After 1.e4
    board.push_san("e4")
    e4_eval = evaluate_board(board)
    print(f"After e4: {e4_eval}")

    # After 1...e5
    board.push_san("e5")
    e5_eval = evaluate_board(board)
    print(f"After e5: {e5_eval}")

    # After 2.Qh5
    board.push_san("Qh5")
    qh5_eval = evaluate_board(board)
    print(f"After Qh5: {qh5_eval}")
    
    # More flexible assertions
    assert abs(e4_eval - e5_eval) < 1.0, "Expected similar evaluation after e4-e5"
    assert qh5_eval >= e5_eval, "Expected Qh5 to not be worse than previous position"

    print("✅ `evaluate_board()` test passed!")

if __name__ == "__main__":
    test_evaluate_board()
