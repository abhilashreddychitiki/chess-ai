import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Environment
    ENV = os.getenv('ENVIRONMENT', 'development')
    
    # Base directory setup
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    
    # Paths
    PATHS = {
        'opening_book': os.path.join(DATA_DIR, 'books', 'Perfect2023.bin'),
        'tablebase': os.path.join(DATA_DIR, 'tablebases', 'syzygy'),
        'model_save': os.path.join(DATA_DIR, 'models', 'chess_model.pth'),
        'stockfish': os.getenv('STOCKFISH_PATH', r"/path/to/stockfish"),
    }
    
    # AI Settings
    MCTS_SETTINGS = {
        'exploration_constant': float(os.getenv('MCTS_EXPLORATION_CONSTANT', '1.41')),
        'max_iterations': int(os.getenv('MCTS_MAX_ITERATIONS', '1000')),
        'max_depth': int(os.getenv('MCTS_MAX_DEPTH', '50'))
    }
    
    RL_SETTINGS = {
        'learning_rate': float(os.getenv('RL_LEARNING_RATE', '0.001')),
        'batch_size': int(os.getenv('RL_BATCH_SIZE', '64')),
        'num_epochs': int(os.getenv('RL_NUM_EPOCHS', '10'))
    }
    
    TIME_SETTINGS = {
        'initial_time': 180,  # 3 minutes
        'increment': 2,
        'min_time_per_move': 0.1,
        'max_time_percentage': 0.2
    }

    @classmethod
    def create_directories(cls):
        """Create necessary directories for the project"""
        directories = [
            os.path.join(cls.DATA_DIR, 'models'),
            os.path.join(cls.DATA_DIR, 'logs'),
            os.path.join(cls.DATA_DIR, 'tablebases'),
            os.path.join(cls.DATA_DIR, 'books')
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True) 