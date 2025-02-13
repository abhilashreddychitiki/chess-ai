import chess
import chess.syzygy
import os

class TablebaseManager:
    def __init__(self, path="tablebases/syzygy"):
        self.tablebase = None
        try:
            if os.path.exists(path):
                self.tablebase = chess.syzygy.open_tablebase(path)
        except:
            print("Warning: Tablebase initialization failed")
    
    def get_wdl(self, board):
        """Get win-draw-loss value from tablebase"""
        if self.tablebase and len(board.piece_map()) <= 7:
            try:
                return self.tablebase.get_wdl(board)
            except:
                return None
        return None
    
    def get_best_move(self, board):
        """Get best move from tablebase"""
        if self.tablebase and len(board.piece_map()) <= 7:
            try:
                return self.tablebase.get_best_move(board)
            except:
                return None
        return None 