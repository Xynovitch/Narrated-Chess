import os
import sys
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

# ==========================================
# ⚙️ USER CONFIGURATION
# ==========================================

STOCKFISH_PATH = os.getenv("STOCKFISH_PATH")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

MOCK_LLM_MODE = False  # Set to True to test GUI without API costs

# Safety checks
if not MOCK_LLM_MODE and not OPENAI_API_KEY:
    print("❌ CRITICAL: OPENAI_API_KEY not found in .env file.")
    print("   Please create a .env file with OPENAI_API_KEY=...")
    sys.exit(1)

if not STOCKFISH_PATH:
    print("⚠️ WARNING: STOCKFISH_PATH not found in .env file.")
    print("   AI moves might fail. Please add STOCKFISH_PATH=... to .env")