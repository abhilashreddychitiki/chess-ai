import chess
from chess_ai import find_best_move_alpha_beta

def play():
    board = chess.Board()

    while not board.is_game_over():
        print(board)  # Display board

        if board.turn == chess.WHITE:
            # AI plays as White
            ai_move = find_best_move_alpha_beta(board, depth=3)
            print(f"AI plays: {ai_move}")
            board.push(ai_move)
        else:
            # Human plays as Black
            human_move = input("Enter your move: ")
            try:
                board.push_san(human_move)
            except:
                print("Invalid move, try again.")

    print("Game over!")
    print("Result:", board.result())

if __name__ == "__main__":
    play()
