import tkinter as tk
from tkinter import scrolledtext
import chess
import threading
from engine import ChessGame
from narrator import Storyteller

class ChessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Narrated Chess: Chronicles of the 64 Squares")
        self.root.geometry("950x650")
        
        self.game = ChessGame()
        self.storyteller = Storyteller()
        self.selected_square = None 
        
        self.init_ui()
        self.update_board_ui()
        self.log_narrative("The armies assemble. The Kingdom of Light prepares to strike.")

    def init_ui(self):
        # --- Layout Containers ---
        self.main_container = tk.Frame(self.root, bg="#2c3e50")
        self.main_container.pack(fill="both", expand=True)

        self.board_frame = tk.Frame(self.main_container, bg="#34495e")
        self.board_frame.pack(side="left", padx=20, pady=20)
        
        self.narrative_frame = tk.Frame(self.main_container, bg="#ecf0f1", width=300)
        self.narrative_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # --- Narrative Area ---
        tk.Label(self.narrative_frame, text="The Chronicle", font=("Garamond", 20, "bold"), bg="#ecf0f1").pack(pady=10)
        
        self.text_area = scrolledtext.ScrolledText(self.narrative_frame, font=("Georgia", 12), wrap=tk.WORD, height=20)
        self.text_area.pack(fill="both", expand=True, padx=10, pady=10)
        self.text_area.config(state=tk.DISABLED) 

        # --- Chess Board Grid ---
        self.buttons = {}
        self.unicodes = {
            'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
            'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙',
            None: ' '
        }
        
        for r in range(8):
            for c in range(8):
                # Calculate square index (0-63)
                sq_index = chess.square(c, 7-r)
                
                color = "#DDB88C" if (r + c) % 2 == 0 else "#A66D4F"
                
                btn = tk.Button(self.board_frame, text=" ", font=("Arial", 32), 
                                width=2, height=1, bg=color, activebackground="#7f8c8d",
                                command=lambda s=sq_index: self.on_square_click(s))
                btn.grid(row=r, column=c)
                self.buttons[sq_index] = btn

    def on_square_click(self, square):
        """Handle Human Clicks"""
        if self.selected_square is None:
            # First click: Select piece
            piece = self.game.board.piece_at(square)
            if piece and piece.color == self.game.board.turn: # Ensure it's user's turn
                self.selected_square = square
                self.highlight_square(square, "yellow")
        else:
            # Second click: Attempt Move
            move = chess.Move(self.selected_square, square)
            
            # Auto-promote to Queen for MVP simplicity
            if chess.Move(self.selected_square, square, promotion=chess.QUEEN) in self.game.board.legal_moves:
                move = chess.Move(self.selected_square, square, promotion=chess.QUEEN)

            if move in self.game.board.legal_moves:
                self.process_turn(move)
                self.selected_square = None
                self.reset_highlights()
                
                # Trigger AI Turn after delay
                self.root.after(500, self.run_ai_turn)
            else:
                # Invalid move -> Deselect
                self.selected_square = None
                self.reset_highlights()

    def process_turn(self, move):
        """Execute move, update UI, and generate narration."""
        self.game.board.push(move)
        if self.game.engine:
            self.game.engine.set_fen_position(self.game.board.fen())
        
        self.update_board_ui()
        self.root.update()
        
        # Thread the narrative generation
        description = self.storyteller.describe_move(self.game.board, move)
        threading.Thread(target=self.fetch_and_display_narration, args=(description,), daemon=True).start()

    def run_ai_turn(self):
        """Queries Stockfish for a move."""
        if self.game.board.is_game_over():
            return

        best_move_uci = self.game.get_ai_move()
        if best_move_uci:
            move = chess.Move.from_uci(best_move_uci)
            self.process_turn(move)

    def fetch_and_display_narration(self, description):
        """Threaded worker for LLM calls."""
        narrative = self.storyteller.generate_narrative(description)
        # Schedule the UI update on the main thread
        self.root.after(0, lambda: self.log_narrative(narrative))

    def log_narrative(self, text):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, text + "\n\n")
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)

    def update_board_ui(self):
        for square, btn in self.buttons.items():
            piece = self.game.board.piece_at(square)
            symbol = self.unicodes[piece.symbol()] if piece else " "
            btn.config(text=symbol)

    def highlight_square(self, square, color):
        self.buttons[square].config(bg=color)

    def reset_highlights(self):
        for r in range(8):
            for c in range(8):
                sq = chess.square(c, 7-r)
                color = "#DDB88C" if (r + c) % 2 == 0 else "#A66D4F"
                self.buttons[sq].config(bg=color)