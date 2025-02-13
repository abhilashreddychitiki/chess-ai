import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from src.chess_ai.config import Config

class ChessNet(nn.Module):
    def __init__(self):
        super(ChessNet, self).__init__()
        # Input shape will be [batch_size, 15, 8, 8]
        self.conv1 = nn.Conv2d(15, 64, 3, padding=1)
        self.conv2 = nn.Conv2d(64, 128, 3, padding=1)
        self.conv3 = nn.Conv2d(128, 256, 3, padding=1)
        self.fc1 = nn.Linear(256 * 8 * 8, 1024)
        self.value_head = nn.Linear(1024, 1)
        self.policy_head = nn.Linear(1024, 4672)
        
    def forward(self, x):
        # Input shape is [batch_size, 8, 8, 15]
        # Need to reshape to [batch_size, 15, 8, 8]
        x = x.permute(0, 3, 1, 2).contiguous()
        
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = torch.relu(self.conv3(x))
        x = x.reshape(-1, 256 * 8 * 8)  # Using reshape instead of view
        x = torch.relu(self.fc1(x))
        value = torch.tanh(self.value_head(x))
        policy = torch.softmax(self.policy_head(x), dim=1)
        return policy, value

class RLTrainer:
    """
    Manages the training of the neural network model.
    
    Attributes:
        device (torch.device): CPU or GPU device for training
        model (ChessNet): Neural network model
        optimizer (torch.optim.Optimizer): Optimization algorithm
    """
    def __init__(self, model=None):
        """
        Initialize the RL trainer with optional pre-trained model.
        
        Args:
            model (ChessNet, optional): Pre-trained model to use
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = model if model else ChessNet().to(self.device)
        self.optimizer = optim.Adam(
            self.model.parameters(), 
            lr=Config.RL_SETTINGS['learning_rate']
        )
        print(f"Using device: {self.device}")
        
    def save_model(self):
        torch.save(self.model.state_dict(), Config.PATHS['model_save'])
        
    def load_model(self):
        try:
            self.model.load_state_dict(torch.load(Config.PATHS['model_save']))
            self.model.eval()  # Set the model to evaluation mode
        except FileNotFoundError:
            print("No saved model found. Training from scratch.")
        
    def board_to_tensor(self, board):
        """
        Convert a chess board to a tensor representation.
        
        Args:
            board (chess.Board): Chess position to encode
            
        Returns:
            np.ndarray: Encoded board state as a tensor
        """
        tensor = np.zeros((8, 8, 15), dtype=np.float32)
        piece_idx = {'P': 0, 'N': 1, 'B': 2, 'R': 3, 'Q': 4, 'K': 5}
        
        # Encode piece positions and additional features
        for square in range(64):
            piece = board.piece_at(square)
            if piece:
                rank, file = square // 8, square % 8
                offset = 0 if piece.color else 6
                tensor[rank, file, piece_idx[piece.symbol().upper()] + offset] = 1
        
        # Add game state features
        tensor[:, :, 12] = float(board.turn)
        tensor[:, :, 13] = float(board.has_kingside_castling_rights(True) or 
                                board.has_kingside_castling_rights(False))
        tensor[:, :, 14] = float(board.has_queenside_castling_rights(True) or 
                                board.has_queenside_castling_rights(False))
        
        return tensor
    
    def train_step(self, positions, moves, values):
        """Single training step"""
        try:
            self.model.train()
            self.optimizer.zero_grad()
            
            # Convert boards to tensors
            position_tensors = [self.board_to_tensor(board) for board in positions]
            position_tensor = torch.FloatTensor(np.stack(position_tensors)).to(self.device)
            
            # Create move policy tensors
            policy_tensors = torch.zeros((len(moves), 4672)).to(self.device)
            for i, move in enumerate(moves):
                from_square = move.from_square
                to_square = move.to_square
                move_index = from_square * 64 + to_square
                policy_tensors[i][move_index] = 1.0
            
            value_tensor = torch.FloatTensor(values).to(self.device)
            
            # Debug prints
            print(f"Position tensor shape: {position_tensor.shape}")
            print(f"Policy tensor shape: {policy_tensors.shape}")
            print(f"Value tensor shape: {value_tensor.shape}")
            
            # Forward pass
            policy_pred, value_pred = self.model(position_tensor)
            
            # Calculate losses
            policy_loss = -torch.sum(policy_tensors * torch.log(policy_pred + 1e-8))
            value_loss = torch.mean((value_tensor - value_pred.squeeze()) ** 2)
            total_loss = policy_loss + value_loss
            
            # Backward pass
            total_loss.backward()
            self.optimizer.step()
            
            return total_loss.item()
            
        except Exception as e:
            print(f"Error in train_step: {str(e)}")
            print(f"Tensor shapes:")
            print(f"Position tensor: {position_tensor.shape if 'position_tensor' in locals() else 'not created'}")
            print(f"Policy tensor: {policy_tensors.shape if 'policy_tensors' in locals() else 'not created'}")
            print(f"Value tensor: {value_tensor.shape if 'value_tensor' in locals() else 'not created'}")
            raise e
    
    def get_move_probabilities(self, board):
        """Get move probabilities from the current model"""
        self.model.eval()
        with torch.no_grad():
            position = self.board_to_tensor(board)
            position_tensor = torch.FloatTensor([position]).to(self.device)
            policy_pred, _ = self.model(position_tensor)
            return policy_pred.cpu().numpy()[0] 