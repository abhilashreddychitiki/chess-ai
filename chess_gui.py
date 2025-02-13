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
import threading
import queue

PIECE_SYMBOLS = {
    'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',  # White pieces
    'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'   # Black pieces
}

class ChessGUI:
    """
    A graphical user interface for the chess game.
    
    Attributes:
        root (tk.Tk): The main window of the application
        board (chess.Board): The chess board state
        ai (ModernChessAI): The AI opponent
        selected_square (int): Currently selected square on the board
        player_color (bool): Color of the human player (True for white)
        ai_move_queue (queue.Queue): Queue for AI move calculations
        is_ai_thinking (bool): Indicates if AI is currently thinking
        last_ai_move (chess.Move): Store the last AI move
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Game")
        
        # Choose color before initializing board
        self.player_color = self.choose_player_color()
        if self.player_color is None:
            self.player_color = chess.WHITE
        
        self.board = chess.Board()
        self.ai = ModernChessAI(use_mcts=True, use_rl=True)
        
        # Initialize state variables
        self.selected_square = None
        self.ai_move_queue = queue.Queue()
        self.is_ai_thinking = False
        self.last_ai_move = None
        
        # Create GUI layout
        self.create_gui()
        
        # Schedule AI's first move if AI is white
        if not self.player_color:  # If player chose black (False)
            self.root.after(100, self.schedule_ai_move)
        
        self.update_display()
        
    def create_gui(self):
        """Create the main GUI layout"""
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)
        
        # Create board
        self.buttons = []
        for row in range(8):
            button_row = []
            for col in range(8):
                button = tk.Button(self.main_frame, width=4, height=2,
                                 command=lambda r=row, c=col: self.square_clicked(r, c))
                button.grid(row=row, column=col)
                button_row.append(button)
            self.buttons.append(button_row)
        
        # Create side panel
        self.side_panel = tk.Frame(self.root)
        self.side_panel.pack(side=tk.RIGHT, padx=10)
        
        # Move entry
        self.move_entry = tk.Entry(self.side_panel)
        self.move_entry.pack()
        
        # Buttons
        tk.Button(self.side_panel, text="Make Move", 
                 command=self.make_move_from_text).pack()
        tk.Button(self.side_panel, text="New Game", 
                 command=self.new_game).pack()
        
        # Status label
        self.status_label = tk.Label(self.side_panel, text="White to move")
        self.status_label.pack()
        
        # Move history
        self.history_text = tk.Text(self.side_panel, height=10, width=20)
        self.history_text.pack()
        
    def update_display(self):
        """Updates the visual representation of the board and game status"""
        # Update board squares
        for row in range(8):
            for col in range(8):
                square = chess.square(col, 7-row)
                piece = self.board.piece_at(square)
                text = self.get_piece_symbol(piece) if piece else ""
                
                # Determine square color
                base_color = "white" if (row + col) % 2 == 0 else "gray"
                
                # Highlight last AI move if exists
                if self.last_ai_move and (square == self.last_ai_move.from_square or 
                                        square == self.last_ai_move.to_square):
                    self.buttons[row][col].config(text=text, bg='light blue')
                else:
                    self.buttons[row][col].config(text=text, bg=base_color)
        
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
        return PIECE_SYMBOLS[piece.symbol()]
    
    def square_clicked(self, row, col):
        """Handles mouse clicks on the chess board"""
        # Prevent moves if it's not player's turn
        if self.board.turn != self.player_color:
            return
        
        square = chess.square(col, 7-row)
        
        # Reset previous selection if it exists
        if self.selected_square is not None:
            old_row = 7 - chess.square_rank(self.selected_square)
            old_col = chess.square_file(self.selected_square)
            old_color = "white" if (old_row + old_col) % 2 == 0 else "gray"
            self.buttons[old_row][old_col].config(bg=old_color)
        
        # If no square is selected, select this one if it has a piece
        if self.selected_square is None:
            piece = self.board.piece_at(square)
            if piece and piece.color == self.board.turn:
                self.selected_square = square
                self.buttons[row][col].config(bg='yellow')
        # If a square was already selected, try to make a move
        else:
            try:
                self.handle_move(self.selected_square, square)
            except ValueError:
                pass
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
            promotion_piece = self.show_promotion_dialog()
            move = chess.Move(start_square, end_square, promotion=promotion_piece)
        else:
            move = chess.Move(start_square, end_square)

        if move in self.board.legal_moves:
            # After making a player's move, clear the last AI move highlight
            self.last_ai_move = None  # Clear AI move highlight when player moves
            self.board.push(move)
            self.update_display()
            self.history_text.insert(tk.END, f"{len(self.board.move_stack)}. {move.uci()}\n")
            
            # Check if game is over after player's move
            if self.board.is_game_over():
                self.show_game_over_message()
                return
            
            # Schedule AI move after a short delay
            self.root.after(100, self.schedule_ai_move)

    def schedule_ai_move(self):
        """Schedule the AI move calculation"""
        self.disable_board()
        self.status_label.config(text="AI is thinking...")
        self.is_ai_thinking = True
        
        # Start AI calculation in a separate thread
        ai_thread = threading.Thread(target=self._calculate_ai_move)
        ai_thread.daemon = True
        ai_thread.start()
        
        # Check for AI move completion periodically
        self.root.after(100, self._check_ai_move)
    
    def _calculate_ai_move(self):
        """Calculate AI move in a separate thread"""
        try:
            ai_move = self.ai.get_best_move(self.board, time_limit=0.5)
            self.ai_move_queue.put(ai_move)
        except Exception as e:
            self.ai_move_queue.put(None)
            print(f"AI move calculation error: {e}")
    
    def _check_ai_move(self):
        """Check if AI move calculation is complete"""
        try:
            ai_move = self.ai_move_queue.get_nowait()
            
            if ai_move:
                self.board.push(ai_move)
                self.last_ai_move = ai_move  # Store the last AI move
                self.update_display()
                self.history_text.insert(tk.END, f"{len(self.board.move_stack)}. {ai_move.uci()}\n")
                
                if self.board.is_game_over():
                    self.show_game_over_message()
            
            self.enable_board()
            self.is_ai_thinking = False
            
        except queue.Empty:
            if self.is_ai_thinking:
                self.root.after(100, self._check_ai_move)

    def disable_board(self):
        """Disable board interaction"""
        for row in self.buttons:
            for button in row:
                button.config(state=tk.DISABLED)

    def enable_board(self):
        """Enable board interaction"""
        for row in self.buttons:
            for button in row:
                button.config(state=tk.NORMAL)
    
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
        dialog.transient(self.root)
        dialog.grab_set()  # Make dialog modal
        
        selected_piece = tk.StringVar(value='Queen')
        result = [chess.QUEEN]  # Default to Queen
        
        def on_ok():
            result[0] = pieces[selected_piece.get()]
            dialog.destroy()
        
        for piece_name in pieces.keys():
            tk.Radiobutton(dialog, text=piece_name, 
                          variable=selected_piece, 
                          value=piece_name).pack()
        
        tk.Button(dialog, text="OK", command=on_ok).pack()
        
        # Wait for dialog to close
        self.root.wait_window(dialog)
        return result[0]
    
    def show_game_over_message(self):
        """Shows game over message with the result"""
        if self.board.is_checkmate():
            winner = "Black" if self.board.turn == chess.WHITE else "White"
            message = f"Checkmate! {winner} wins!"
        elif self.board.is_stalemate():
            message = "Game Over - Stalemate!"
        elif self.board.is_insufficient_material():
            message = "Game Over - Draw by insufficient material!"
        elif self.board.is_fifty_moves():
            message = "Game Over - Draw by fifty-move rule!"
        elif self.board.is_repetition():
            message = "Game Over - Draw by repetition!"
        else:
            message = "Game Over!"
        
        messagebox.showinfo("Game Over", message)
    
    def make_move_from_text(self):
        """Processes moves entered via text input"""
        # Prevent moves if it's not player's turn
        if self.board.turn != self.player_color:
            messagebox.showerror("Error", "Not your turn!")
            return
        
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
    
    def new_game(self):
        """Resets the game to initial state"""
        self.board = chess.Board()
        self.history_text.delete(1.0, tk.END)
        self.update_display()

    def choose_player_color(self):
        """Let player choose their color"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Choose Your Color")
        dialog.transient(self.root)
        dialog.grab_set()
        
        color = [chess.WHITE]  # Default to white
        
        def set_color(is_white):
            color[0] = chess.WHITE if is_white else chess.BLACK
            dialog.destroy()
        
        # Center the buttons
        frame = tk.Frame(dialog)
        frame.pack(padx=20, pady=20)
        
        tk.Button(frame, text="White", width=10,
                 command=lambda: set_color(True)).pack(side=tk.LEFT, padx=10)
        tk.Button(frame, text="Black", width=10,
                 command=lambda: set_color(False)).pack(side=tk.LEFT, padx=10)
        
        # Wait for dialog
        self.root.wait_window(dialog)
        return color[0]

def main():
    # Create necessary directories
    Config.create_directories()
    
    # Initialize GUI
    root = tk.Tk()
    app = ChessGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 