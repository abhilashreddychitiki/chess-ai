"""
Chess GUI implementation using tkinter.
Provides a graphical interface for playing chess against the AI.
"""

import tkinter as tk
from tkinter import messagebox
import chess
from PIL import Image, ImageTk
from src.chess_ai.chess_ai import ModernChessAI
from src.chess_ai.config import Config

class ChessGUI:
    """
    A graphical user interface for the chess game.
    
    Attributes:
        root (tk.Tk): The main window of the application
        board (chess.Board): The chess board state
        ai (ModernChessAI): The AI opponent
        selected_square (int): Currently selected square on the board
        player_color (bool): Color of the human player (True for white)
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Game")
        self.board = chess.Board()
        self.ai = ModernChessAI(use_mcts=True, use_rl=True)
        
        # Initialize GUI components
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)
        
        # Create chess board display
        self.board_frame = tk.Frame(self.main_frame)
        self.board_frame.pack(side=tk.LEFT)
        self.buttons = [[None for _ in range(8)] for _ in range(8)]
        self.create_board_buttons()
        
        # Create side panel with controls
        self.side_panel = tk.Frame(self.main_frame)
        self.side_panel.pack(side=tk.LEFT, padx=20)
        
        # Move input controls
        self.move_label = tk.Label(self.side_panel, text="Enter move (e.g., e2e4):")
        self.move_label.pack()
        self.move_entry = tk.Entry(self.side_panel)
        self.move_entry.pack()
        self.make_move_button = tk.Button(self.side_panel, text="Make Move", command=self.make_player_move)
        self.make_move_button.pack(pady=5)
        
        # Game controls
        self.new_game_button = tk.Button(self.side_panel, text="New Game", command=self.new_game)
        self.new_game_button.pack(pady=5)
        
        # Status and history display
        self.status_label = tk.Label(self.side_panel, text="White to move", wraplength=150)
        self.status_label.pack(pady=10)
        self.history_label = tk.Label(self.side_panel, text="Move History:")
        self.history_label.pack()
        self.history_text = tk.Text(self.side_panel, height=10, width=20)
        self.history_text.pack()
        
        # Game state initialization
        self.selected_square = None
        self.player_color = self.choose_player_color()
        self.ai_color = chess.WHITE if self.player_color == chess.BLACK else chess.BLACK
        
        # Start game with AI move if AI is white
        if self.ai_color == chess.WHITE:
            self.make_ai_move()
        
        self.update_display()
        
    def create_board_buttons(self):
        """Creates the 8x8 grid of buttons representing the chess board"""
        for row in range(8):
            for col in range(8):
                color = "white" if (row + col) % 2 == 0 else "gray"
                button = tk.Button(self.board_frame, width=5, height=2, bg=color)
                button.grid(row=row, column=col)
                button.bind('<Button-1>', lambda e, r=row, c=col: self.square_clicked(r, c))
                self.buttons[row][col] = button
    
    def update_display(self):
        """Updates the visual representation of the board and game status"""
        # Update board squares
        for row in range(8):
            for col in range(8):
                square = chess.square(col, 7-row)
                piece = self.board.piece_at(square)
                text = self.get_piece_symbol(piece) if piece else ""
                self.buttons[row][col].config(text=text)
        
        # Update game status
        status = "White" if self.board.turn else "Black"
        if self.board.is_checkmate():
            status = f"Checkmate! {'Black' if self.board.turn else 'White'} wins!"
        elif self.board.is_stalemate():
            status = "Draw by stalemate!"
        elif self.board.is_insufficient_material():
            status = "Draw by insufficient material!"
        else:
            status = f"{status} to move"
        
        self.status_label.config(text=status)
    
    def get_piece_symbol(self, piece):
        """Converts chess piece to Unicode symbol"""
        if piece is None:
            return ""
        symbols = {
            'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
            'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
        }
        return symbols[piece.symbol()]
    
    def square_clicked(self, row, col):
        """Handles mouse clicks on the chess board"""
        square = chess.square(col, 7-row)
        if self.selected_square is None:
            if self.board.piece_at(square):
                self.selected_square = square
                self.buttons[row][col].config(bg='yellow')
        else:
            try:
                self.handle_move(self.selected_square, square)
            except ValueError:
                pass
            
            # Reset selection
            old_row = 7 - chess.square_rank(self.selected_square)
            old_col = chess.square_file(self.selected_square)
            old_color = "white" if (old_row + old_col) % 2 == 0 else "gray"
            self.buttons[old_row][old_col].config(bg=old_color)
            self.selected_square = None
    
    def handle_move(self, start_square, end_square):
        """Processes a move and triggers AI response"""
        # Check if this is a pawn promotion move
        piece = self.board.piece_at(start_square)
        is_promotion = (piece is not None and 
                       piece.piece_type == chess.PAWN and 
                       ((end_square >= 56 and piece.color) or  # White pawn reaching 8th rank
                        (end_square <= 7 and not piece.color)))  # Black pawn reaching 1st rank
        
        if is_promotion:
            # Create promotion dialog
            promotion_piece = self.show_promotion_dialog()
            move = chess.Move(start_square, end_square, promotion=promotion_piece)
        else:
            move = chess.Move(start_square, end_square)

        if move in self.board.legal_moves:
            self.board.push(move)
            self.update_display()
            self.history_text.insert(tk.END, f"{len(self.board.move_stack)}. {move.uci()}\n")
            
            if not self.board.is_game_over():
                self.make_ai_move()
    
    def show_promotion_dialog(self):
        """Shows a dialog for selecting promotion piece"""
        pieces = {
            'Queen': chess.QUEEN,
            'Rook': chess.ROOK,
            'Bishop': chess.BISHOP,
            'Knight': chess.KNIGHT
        }
        
        dialog = tk.Toplevel()
        dialog.title("Choose promotion piece")
        selected_piece = tk.StringVar(value='Queen')
        
        for piece_name in pieces.keys():
            tk.Radiobutton(dialog, text=piece_name, 
                          variable=selected_piece, 
                          value=piece_name).pack()
        
        button = tk.Button(dialog, text="OK", 
                          command=dialog.quit)
        button.pack()
        
        dialog.mainloop()
        piece_type = pieces[selected_piece.get()]
        dialog.destroy()
        return piece_type
    
    def make_player_move(self):
        """Processes moves entered via text input"""
        move_uci = self.move_entry.get().strip()
        try:
            move = chess.Move.from_uci(move_uci)
            if move in self.board.legal_moves:
                self.handle_move(move.from_square, move.to_square)
                self.move_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Illegal move!")
        except ValueError:
            messagebox.showerror("Error", "Invalid move format!")
    
    def make_ai_move(self):
        """Executes the AI's move"""
        if not self.board.is_game_over():
            ai_move = self.ai.get_best_move(self.board, time_limit=1.0)
            if ai_move:
                self.board.push(ai_move)
                self.update_display()
                self.history_text.insert(tk.END, f"{len(self.board.move_stack)}. {ai_move.uci()}\n")
    
    def new_game(self):
        """Resets the game to initial state"""
        self.board = chess.Board()
        self.history_text.delete(1.0, tk.END)
        self.update_display()

    def choose_player_color(self):
        """Displays color selection dialog"""
        popup = tk.Toplevel(self.root)
        popup.title("Choose Color")
        popup.geometry("300x150")
        popup.transient(self.root)
        
        result = [None]
        
        def set_color(color):
            result[0] = color
            popup.destroy()
        
        tk.Label(popup, text="Choose your color:", font=('Arial', 14)).pack(pady=10)
        tk.Button(popup, text="White", command=lambda: set_color(chess.WHITE)).pack(pady=5)
        tk.Button(popup, text="Black", command=lambda: set_color(chess.BLACK)).pack(pady=5)
        
        self.root.wait_window(popup)
        return result[0]

def main():
    # Create necessary directories
    Config.create_directories()
    
    # Initialize GUI
    root = tk.Tk()
    app = ChessGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 