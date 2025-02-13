import chess
import math
import random
from evaluation import evaluate_board
from src.chess_ai.config import Config  # Import the Config class

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
        self.children = {}
        self.wins = 0
        self.visits = 0
        self.untried_moves = list(board.legal_moves)
        
    def ucb1(self):
        """Calculate UCB1 value for node selection"""
        if self.visits == 0:
            return float('inf')
        return (self.wins / self.visits + 
                1.41 * math.sqrt(math.log(self.parent.visits) / self.visits))
    
    def select_child(self):
        """Select child with highest UCB1 value"""
        if not self.children:
            return None
        return max(self.children, key=lambda c: c.ucb1())

class MCTS:
    """
    Monte Carlo Tree Search algorithm implementation.
    
    Attributes:
        board (chess.Board): Starting position
        time_limit (float): Time limit for search in seconds
        exploration_constant (float): UCB1 exploration parameter
        max_iterations (int): Maximum number of iterations
        max_depth (int): Maximum depth for rollouts
        root (Node): Root node of the search tree
    """
    def __init__(self, board, time_limit):
        self.board = board
        self.time_limit = time_limit
        self.exploration_constant = Config.MCTS_SETTINGS['exploration_constant']
        self.max_iterations = Config.MCTS_SETTINGS['max_iterations']
        self.max_depth = Config.MCTS_SETTINGS['max_depth']
        self.root = Node(board)
    
    def get_best_move(self):
        # Implement MCTS logic here
        pass

    def select(self):
        """Select a leaf node to expand"""
        node = self.root
        while node.untried_moves == [] and node.children != []:
            node = node.select_child()
        return node
    
    def expand(self, node):
        """Expand a leaf node by adding a child"""
        if node.untried_moves:
            move = random.choice(node.untried_moves)
            node.untried_moves.remove(move)
            new_board = node.board.copy()
            new_board.push(move)
            child = Node(new_board, parent=node)
            node.children[move] = child
            return child
        return node
    
    def simulate(self, node):
        """Simulate a random game from the node"""
        board = node.board.copy()
        depth = 0
        
        while not board.is_game_over() and depth < 50:
            moves = list(board.legal_moves)
            move = random.choice(moves)
            board.push(move)
            depth += 1
        
        # Use evaluation function for terminal state
        return evaluate_board(board)
    
    def backpropagate(self, node, result):
        """Update node statistics"""
        while node is not None:
            node.visits += 1
            node.wins += result
            node = node.parent
            result = -result
    
    def get_best_move(self):
        """Get the best move according to MCTS"""
        import time
        start_time = time.time()
        
        while time.time() - start_time < self.time_limit:
            leaf = self.select()
            child = self.expand(leaf)
            result = self.simulate(child)
            self.backpropagate(child, result)
        
        # Return move of most visited child
        return max(self.root.children, key=lambda c: c.visits).move 