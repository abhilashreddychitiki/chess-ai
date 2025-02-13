# Chess AI Training Pipeline

A production-ready chess AI training system using Reinforcement Learning (RL) and Monte Carlo Tree Search (MCTS).

## Table of Contents

- [Features](#features)
- [Setup](#setup)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Testing](#testing)
- [Monitoring](#monitoring)
- [Configuration](#configuration)
- [Contributing](#contributing)

## Features

- **Self-Play Training**: Generates games by having the AI play against itself to improve its strategies.
- **Reinforcement Learning**: Trains the AI using RL techniques to evaluate and improve move selections.
- **Monte Carlo Tree Search (MCTS)**: Enhances decision-making by exploring possible move sequences.
- **Stockfish Integration**: Learns from the renowned Stockfish engine to benchmark and improve move quality.
- **Data Augmentation**: Augments training data by mirroring and rotating board positions.
- **Comprehensive Logging**: Logs training progress and system events for monitoring and debugging.
- **Modular Structure**: Organized codebase for ease of maintenance and scalability.

## Prerequisites

- Python 3.8 or higher
- CUDA-compatible GPU (recommended for training)
- Stockfish chess engine
- Opening book database

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/abhilashreddychitiki/chess-ai.git
   cd chess-ai-project
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Fill in the required settings in the `.env` file.

5. **Setup Stockfish**

   - Download and install Stockfish from [Stockfish Official Site](https://stockfishchess.org/download/).
   - Update the `STOCKFISH_PATH` in `.env` with the path to the Stockfish executable.

6. **Setup Opening Book**
   - Download the Perfect2023.bin opening book from [Computer Chess Download Page](https://sites.google.com/site/computerschess/download)
   - Place the opening book file in `data/books/Perfect2023.bin`
   - Ensure the path matches the configuration in `src/chess_ai/config.py`

## Directory Structure

```
chess-ai-project/
├── data/
│   ├── books/          # Opening book files
│   ├── logs/           # Training and game logs
│   ├── models/         # Saved model checkpoints
│   └── tablebases/     # Endgame tablebases
├── src/
│   └── chess_ai/       # Core AI implementation
├── tests/              # Test suite
└── utils/              # Utility functions
```

## Usage

### Train the AI

Run the training pipeline:

```bash
python train_ai.py
```

### Play Against the AI

Launch the graphical interface:

```bash
python -m tests.test_game
```

## Testing

Run all tests using `pytest`:

```bash
pytest tests/
```

### Specific Tests

- **AI Components**: `tests/test_ai.py`
- **Training Pipeline**: `tests/test_training.py`
- **Board Evaluation**: `tests/test_evaluation.py`
- **Stockfish Integration**: `tests/test_stockfish.py`
- **Move Comparison**: `tests/compare_moves.py`
- **AI Speed**: `tests/test_ai_speed.py`

## Monitoring

- **Logs**: Stored in the `logs/` directory with timestamp-based filenames (e.g., `chess_ai_20230427_153045.log`).
- **Model Saving**: Trained models are saved in the `models/` directory with timestamped filenames.

## Configuration

All settings can be configured via environment variables or the `.env` file. Refer to `.env.example` for available configurations.

### Important Configuration Options

- **Environment**

  - `ENVIRONMENT`: Set to `development` or `production`

- **Paths**

  - `STOCKFISH_PATH`: Path to the Stockfish executable
  - `MODEL_PATH`: Directory to save trained models

- **AI Settings**
  - `MCTS_EXPLORATION_CONSTANT`: Controls exploration vs exploitation in MCTS
  - `MCTS_MAX_ITERATIONS`: Maximum number of MCTS iterations
  - `MCTS_MAX_DEPTH`: Maximum depth for MCTS search
  - `RL_LEARNING_RATE`: Learning rate for neural network training
  - `RL_BATCH_SIZE`: Batch size for training
  - `RL_NUM_EPOCHS`: Number of training epochs

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.
