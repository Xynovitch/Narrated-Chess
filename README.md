Here is a professional, ready-to-use `README.md` for your repository. You can create a file named `README.md` in your folder, paste this content in, and push it to GitHub.

---

# ⚔️ Narrated Chess: Chronicles of the 64 Squares

> **"Where every pawn is a hero, and every move is a verse."**

**Narrated Chess** is a Python-based chess application that transforms a standard game into an epic, high-fantasy story. By combining a robust chess engine (Stockfish) with a Large Language Model (OpenAI), this project narrates every move, capture, and checkmate in **real-time rhyming poetry**.

Unlike standard chess narration, this system assigns **persistent identities** to every piece on the board (e.g., "Sir Galahad", "Squire Elric", "The Void Walker"). If a specific Squire captures a Queen, the bard sings of *that specific hero's* victory.

---

## ✨ Features

* **🎭 Epic Poetic Narration:** An AI Bard generates a unique 4-line rhyming stanza for every move in the style of High Fantasy legends.
* **🆔 Persistent Unit Identity:** Every square on the board has a unique RPG name. The system tracks "Sir Valerius" as he rides across the board—he doesn't just become "a knight."
* **🧠 Smart Tactical Awareness:** The narrative engine detects specific tactics (Forks, Pins, Discovered Attacks) and dramatically describes the threat (e.g., "He holds a blade to the throat of the Queen").
* **🤖 Human vs. AI:** Play against the powerful **Stockfish** engine.
* **⚡ Threaded Performance:** The narration runs on background threads, ensuring the chessboard remains smooth and responsive while the poem is being composed.
* **🔒 Secure Configuration:** Uses `.env` environment variables to keep API keys safe.

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Xynovitch/Narrated-Chess.git
cd Narrated-Chess

```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt

```

*(If you don't have a requirements file yet, install these manually:)*

```bash
pip install python-chess stockfish openai python-dotenv

```

### 3. Install Stockfish

You need the Stockfish engine executable for the AI opponent.

* **Mac (Homebrew):** `brew install stockfish`
* **Windows:** Download from [stockfishchess.org](https://stockfishchess.org/download/), extract the ZIP, and note the path to the `.exe` file.

---

## ⚙️ Configuration

This project uses a `.env` file to manage secrets securely.

1. Create a file named `.env` in the root directory.
2. Add your OpenAI API Key and the path to your Stockfish executable:

```env
# .env
OPENAI_API_KEY=sk-proj-your-actual-api-key-here
STOCKFISH_PATH=/opt/homebrew/bin/stockfish
# Note: On Windows, use double backslashes, e.g., C:\\Users\\Name\\stockfish.exe

```

---

## 🚀 Usage

Run the main script to launch the GUI:

```bash
python main.py

```

1. **Play as White:** Click a piece (it highlights yellow), then click a destination square.
2. **Watch the Chronicle:** The text panel on the right will update with a new poem describing your move.
3. **AI Response:** Stockfish will reply instantly as the "Empire of Shadow," triggering its own villainous narration.

---

## 📂 Project Structure

* **`main.py`**: The entry point. Initializes the application.
* **`gui.py`**: Handles the Tkinter window, board rendering, and thread management.
* **`engine.py`**: Manages the Game Logic and Stockfish integration.
* **`narrator.py`**: The "Brain" of the operation. Handles:
* **Identity Tracking:** Maps squares to names (e.g., E1 -> King Theoden).
* **Tactical Analysis:** Detects captures/checks.
* **Prompt Engineering:** Sends instructions to OpenAI to generate rhymes.


* **`config.py`**: Loads environment variables safely.

---

## 🎨 Customization

Want to change the names or the setting?

Open **`narrator.py`** and modify the `_initialize_names` method. You can rename "The Kingdom of Light" to anything you want (e.g., "The Galactic Federation", "The Spartan Army").

You can also modify the **System Prompt** in `generate_narrative` to change the poetic style (e.g., "Homeric Verse", "Cyberpunk Slang", "Shakespearean Sonnet").

---

## 📜 License

This project is open-source. Feel free to fork and modify!