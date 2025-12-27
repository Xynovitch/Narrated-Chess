import chess
from stockfish import Stockfish
from config import STOCKFISH_PATH

class ChessGame:
    def __init__(self):
        self.board = chess.Board()
        self.engine = None
        
        if STOCKFISH_PATH:
            try:
                self.engine = Stockfish(path=STOCKFISH_PATH)
                self.engine.set_depth(10) # Adjust difficulty
            except Exception as e:
                print(f"Stockfish Error: {e}")
                print("Make sure the path in .env is correct and points to the executable.")
        else:
            print("Stockfish path not provided. AI will not move.")

    def make_move(self, move_uci):
        move = chess.Move.from_uci(move_uci)
        if move in self.board.legal_moves:
            self.board.push(move)
            if self.engine:
                self.engine.set_fen_position(self.board.fen())
            return True
        return False

    def get_ai_move(self):
        if self.engine and not self.board.is_game_over():
            return self.engine.get_best_move()
        return None