import dotenv
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.server.app import app

dotenv.load_dotenv()


if __name__ == "__main__":
    app.start(host="0.0.0.0", port=8080)
