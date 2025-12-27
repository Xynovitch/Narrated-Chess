import tkinter as tk
from gui import ChessApp

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = ChessApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Crucial Error: {e}")
        input("Press Enter to exit...")