import chess
from src.chess_ai.chess_ai import ModernChessAI
from src.chess_ai.self_play import SelfPlayTrainer
import stockfish
from src.chess_ai.config import Config
from utils.logger import setup_logger
import traceback
import os
import random
from datetime import datetime

logger = setup_logger()

class TrainingPipeline:
    def __init__(self):
        self.config = Config()
        self.logger = logger
        
        try:
            self.ai = ModernChessAI(use_mcts=True, use_rl=True)
            self.self_play_trainer = SelfPlayTrainer(num_games=100)
            self.stockfish_engine = stockfish.Stockfish(path=Config.STOCKFISH_PATH)
        except Exception as e:
            self.logger.error(f"Failed to initialize training pipeline: {str(e)}")
            raise
    
    def train(self):
        try:
            self.logger.info("Starting AI training pipeline...")
            
            # Phase 1: Self-play training
            self.logger.info("Phase 1: Self-play training")
            positions, moves, results = self.self_play_trainer.train()
            
            # Train on self-play data
            self.ai.train(positions, moves, results)
            
            # Phase 2: Learn from Stockfish
            self.logger.info("Phase 2: Learning from Stockfish")
            stockfish_data = self._generate_stockfish_data()
            
            # Train on Stockfish data
            self.ai.train(
                stockfish_data['positions'],
                stockfish_data['moves'],
                stockfish_data['values']
            )
            
            # Save the trained model
            model_path = self._save_model()
            self.logger.info(f"Training complete! Model saved at: {model_path}")
            
        except Exception as e:
            self.logger.error(f"Training failed: {str(e)}\n{traceback.format_exc()}")
            raise
    
    def _generate_stockfish_data(self):
        positions, moves, values = [], [], []
        board = chess.Board()
        
        try:
            for _ in range(1000):
                if not self._process_position(board, positions, moves, values):
                    board.reset()
            return {'positions': positions, 'moves': moves, 'values': values}
        except Exception as e:
            self.logger.error(f"Stockfish data generation failed: {str(e)}")
            raise
    
    def _process_position(self, board, positions, moves, values):
        try:
            self.stockfish_engine.set_position(board.fen())
            best_move = self.stockfish_engine.get_best_move()
            
            if best_move:
                positions.append(board.copy())
                moves.append(chess.Move.from_uci(best_move))
                values.append(1.0)
                
                # Make a random move to generate new position
                legal_moves = list(board.legal_moves)
                if legal_moves:
                    board.push(random.choice(legal_moves))
                    return True
            return False
        except Exception as e:
            self.logger.warning(f"Failed to process position: {str(e)}")
            return False
    
    def _save_model(self):
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            model_path = os.path.join(
                Config.MODEL_PATH,
                f'chess_model_{timestamp}.pth'
            )
            self.ai.rl_trainer.save_model(model_path)
            return model_path
        except Exception as e:
            self.logger.error(f"Failed to save model: {str(e)}")
            raise

if __name__ == "__main__":
    Config.create_directories()
    pipeline = TrainingPipeline()
    pipeline.train() 