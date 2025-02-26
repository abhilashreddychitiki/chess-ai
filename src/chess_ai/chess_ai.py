"""
Modern Chess AI implementation using MCTS and Reinforcement Learning.
Includes opening book and tablebase support.
"""

import chess
import chess.polyglot
import random
from src.mcts import MCTS
from src.chess_ai.reinforcement import RLTrainer
from src.time_management import TimeManager
from src.chess_ai.config import Config
from src.chess_ai.tablebase import TablebaseManager
import logging

logger = logging.getLogger(__name__)

# Load Polyglot Opening Book
def get_opening_move(board):
    """
    Retrieves a move from the opening book database.
    
    Args:
        board (chess.Board): Current board position
        
    Returns:
        chess.Move: A move from the opening book, or None if not found
    """
    try:
        with chess.polyglot.open_reader(Config.PATHS['opening_book']) as reader:
            for entry in reader.find_all(board):
                return entry.move
    except Exception as e:
        print(f"Opening book error: {str(e)}")
        return None

class ModernChessAI:
    """
    Advanced chess AI combining multiple strategies.
    
    Attributes:
        use_mcts (bool): Whether to use Monte Carlo Tree Search
        use_rl (bool): Whether to use Reinforcement Learning
        rl_trainer (RLTrainer): Neural network for move evaluation
        time_manager (TimeManager): Manages time control
        tablebase (TablebaseManager): Endgame tablebase handler
    """
    def __init__(self, use_mcts=True, use_rl=True):
        self.use_mcts = use_mcts
        self.use_rl = use_rl
        if use_rl:
            self.rl_trainer = RLTrainer()
            self.rl_trainer.load_model()  # Load the trained model
        self.time_manager = TimeManager(
            initial_time=Config.TIME_SETTINGS['initial_time'],
            increment=Config.TIME_SETTINGS['increment']
        )
        self.tablebase = TablebaseManager(path=Config.PATHS['tablebase'])
    
    def get_best_move(self, board, time_limit=1.0):
        """Get the best move for the current position"""
        # Reduce iterations to make moves faster (100 iterations per second instead of 1000)
        iterations = int(time_limit * 100)
        
        # Initialize MCTS with max_iterations
        mcts = MCTS(board, max_iterations=iterations)
        return mcts.get_best_move()
    
    def train(self, positions, moves, values=None):
        """Train the AI on a set of positions"""
        if not self.use_rl:
            return
        
        if values is None:
            values = [1.0] * len(positions)  # Default to positive values
        
        return self.rl_trainer.train_step(positions, moves, values)
