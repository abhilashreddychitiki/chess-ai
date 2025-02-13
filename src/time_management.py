import chess
import time
from src.chess_ai.config import Config  # Import the Config class

class TimeManager:
    def __init__(self, initial_time=None, increment=None):
        self.initial_time = initial_time or Config.TIME_SETTINGS['initial_time']
        self.increment = increment or Config.TIME_SETTINGS['increment']
        self.remaining_time = self.initial_time
        self.move_count = 0
        
    def get_time_for_move(self, board):
        """Calculate how much time to spend on the current move"""
        # More time in complex positions, less in simple ones
        position_complexity = self._calculate_complexity(board)
        
        # Basic time management
        remaining_moves = max(40 - self.move_count, 20)  # Assume at least 20 more moves
        base_time = self.remaining_time / remaining_moves
        
        # Adjust for position complexity
        allocated_time = base_time * position_complexity
        
        # Never use more than 20% of remaining time
        max_time = self.remaining_time * Config.TIME_SETTINGS['max_time_percentage']
        allocated_time = min(allocated_time, max_time)
        
        return max(
            min(allocated_time, 
                self.remaining_time * Config.TIME_SETTINGS['max_time_percentage']),
            Config.TIME_SETTINGS['min_time_per_move']
        )
    
    def _calculate_complexity(self, board):
        """Calculate position complexity factor"""
        complexity = 1.0
        
        # More pieces = more complex
        piece_count = len(board.piece_map())
        complexity *= (piece_count / 32)
        
        # More legal moves = more complex
        move_count = len(list(board.legal_moves))
        complexity *= (move_count / 20)
        
        # Critical phases need more time
        if board.is_check():
            complexity *= 1.5
        
        return min(max(complexity, 0.5), 2.0)  # Keep between 0.5 and 2.0
    
    def update_clock(self, time_spent):
        """Update remaining time after a move"""
        self.remaining_time -= time_spent
        self.remaining_time += self.increment
        self.move_count += 1 