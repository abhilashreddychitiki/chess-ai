import chess
from src.chess_ai.chess_ai import ModernChessAI
from src.chess_ai.config import Config
from utils.logger import setup_logger

def play():
    """
    Start a chess game between human player and AI.
    Handles move input, validation, and game flow.
    """
    board = chess.Board()
    ai = ModernChessAI(use_mcts=True, use_rl=True)
    logger = setup_logger()

    while not board.is_game_over():
        print(board)
        
        if board.turn:  # AI's turn (White)
            ai_move = ai.get_best_move(board, time_limit=1.0)
            board.push(ai_move)
            logger.info(f"AI plays: {ai_move}")
            print(f"AI plays: {ai_move}")
        else:  # Human's turn (Black)
            while True:
                try:
                    human_move = input("Enter your move (e.g., e2e4): ")
                    board.push_san(human_move)
                    logger.info(f"Human plays: {human_move}")
                    break
                except ValueError:
                    print("Invalid move, please try again.")

    print("Game over!")
    print(f"Result: {board.result()}")

if __name__ == "__main__":
    play()