from src.chess_ai.self_play import SelfPlayTrainer
from src.chess_ai.config import Config

def main():
    # Create necessary directories
    Config.create_directories()
    
    # Initialize trainer
    trainer = SelfPlayTrainer(num_games=100)  # Adjust number of games as needed
    
    # Start training
    print("Starting self-play training...")
    positions, moves, results = trainer.train()
    
    print(f"\nTraining completed!")
    print(f"Total positions collected: {len(positions)}")
    print(f"Total moves analyzed: {len(moves)}")

if __name__ == "__main__":
    main() 