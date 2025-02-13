import pytest
from train_ai import TrainingPipeline
from src.chess_ai.chess_ai import ModernChessAI
import chess
import os

@pytest.fixture
def training_pipeline():
    return TrainingPipeline()

def test_training_initialization(training_pipeline):
    assert training_pipeline.ai is not None
    assert training_pipeline.self_play_trainer is not None
    assert training_pipeline.stockfish_engine is not None

def test_stockfish_data_generation(training_pipeline):
    data = training_pipeline._generate_stockfish_data()
    assert 'positions' in data
    assert 'moves' in data
    assert 'values' in data
    assert len(data['positions']) > 0
    assert len(data['moves']) == len(data['positions'])
    assert len(data['values']) == len(data['positions'])

def test_model_saving(training_pipeline):
    model_path = training_pipeline._save_model()
    assert os.path.exists(model_path) 