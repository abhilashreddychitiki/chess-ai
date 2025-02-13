import tkinter as tk
from chess_gui import ChessGUI

def main():
    root = tk.Tk()
    app = ChessGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 