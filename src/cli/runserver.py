import dotenv
import sys
import os
import uvicorn

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

dotenv.load_dotenv()


if __name__ == "__main__":
    uvicorn.run(
        "src.server.app:app", host="0.0.0.0", port=8080, reload=True, log_level="info"
    )
