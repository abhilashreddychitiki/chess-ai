from stockfish import Stockfish
from src.chess_ai.config import PATHS

def test_stockfish_installation():
    try:
        # Initialize Stockfish
        stockfish = Stockfish(path=PATHS['stockfish'])
        
        # Test if Stockfish is working
        stockfish.set_position([])
        best_move = stockfish.get_best_move()
        
        print("✅ Stockfish is working correctly!")
        print(f"Best move from starting position: {best_move}")
        
        # Test evaluation
        evaluation = stockfish.get_evaluation()
        print(f"\nPosition evaluation: {evaluation}")
        
        # Test setting position
        test_position = "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2"
        stockfish.set_fen_position(test_position)
        best_move = stockfish.get_best_move()
        print(f"Best move in test position: {best_move}")
        
    except Exception as e:
        print("❌ Error initializing Stockfish:")
        print(e)
        print("\nPlease check if:")
        print("1. The path in config.py is correct")
        print("2. Stockfish executable has proper permissions")
        print("3. You're using the correct version for your system")
        print("\nTrying to install/upgrade stockfish package...")
        print("Run: pip install --upgrade stockfish")

if __name__ == "__main__":
    test_stockfish_installation() 