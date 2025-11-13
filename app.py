# app.py (root)
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

# jalankan main App
from main import App  # src/main.py harus punya class App
if __name__ == "__main__":
    App().mainloop()
