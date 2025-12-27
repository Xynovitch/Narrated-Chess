import time
import chess
from openai import OpenAI
from config import OPENAI_API_KEY, MOCK_LLM_MODE

class Storyteller:
    def __init__(self):
        if not MOCK_LLM_MODE and OPENAI_API_KEY:
            self.client = OpenAI(api_key=OPENAI_API_KEY)
        else:
            self.client = None
            
        self.history = []  # Rolling memory
        
        # --- IDENTITY SYSTEM ---
        # We map square indices (0-63) to unique names.
        # This dictionary tracks where every named character is currently standing.
        self.unit_names = self._initialize_names()

    def _initialize_names(self):
        """Assigns unique names to the starting positions."""
        names = {}
        
        # --- WHITE (The Kingdom of Light) ---
        # Back Rank
        names[chess.A1] = "The Tower of Dawn"
        names[chess.B1] = "Sir Valerius (Cavalier)"
        names[chess.C1] = "Bishop Eldrin"
        names[chess.D1] = "Queen Aurelia"
        names[chess.E1] = "King Theoden"
        names[chess.F1] = "Bishop Caelum"
        names[chess.G1] = "Sir Galahad (Cavalier)"
        names[chess.H1] = "The Tower of Dusk"
        
        # Pawns (A2-H2)
        pawn_names = ["Squire Alaric", "Squire Baldric", "Squire Cedric", 
                      "Squire Darius", "Squire Elric", "Squire Finn", 
                      "Squire Garrick", "Squire Henry"]
        for i, name in enumerate(pawn_names):
            names[chess.square(i, 1)] = name

        # --- BLACK (The Shadow Empire) ---
        # Back Rank
        names[chess.A8] = "The Spire of Agony"
        names[chess.B8] = "Dark Rider Vane"
        names[chess.C8] = "Sorcerer Malgor"
        names[chess.D8] = "Empress Morgana"
        names[chess.E8] = "Lord Malakar"
        names[chess.F8] = "Sorcerer Zog"
        names[chess.G8] = "Dark Rider Kael"
        names[chess.H8] = "The Spire of Ruin"
        
        # Pawns (A7-H7)
        shadow_pawns = ["Minion Grunt", "Orc Berserker", "Goblin Spy", 
                        "Shadow Stalker", "Void Walker", "Dark Acolyte", 
                        "Blood Reaver", "Bone Crusher"]
        for i, name in enumerate(shadow_pawns):
            names[chess.square(i, 6)] = name
            
        return names

    def _update_positions(self, move):
        """Moves the name from origin to destination."""
        source = move.from_square
        dest = move.to_square
        
        # Get the actor's name
        actor_name = self.unit_names.get(source, "Unknown Soldier")
        
        # Move the actor in our tracking dict
        self.unit_names[dest] = actor_name
        # Clear the old spot
        if source in self.unit_names:
            del self.unit_names[source]
            
        # Handle Castling (The Rook moves too!)
        # Kingside White
        if source == chess.E1 and dest == chess.G1:
            self.unit_names[chess.F1] = self.unit_names.pop(chess.H1, "Rook")
        # Queenside White
        elif source == chess.E1 and dest == chess.C1:
            self.unit_names[chess.D1] = self.unit_names.pop(chess.A1, "Rook")
        # Kingside Black
        elif source == chess.E8 and dest == chess.G8:
            self.unit_names[chess.F8] = self.unit_names.pop(chess.H8, "Rook")
        # Queenside Black
        elif source == chess.E8 and dest == chess.C8:
            self.unit_names[chess.D8] = self.unit_names.pop(chess.A8, "Rook")

    def describe_move(self, board, move):
        """
        Describes the move using SPECIFIC NAMES and looks for tactics.
        """
        # 1. IDENTIFY ACTORS (Before we update internal state)
        actor_name = self.unit_names.get(move.from_square, "A nameless shadow")
        victim_name = self.unit_names.get(move.to_square, None) # Might be None if empty
        
        # 2. CHECK TACTICS (Using the board state)
        # Note: 'board' passed here usually has the move ALREADY pushed in previous code.
        # BUT for names, we need the board state *before* the move logic clears the capture.
        # To rely on our internal dict, we trust 'victim_name'. 
        
        # Determine capture
        board.pop() # Step back to pre-move state to verify capture flags
        is_capture = board.is_capture(move)
        is_check = board.gives_check(move) # Check if this move WILL give check
        board.push(move) # Restore board

        # 3. BUILD DESCRIPTION
        desc = f"{actor_name} moves to {chess.square_name(move.to_square)}."

        if is_capture and victim_name:
            desc = f"{actor_name} CHARGES and SLAUGHTERS {victim_name}!"
        
        if is_check:
            desc += " The enemy King is threatened by this blade!"

        # 4. THREAT DETECTION (Post-move analysis)
        # Who is 'actor_name' threatening now?
        attacked_squares = board.attacks(move.to_square)
        threat_list = []
        for sq in attacked_squares:
            target_piece = board.piece_at(sq)
            if target_piece and target_piece.color != board.turn: # Enemies (board.turn is currently the OTHER player, so we check != current turn? No, board.turn is next player.)
                # Actually simpler: Look up the name at that square in our dict
                threatened_name = self.unit_names.get(sq)
                if threatened_name:
                    threat_list.append(threatened_name)

        if threat_list:
            # Pick the most important sounding one
            important_threats = [t for t in threat_list if "Squire" not in t and "Minion" not in t]
            if important_threats:
                desc += f" {actor_name} is now pointing a weapon directly at {important_threats[0]}!"

        # 5. UPDATE INTERNAL TRACKING
        self._update_positions(move)

        return desc

    def generate_narrative(self, move_description):
        if MOCK_LLM_MODE or not self.client:
            time.sleep(0.5) 
            return f"[MOCK POET] {move_description}"

        context_str = "\n".join(self.history[-2:])
        
        prompt = f"""
        Context:
        {context_str}
        
        Event:
        {move_description}
        
        Task: Write a 4-line stanza of rhyming poetry (AABB or ABAB).
        
        Strict Rules:
        1. USE THE SPECIFIC NAMES provided in the Event (e.g. "Squire Cedric", "Lord Malakar").
        2. Do NOT invent new names.
        3. Describe the specific action (Killing, Threatening, or Moving).
        4. Tone: High Fantasy.
        
        Example Output:
        "Sir Galahad rides with a heart so bold,
        To capture the Goblin and steal his gold,
        His lance strikes true with a holy sound,
        And leaves the beast rotting on the ground."
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a bard recording history."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=120, 
                temperature=0.9
            )
            narrative = response.choices[0].message.content.strip()
            self.history.append(narrative)
            return narrative
        except Exception as e:
            return f"The Bard is silent: {str(e)}"