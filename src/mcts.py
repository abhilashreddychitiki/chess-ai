import chess
import math
import random
from evaluation import evaluate_board
from src.chess_ai.config import Config

class Node:
    """
    Node in the MCTS tree representing a board position.
    
    Attributes:
        board (chess.Board): Chess position at this node
        parent (Node): Parent node in the tree
        children (dict): Child nodes mapped by moves
        wins (float): Number of wins from this position
        visits (int): Number of times this node was visited
        untried_moves (list): Legal moves not yet explored
    """
    def __init__(self, board, parent=None):
        self.board = board.copy()
        self.parent = parent
        self.children = {}  # Map moves to nodes
        self.wins = 0
        self.visits = 0
        self.untried_moves = list(board.legal_moves)
    
    def ucb1(self):
        """Calculate UCB1 value for node selection"""
        if self.visits == 0:
            return float('inf')
        return (self.wins / self.visits + 
                Config.MCTS_SETTINGS['exploration_constant'] * 
                math.sqrt(math.log(self.parent.visits) / self.visits))
    
    def select_child(self):
        """Select child with highest UCB1 value"""
        if not self.children:
            return None
        return max(self.children.values(), key=lambda node: node.ucb1())
    
    def expand(self):
        """Expand the tree by adding a new child node"""
        if not self.untried_moves:
            return None
        
        move = self.untried_moves.pop()
        new_board = self.board.copy()
        new_board.push(move)
        child_node = Node(new_board, parent=self)
        self.children[move] = child_node
        return child_node
    
    def update(self, result):
        """Update node statistics"""
        self.visits += 1
        self.wins += result

class MCTS:
    def __init__(self, board, max_iterations=None):
        self.root = Node(board)
        self.max_iterations = max_iterations or Config.MCTS_SETTINGS['max_iterations']
    
    def select(self):
        """Select a leaf node using UCB1"""
        node = self.root
        while node.untried_moves == [] and node.children:
            node = node.select_child()
        return node
    
    def simulate(self, board):
        """Run a random simulation from the current position"""
        temp_board = board.copy()
        depth = 0
        max_depth = Config.MCTS_SETTINGS['max_depth']
        
        while not temp_board.is_game_over() and depth < max_depth:
            legal_moves = list(temp_board.legal_moves)
            move = random.choice(legal_moves)
            temp_board.push(move)
            depth += 1
        
        # Evaluate final position
        if temp_board.is_checkmate():
            return 1.0 if temp_board.turn != board.turn else 0.0
        elif temp_board.is_stalemate() or temp_board.is_insufficient_material():
            return 0.5
        else:
            # Use evaluation function for non-terminal positions
            eval_score = evaluate_board(temp_board)
            return 1.0 / (1.0 + math.exp(-eval_score/100))  # Sigmoid normalization
    
    def backpropagate(self, node, result):
        """Backpropagate the simulation result up the tree"""
        while node is not None:
            node.update(result)
            node = node.parent
            result = 1 - result  # Flip result for opponent
    
    def get_best_move(self):
        """Run MCTS and return the best move"""
        for _ in range(self.max_iterations):
            leaf = self.select()
            child = leaf.expand()
            
            if child is None:
                simulation_result = self.simulate(leaf.board)
            else:
                simulation_result = self.simulate(child.board)
                leaf = child
            
            self.backpropagate(leaf, simulation_result)
        
        # Select move with highest visit count
        if not self.root.children:
            return random.choice(list(self.root.board.legal_moves))
        
        return max(self.root.children.items(),
                  key=lambda x: x[1].visits)[0] 