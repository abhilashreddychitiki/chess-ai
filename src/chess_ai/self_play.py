"""
Self-play training module for the chess AI.
Generates training data through AI vs AI games.
"""

import chess
from src.chess_ai.chess_ai import ModernChessAI
import random

class SelfPlayTrainer:
    """
    Manages self-play training process for the AI.
    
    Attributes:
        num_games (int): Number of games to play
        positions (list): Collected board positions
        moves (list): Moves played in the games
        results (list): Game results for training
        ai (ModernChessAI): AI instance for self-play
    """
    def __init__(self, num_games=1000):
        self.num_games = num_games
        self.positions = []
        self.moves = []
        self.results = []
        self.ai = ModernChessAI(use_mcts=True, use_rl=True)
        
    def generate_game(self):
        board = chess.Board()
        game_positions = []
        game_moves = []
        
        while not board.is_game_over():
            # Add random moves occasionally to explore different positions
            if random.random() < 0.1:
                legal_moves = list(board.legal_moves)
                move = random.choice(legal_moves)
            else:
                move = self.ai.get_best_move(board, time_limit=0.1)
            
            game_positions.append(board.copy())
            game_moves.append(move)
            board.push(move)
        
        # Store game result
        result = board.result()
        if result == "1-0":
            final_score = 1.0
        elif result == "0-1":
            final_score = -1.0
        else:
            final_score = 0.0
            
        # Update position evaluations based on final result
        for pos, move in zip(game_positions, game_moves):
            self.positions.append(pos)
            self.moves.append(move)
            self.results.append(final_score)
            final_score *= -1  # Alternate for each position
        
        return game_moves, result
    
    def train(self):
        for i in range(self.num_games):
            moves, result = self.generate_game()
            print(f"Game {i+1}: {result} in {len(moves)} moves")
            
            # Train the RL model periodically
            if len(self.positions) >= 1000:
                self.ai.train(self.positions, self.moves, self.results)
                self.positions = []
                self.moves = []
                self.results = []
        
        return self.positions, self.moves, self.results 